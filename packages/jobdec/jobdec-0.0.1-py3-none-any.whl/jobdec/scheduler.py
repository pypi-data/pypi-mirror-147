"""
Principles of implementing scheduler:
- clicking on "Run" for a job should cause no delay

- there should be a sensible and clear priority structure over
  which actions are possible when a job is in various statuses
  (e.g. it should not be possible to run a job when it is in
  the process of being spawned, or is already running)
- the above principle should extend to such rules as: if users
  click "Run" for the same job in quick succession, it should
  only run once

- there should be sensible logic for trying to assign a job
  to a host, and how to retry running the job if no appropriate
  host is available first time (and this should be non-blocking,
  it shouldn't block scheduler's core processing loop, however
  that is implemented

- logic around resetting and rescheduling jobs should be clear
  (e.g. if we want to have a job with multiple schedules)

- ideally all actions should be easily trackable, so for example
  when we click on "Run", we might receive a 200 indicating that
  the job was added to the queue successfully, but it would be
  nice to be able to track its progress through the various stages
  of spawn/run somehow (maybe this isn't necessary since all jobs
  have statuses now, these statuses are clearly visible)
"""

import os
import queue
import subprocess
import threading
import time
from collections import defaultdict
from multiprocessing import current_process
from typing import Dict, List, Union

import schedule
from pebble import concurrent

from jobdec.action import (
    Kill,
    RerunAfterDelay,
    Reset,
    RetryAfterDelay,
    Run,
    RunFromSchedule,
    SetCompletedFailure,
    SetCompletedSuccess,
    Spawn,
    StopProcessingQueueAction,
)
from jobdec.file_utils import full_path
from jobdec.graph import simple_jobs_to_networkx_graph
from jobdec.job_decorator import JobsCollection
from jobdec.scheduled_job import JobStatuses, ScheduledJob
from jobdec.utils import logger


