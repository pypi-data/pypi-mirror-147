#!/usr/bin/env python3

import argparse
import logging
import os
import os.path
import signal
import psutil

logging.basicConfig(
    format="%(levelname)s:%(funcName)s:%(message)s", level=logging.INFO
)
log = logging.getLogger(__name__)

VERSION = "0.1.2"

def find_procs_by_name(name):
    "Return a list of processes matching 'name'."
    ls = []
    for p in psutil.process_iter(["name", "exe", "cmdline"]):
        if (
            name == p.info["name"]
            or p.info["exe"]
            and os.path.basename(p.info["exe"]) == name
            or p.info["cmdline"]
            and [x for x in p.info["cmdline"] if name in x]
        ):
            ls.append(p)
    return ls


def substr_in_list(sstr, list):
    log.debug(f"sstr = {sstr}, list = {list}")
    out = [x for x in list if sstr in x]
    log.debug(f"{out}")
    return bool(out)


def find_ancestory_by_name(p, name):
    # Recursion got to the top, return with None
    log.debug(f"process = {p}")
    if p == 1:
        return None
    else:
        if (
            name == p.name()
            or (p.exe() and os.path.basename(p.exe()) == name)
            or (p.cmdline() and substr_in_list(name, p.cmdline()))
        ):
            return p
        else:
            return find_ancestory_by_name(psutil.Process(p.ppid()), name)


def kill_proc_tree(pid, sig=signal.SIGTERM, include_parent=True, timeout=None):
    """Kill a process tree (including grandchildren) with signal
    "sig" and return a (gone, still_alive) tuple.
    """
    if isinstance(pid, psutil.Process):
        parent = pid
    elif isinstance(pid, int):
        parent = psutil.Process(pid)
    assert parent.pid != os.getpid(), "won't kill myself"
    children = parent.children(recursive=True)
    if include_parent:
        children.append(parent)
    for p in children:
        try:
            p.terminate()
        except psutil.NoSuchProcess:
            pass
    gone, alive = psutil.wait_procs(children, timeout=5)
    for p in alive:
        try:
            p.kill()
        except psutil.NoSuchProcess:
            pass


def main():
    parser = argparse.ArgumentParser(
        description="Nero: patricide, kill an ancestor")
    parser.add_argument("child",
                        help="name of the child process")
    parser.add_argument("parent",
                        help="name of the parent process to be killed")
    args = parser.parse_args()

    ch_proc = find_procs_by_name(args.child)
    cur_pid = os.getpid()
    # remove itself from the list of child processes
    ch_proc = [x for x in ch_proc if x.pid != cur_pid]
    if ch_proc:
        to_be_killed = find_ancestory_by_name(ch_proc[0], args.parent)
    kill_proc_tree(to_be_killed)


if __name__ == "__main__":
    main()
