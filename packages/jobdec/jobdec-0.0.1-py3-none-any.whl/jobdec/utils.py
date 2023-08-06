import logging
import os


def set_up_logging():
    # create logger
    logger = logging.getLogger("__pyschedule__")
    logger.setLevel(logging.INFO)

    # create formatter
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    # We now decide what sort of logging to do,
    # based on whether we're in a scheduler job
    # process, or the main process.
    scheduler_name = os.environ.get("SCHEDULER_NAME")
    job_name = os.environ.get("SCHEDULER_TASK_NAME")
    if scheduler_name and job_name:
        # We're in a scheduler process, log to
        # an appropriate folder and file in /tmp
        folder = f"/tmp/{scheduler_name}"
        if not os.path.exists(folder):
            os.mkdir(folder)

        filename = f"{folder}/{job_name}.txt"
        handler = logging.FileHandler(filename)
    else:
        # We're in the main process, log to stdout
        handler = logging.StreamHandler()

    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger


logger = set_up_logging()
