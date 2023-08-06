import datetime
import threading
from enum import Enum, auto

from jobdec.utils import logger

# User actions are Run, Kill
# These are the only two actions we need to care about interrupting other actions.
# We could also have SetCompleted actions appearing "out of nowhere", since these
# appear from a separate thread. However they should only ever appear when a job
# is in Running state.


class JobStatuses(Enum):
    pending = auto()
    pending_searching_for_host = auto()
    pending_no_host_found = auto()
    pending_about_to_run = auto()

    # This enum means "waiting to retry, having
    # failed to spawn the job due to not finding
    # a host with enough free memory".
    pending_waiting_to_retry = auto()

    running = auto()
    succeeded = auto()

    # This enum means "the job failed the first
    # time, but it will be re-run soon according
    # to its
    failed_waiting_to_rerun = auto()

    failed = auto()
    killed = auto()


class ScheduledJob:
    def __init__(
        self,
        name,
        function=None,
        depends_on=None,
        schedule=None,
        min_ram=1,
        rerun_delays=None,
    ):
        self.name = name
        self.function = function or (lambda: None)
        self.schedule = schedule
        self.depends_on = depends_on or []
        self.min_ram = min_ram

        self.status = JobStatuses.pending
        self.status_counter = 0
        self.last_updated = datetime.datetime.now().isoformat()

        self.lock = threading.Lock()
        self.failed_spawns = 0
        self.host = None
        self.action_list = []

        self.failures = 0
        self.rerun_delays = rerun_delays or []

    @property
    def next_run(self):
        return self.schedule.next_run if self.schedule else None

    def __str__(self):
        return f"Task({self.name}: {self.min_ram}MB)"

    def to_json(self):
        next_run = self.next_run
        scheduled_at = next_run.isoformat() if next_run else None
        d = {
            "name": self.name,
            "scheduled_at": scheduled_at,
            "depends_on": self.depends_on,
            "min_ram": self.min_ram,
            "status": self.status.name,
            "status_counter": self.status_counter,
            "last_updated": self.last_updated,
            "failed_spawns": self.failed_spawns,
            "host": str(self.host),
            "actions": [a.to_json() for a in self.action_list],
            "failures": self.failures,
            "rerun_delays": self.rerun_delays,
        }
        return d

    def update(self, new_status):
        with self.lock:
            self.status = new_status
            self.last_updated = datetime.datetime.now().isoformat()
            self.status_counter += 1
            logger.info(f"{self} -> {self.status.name} ({self.status_counter})")

    def increment_failed_spawns(self):
        with self.lock:
            self.failed_spawns += 1

    def increment_failures(self):
        with self.lock:
            self.failures += 1

    def update_host(self, host):
        self.host = host
