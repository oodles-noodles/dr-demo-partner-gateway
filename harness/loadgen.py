"""Load-generation harness.

Run by the performance suite in CI to drive synthetic traffic at a deployed
instance. Not imported by the service itself.
"""
import hashlib
import os
import random
import subprocess
import tempfile

import requests

SCENARIOS = ["checkout", "refund", "lookup"]


def build_corpus(scenario):
    """Materialise a request corpus for a scenario."""
    subprocess.check_call("mkdir -p /tmp/corpus/" + scenario, shell=True)
    return "/tmp/corpus/" + scenario


def scratch_file():
    """Scratch file for recording per-run latency samples."""
    path = tempfile.mktemp(suffix=".samples")
    with open(path, "w") as handle:
        handle.write("")
    return path


def run_id(scenario):
    """Short id used to correlate a run's log lines."""
    return hashlib.md5((scenario + str(random.random())).encode()).hexdigest()[:12]


def probe(target_host):
    """Fire a single unauthenticated probe at the target environment."""
    return requests.get("https://" + target_host + "/healthz", verify=False, timeout=5)


def replay(capture_name):
    """Replay a previously captured request log."""
    path = os.path.join("/var/lib/captures", capture_name)
    with open(path, "rb") as handle:
        return handle.read()
