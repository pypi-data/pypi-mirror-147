from datetime import datetime


class Action:
    def __init__(self, job):
        self.job = job
        self.status_snapshot = job.status
        self.status_counter_snapshot = job.status_counter
        self.follow_up_action = None

        self.status = "created"
        self.created_at = datetime.now()

        # No need to use job.lock here since appending to a list is thread safe, apparently
        self.job.action_list.append(self)

    def __str__(self):
        return f"Action: {self.__class__.__name__} {self.job}"

    def to_json(self):
        d = {
            "action": self.__class__.__name__,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
        }
        return d


class Reset(Action):
    pass


class Kill(Action):
    # The action for a "force kill" operation. This results in
    # the same outcome as a Reset: the job should end up in
    # pending state. The only difference is that for a Kill
    pass


class ActionWithDelay(Action):
    def __init__(self, job, delay):
        super().__init__(job)
        self.delay = delay

    def __str__(self):
        return f"Action: {self.__class__.__name__}({self.delay}s) {self.job}"


class RetryAfterDelay(ActionWithDelay):
    pass


class RerunAfterDelay(ActionWithDelay):
    pass


class Run(Action):
    pass


class RunFromSchedule(Action):
    pass


class Spawn(Action):
    pass


class SetCompletedSuccess(Action):
    pass


class SetCompletedFailure(Action):
    pass


class StopProcessingQueueAction(Action):
    """An action which tells the loop which processes the action
    queue to exit
    """

    pass