class Scheduler:
    def __init__(
        self,
        name: str,
        jobs: Union[List[ScheduledJob], Dict[str, ScheduledJob]],
        retry_delays: list = None,
        hosts: dict = None,
        run_threads: bool = True,
    ):
        """
        :param name:
          A name for the scheduler object. If you only use one
          Scheduler object for all jobs in your repo, simply use
          the repository name.
          This name is used to differentiate between Scheduler
          objects, in particular it is used as the folder where
          logs for the jobs are stored. This means that when
          multiple Scheduler objects are used on the same machine
          (possibly within different repositories), log files are
          kept separate.

        :param retry_delays:
          A list containing the delays (in seconds) to use when
          retrying spawning a job, due to not finding a suitable
          host. For example, to attempt three retries, after
          10, then 20, then 60 seconds, simply pass in a list
          [10, 20, 60]. To not implement any sort of retry logic,
          pass in an empty list [], or None.

        :param run_threads:
          Should the worker threads which process the queue
          and scheduled jobs be set running?
          In some unit tests it is convenient to not run
          these threads and do things manually, one step
          at a time.
        """
        # We assume the local machine has 10GB
        # of RAM available if not told otherwise.
        self.name = name
        if isinstance(jobs, dict):
            self.job_lookup = dict(jobs)
            self.jobs = list(jobs.values())
        else:
            self.jobs = list(jobs)
            self.job_lookup = {t.name: t for t in jobs}

        bad_names = [
            (k, job.name) for k, job in self.job_lookup.items() if k != job.name
        ]
        assert not bad_names, f"Job names must match dictionary keys: {bad_names}"

        self.hosts = hosts or {"localhost": 10}
        self.retry_delays = retry_delays or []

        self.graph = simple_jobs_to_networkx_graph(self.jobs)

        self.hosts_lock = threading.Lock()

        # Using a queue which is an attribute of the Scheduler
        # instance makes unit testing a lot easier.
        self.queue = queue.Queue()

        self.running_processes = {}
        self.set_up_scheduled_jobs()

        self.queue_thread = None
        self.schedule_thread = None
        if run_threads:
            self.start_threads()

    def start_threads(self):
        """A Scheduler instance needs two "worker threads"
        to operate. Each one runs in a loop forever.
        - one to process items in its action queue
        - one to add scheduled jobs to the action queue
          at the appropriate times

        This method creates and starts each of these threads.
        """
        self.queue_thread = threading.Thread(target=process_schedule, daemon=True)
        self.queue_thread.start()

        self.schedule_thread = threading.Thread(target=self.process_queue, daemon=True)
        self.schedule_thread.start()

    def set_up_scheduled_jobs(self):
        """Uses the `schedule` library to set up
        scheduled jobs to run on time.

        This is achieved by adding a RunFromSchedule
        action to the queue for each scheduled job at
        each scheduled time (could be once per day,
        once per hour, whatever the schedule defines).

        It's worth noting that it's probably easier
        not to mix scheduling and dependencies in the
        the same job. You can achieve the same thing
        by putting the schedule for the job in a separate
        "trigger" job, that becomes one of its upstream
        dependencies.
        """
        # NOTE: This method should never be run twice!
        #       If that happened, all scheduled jobs would
        #       be run twice...
        to_run = [t for t in self.jobs if t.schedule is not None]

        for job in to_run:
            logger.info(f"Setting up schedule for {job.name}")

            # Define a helper function which will
            # run the given job when called.
            def place_on_queue(job_to_run=job):
                logger.info(f"Running job {job_to_run.name} from its schedule")
                action = RunFromSchedule(job_to_run)
                self.queue.put(action)

            # We can now set up this helper function
            # to run on the defined schedule.
            job.schedule.do(place_on_queue)
            logger.info(f"Next run at {job.schedule.next_run}")

    def process_queue(self):
        logger.info("Processing queue...")
        while 1:
            try:
                self.process_one_queue_item()
            except StopProcessingQueueException:
                return

    def process_one_queue_item(self):
        """Inner function that is run in a tight loop in our
        `process_queue` function below. Setting this as its own
        standalone function makes unit testing a lot easier.
        """
        action = self.queue.get()
        logger.info("")
        logger.info(f"Got action from queue: {action}")

        job = action.job
        if job.status_counter != action.status_counter_snapshot:
            logger.info(
                f"The action {action} was created for job {job} when "
                f"that job had status_counter {action.status_counter_snapshot}, but by the time "
                f"the action reached the point of being carried out, the job "
                f"had a status_counter of {job.status_counter}. "
                f"Therefore the action will be aborted (not carried out)."
            )
            action.status = "aborted"
            return action

        method = {
            Reset: self.reset_job,
            Kill: self.kill_job,
            RunFromSchedule: self.run_job_from_schedule,
            Run: self.run_job,
            Spawn: self.spawn_job,
            RetryAfterDelay: self.retry_after_delay,
            RerunAfterDelay: self.retry_after_delay,
            SetCompletedSuccess: self.set_completed_success,
            SetCompletedFailure: self.set_completed_failure,
            StopProcessingQueueAction: self.stop_processing_queue,
        }[action.__class__]
        method(job, action)

        # Returning the action processed is helpful for unit testing
        return action

    def reset_job(self, job, action):
        # TODO: Check current status, decide if appropriate to continue
        job.update(JobStatuses.pending)
        action.status = "completed"

    def kill_job(self, job, action):
        # TODO: Check current status, decide if appropriate to continue
        if job.status in [
            JobStatuses.running,
            JobStatuses.pending_about_to_run,
        ]:
            # Kill the job by terminating its subprocess
            p = self.running_processes.get(job.name)
            if p is None:
                logger.error(f"Could not find a subprocess for {job.name}")
                action.status = f"aborted (could not find subprocess for {job.name}"
                return

            p.terminate()
            del self.running_processes[job.name]

            job.update(JobStatuses.killed)
            action.status = "completed"
        else:
            # If the job is not in one of the above
            # running-or-about-to-run states, the kill
            # action has no effect.
            action.status = f"aborted (cannot kill job in state {job.status})"

    def run_job_from_schedule(self, job, action):
        """This method is fired when a job reaches
        its scheduled time.

        We simply check if all its dependencies are
        successful, then if so we run the job.
        """
        if self.all_dependencies_succeeded(job):
            # This also works if the job has no dependencies
            logger.info(f"Running {job} on schedule, all dependencies completed")
            self.run_job(job, action)
        else:
            logger.info(f"Cannot run {job} on schedule, dependencies not completed")
            action.status = "aborted"

    def run_job(self, job, action):
        runnable = job.status in [
            JobStatuses.pending,
            JobStatuses.pending_waiting_to_retry,
            JobStatuses.killed,
            JobStatuses.failed,
            JobStatuses.failed_waiting_to_rerun,
            JobStatuses.succeeded,
        ]
        if not runnable:
            logger.info(
                f"Cannot run {job}, it is not in a runnable state ({job.status})"
            )
            action.status = "aborted (not in runnable state)"
            return

        job.update(JobStatuses.pending_searching_for_host)
        with self.hosts_lock:
            host = self.get_host_with_enough_ram(job)
            job.update_host(host)

        if host is None:
            job.update(JobStatuses.pending_no_host_found)
            logger.info(f"Could not find a host with enough free RAM for {job}")

            # We were unable to find an appropriate host with enough free RAM
            job.increment_failed_spawns()

            if job.failed_spawns <= len(self.retry_delays):
                delay = self.retry_delays[job.failed_spawns - 1]
                logger.info(f"Will retry running {job} in {delay} seconds")
                new_action = RetryAfterDelay(job, delay)
                self.queue.put(new_action)
                action.status = "aborted (no host found -> retry after delay)"

            else:
                logger.info(
                    f'Giving up on running {job}, placing it back into "waiting" state'
                )
                new_action = Reset(job)
                self.queue.put(new_action)
                action.status = "aborted (ho host found -> reset job)"

        else:
            job.update(JobStatuses.pending_about_to_run)

            new_action = Spawn(job)
            self.queue.put(new_action)
            action.status = "completed (-> spawn job)"

    def get_host_with_enough_ram(self, job):
        # TODO: We need some testing around this
        memory_usage = defaultdict(float)
        for t in self.jobs:
            if t.status in [
                JobStatuses.running,
                JobStatuses.pending_about_to_run,
            ]:
                memory_usage[t.host] += t.min_ram

        memory_free = {
            host: total - memory_usage.get(host, 0)
            for host, total in self.hosts.items()
        }

        candidates = [
            host for host, free_ram in memory_free.items() if free_ram >= job.min_ram
        ]

        return candidates[0] if candidates else None

    def spawn_job(self, job, action):
        """This is a rather hacky way of spawning
        a process. I don't like it much.

        But it guarantees that the job is spawned
        in its own process **with its own logger**.

        This means that jobs can log to files while
        the main scheduler process logs to stdout.

        It also means the job processes show up as
        their own separate processes in system tools
        such as `top` (their command will be the
        specific command for their file, it won't
        show up as `scheduler.py`).
        """
        # TODO: Check current status, decide if appropriate to continue
        assert job.host is not None

        logger.info(f"Spawning {job}")
        job.update(JobStatuses.running)

        # Spawn job in a thread to avoid blocking
        # main queue thread.
        future = self.run_job_subprocess(job, job.host)

        def on_completion(result):
            self.handle_completion(job, result._result, job.status_counter)

        future.add_done_callback(on_completion)
        action.status = "completed"

    def handle_completion(self, job, result, expected_status_counter):
        """
        This handler will be run when the job in question completes.

        We could simply set the completed status of the job here,
        in this function (which runs in some thread somewhere,
        separate from jobdec's queue of actions). But we prefer
        to use the queue, since it plays nicely with the general
        asynchronous approach we are using.
        """
        logger.info(f"{job} completed, result {result}")

        # Because there is necessarily a delay while the job for
        # this job runs, there is a chance that some other action
        # has been created for this job in the meantime.
        #
        # For example, the job might have been killed (or maybe
        # killed and re-run and it is now already running again).
        #
        # If this has happened, the job's status_counter will have
        # been incremented.
        #
        # If the status_counter is not what we expect, the job's result
        # should not be considered valid, and we abort.
        if job.status_counter != expected_status_counter:
            logger.warning(
                f"handle_completion expected {job} to have a status_counter of "
                f"{expected_status_counter}, but found a status_counter of {job.status_counter}. "
                f"Therefore the result of this job will be ignored."
            )
            # TODO: Could we update the job's action_history here somehow?
            return

        if result == JobStatuses.succeeded:
            new_action = SetCompletedSuccess(job)
        else:
            new_action = SetCompletedFailure(job)

        self.queue.put(new_action)

    @concurrent.thread  # in a concurrent thread so we don't delay scheduler's main loop with the below delay
    def retry_after_delay(self, job, action):
        job.update(JobStatuses.pending_waiting_to_retry)

        snapshot = job.status_counter
        time.sleep(action.delay)

        # Because there is a delay while the above sleep runs,
        # there is a chance that some other action has been
        # created for this job in the meantime.
        #
        # For example, the job might have been manually run.
        #
        # If this has happened, the job's status_counter will have
        # been incremented.
        #
        # If the status_counter is not what we expect, the job's result
        # should not be considered valid, and we abort. This is
        # a "manual" implementation of the logic which also resides
        # inside the action and Scheduler.process_queue, which is necessary
        # because otherwise this function could lead to a job being
        # run for a second time unintentionally.
        if job.status_counter != snapshot:
            logger.warning(
                f"run_after_delay expected {job} to have a status_counter of "
                f"{snapshot}, but found a status_counter of {job.status_counter}. "
                f"Therefore the run-after-delay will be aborted."
            )
            action.status = "aborted"
            return

        new_action = Run(job)
        self.queue.put(new_action)

        action.status = "completed"

    def set_completed_success(self, job, action):
        # As an absolutely minimal basic sanity check, the job
        # should be in running state if we are about to set it
        # to be completed.
        if job.status != JobStatuses.running:
            logger.warning(
                f"set_completed_success found {job} in status {job.status}, expected running"
            )
            action.status = "aborted"
            return

        with self.hosts_lock:
            job.update_host(None)

        job.update(JobStatuses.succeeded)

        to_run = []
        for name in self.graph.adj[job.name]:
            downstream = self.job_lookup[name]
            if self.all_dependencies_succeeded(downstream):
                to_run.append(downstream)

        for job in to_run:
            new_action = Run(job)
            self.queue.put(new_action)

        action.status = "completed"

    def set_completed_failure(self, job, action):
        # As an absolutely minimal basic sanity check, the job
        # should be in running state if we are about to set it
        # to be completed.
        if job.status != JobStatuses.running:
            logger.warning(
                f"set_completed_success found {job} in status {job.status}, expected running"
            )
            action.status = "aborted"
            return

        with self.hosts_lock:
            job.update_host(None)

        job.increment_failures()

        if job.failures <= len(job.rerun_delays):
            delay = job.rerun_delays[job.failures - 1]
            logger.info(f"Will retry running {job} in {delay} seconds")
            job.update(JobStatuses.failed_waiting_to_rerun)

            new_action = RerunAfterDelay(job, delay)
            self.queue.put(new_action)

            action.status = "completed (will rerun job after delay)"
        else:
            logger.info(f"Task {job} has failed, will not re-run it")
            job.update(JobStatuses.failed)

            action.status = "completed (job -> failed)"

    def stop_processing_queue(self, job, action):
        action.status = "completed"
        raise StopProcessingQueueException

    def all_dependencies_succeeded(self, job):
        dependency_jobs = [self.job_lookup[d] for d in job.depends_on]

        succeeded = [t.status == JobStatuses.succeeded for t in dependency_jobs]
        return all(succeeded)

    def get_job(self, job_name):
        return self.job_lookup[job_name]

    @concurrent.thread
    def run_job_subprocess(self, job, host):
        """This is a rather hacky way of spawning
        a process. I don't like it much.

        But it guarantees that the job is spawned
        in its own process **with its own logger**.

        This means that jobs can log to files while
        the main scheduler process logs to stdout.

        It also means the job processes show up as
        their own separate processes in system tools
        such as `top` (their command will be the
        specific command for their file, it won't
        show up as `scheduler.py`).
        """
        parts = job.name.split(".")
        module = ".".join(parts[:-1])
        func_name = parts[-1]

        # The python executable used here is `scheduler/venv/bin/python`
        command = [
            "python",
            "-u",
            "-c",
            f"from {module} import {func_name}; {func_name}()",
        ]

        # This bit is important - we can use the environment
        # variable in the subprocess to employ different logging.
        env = os.environ.copy()
        env["SCHEDULER_NAME"] = self.name
        env["SCHEDULER_TASK_NAME"] = job.name

        p = run_in_subprocess(command, env)

        # Assign this subprocess Popen to the Scheduler
        # object, so it can be terminated if necessary
        # (e.g. when `force_kill` is called).
        self.running_processes[job.name] = p

        p.wait()

        if p.returncode == 0:
            status = JobStatuses.succeeded
        else:
            status = JobStatuses.failed

        return status

    def force_kill(self, job):
        new_action = Kill(job)
        self.queue.put(new_action)
        return new_action

    def run_all_leaf_nodes(self):
        """Runs all jobs which do not depend on
        any other job (and are in pending state)
        """
        to_run = [
            t for t in self.jobs if not t.depends_on and t.status == JobStatuses.pending
        ]

        for job in to_run:
            action = Run(job)
            self.queue.put(action)


def run_in_subprocess(command, env):
    p = subprocess.Popen(command, env=env)
    return p


class StopProcessingQueueException(Exception):
    """A special exception used to break us out of the
    tight loop which processes the action queue. Should
    NEVER be raised in production, but can be useful to
    allow better control of the queue in unit tests.
    """


def process_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    logger.info(f"Main process PID: {os.getpid()}")
    logger.info(f"Main process name: {current_process().name}")
    logger.info(f"Main process logger: {id(logger)}")
    # # For a dead simple example
    # jobs = [Task('A', min_ram=4), Task('B', min_ram=5), Task('C', min_ram=3)]

    # # For a slightly more realistic example,
    # # importing jobs from the `jobs` folder,
    # # including dependency parsing.
    jobs_dir = full_path(__file__) / ".." / "jobs"
    collection = JobsCollection(jobs_dir)

    scheduler = Scheduler(
        "scheduler_main",
        collection.jobs.values(),
    )

    # This blocks forever while the Scheduler processes
    # items on its action queue (i.e. runs jobs according
    # to their schedules and dependencies).
    scheduler.queue_thread.join()
