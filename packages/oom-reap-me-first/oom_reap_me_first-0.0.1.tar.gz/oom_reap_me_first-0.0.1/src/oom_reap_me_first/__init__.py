from glob import glob
import os


VERSION = "0.0.1"


def read_oom_score(pid):
    return _read_oom_from_file_path(f"/proc/{pid}/oom_score")


def read_oom_score_adj(pid):
    return _read_oom_from_file_path(f"/proc/{pid}/oom_score_adj")


def get_current_max_oom_score():
    return max(_read_oom_from_file_path(path) for path in glob("/proc/*/oom_score"))


def get_current_max_oom_score_adj():
    return max(_read_oom_from_file_path(path) for path in glob("/proc/*/oom_score_adj"))


def set_oom_score_adj(pid, score=1_000):
    with open(f"/proc/{pid}/oom_score_adj", "w") as fp:
        fp.write(str(score))


def _read_oom_from_file_path(path):
    with open(path) as fp:
        return int(fp.read())


def run():
    set_oom_score_adj(os.getpid())
