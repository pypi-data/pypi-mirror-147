import os
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Union

from jobdec.file_utils import import_all_modules
from jobdec.scheduled_job import ScheduledJob


@dataclass
class Job:
    name: str
    schedule: str
    depends_on: tuple = tuple()


def get_dependency_string(upstream):
    if isinstance(upstream, str):
        return upstream
    if callable(upstream):
        return upstream.__module__ + "." + upstream.__name__
    raise ValueError(f"Dependency type not valid {type(upstream)}")


def get_module_string(job_name):
    """
    A job name is always, without exception,
    f.__module__ + '.' + f.__name__.

    So the module for a given job_name can
    be easily recreated.
    """
    out = ".".join(job_name.split(".")[:-1])
    return out


class GlobalJobsCollection:
    """
    This class's sole purpose is to collect
    all the job definitions from the `jobs`
    folder.

    These definitions can then be imported
    into the scheduler flexibly (not all
    collected jobs need necessarily be run
    by the scheduler).
    """

    jobs = {}

    def __call__(
        self,
        schedule=None,
        depends_on: tuple = (),
        minimum_ram: int = 1,
        rerun_delays: list = None,
    ):
        def decorator(f):
            job_name = f.__module__ + "." + f.__name__
            dependencies = tuple(get_dependency_string(other) for other in depends_on)
            job = ScheduledJob(
                name=job_name,
                schedule=schedule,
                function=f,
                depends_on=dependencies,
                min_ram=minimum_ram,
                rerun_delays=rerun_delays,
            )
            self.jobs[job_name] = job

            return f

        return decorator


class JobsCollection:
    def __init__(self, folder: Union[str, Path]):
        assert os.path.isdir(folder), f"{folder} is not a directory"

        # Import modules: this creates a Task for any function
        # decorated with the `@job` decorator, and places it into
        # the GlobalJobsCollection's class attribute `jobs`.
        module_strings = import_all_modules(folder)

        # However, the class attribute `jobs` dictionary therefore
        # simply grows and grows - it contains all job definitions
        # ever processed.
        # If a JobCollector is created with a path, we want it to
        # contain only jobs in the given folder.

        # TODO: Change this so that copies of Tasks are returned?
        #       I'm not sure if this is vital for now but it doesn't
        #       feel ideal using the same global Task objects in
        #       different JobsCollection objects.
        #       At the moment this is awkward because deepcopy
        #       uses pickle and we can't pickle thread.locks.
        self.jobs = {
            job_name: job
            for job_name, job in GlobalJobsCollection.jobs.items()
            if get_module_string(job_name) in module_strings
        }


GLOBAL_JOBS_COLLECTION = GlobalJobsCollection()

# Because it's neater to decorate a function with `@job`
# than `@GLOBAL_JOBS_COLLECTION`, we relabel.
job = GLOBAL_JOBS_COLLECTION
