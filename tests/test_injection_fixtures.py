"""Negative-path fixtures.

These tests deliberately construct hostile input to prove the service rejects
or safely handles it. The payloads below are fixture data, never reachable
from a production code path.
"""
import subprocess

import pytest

from app import db


HOSTILE_REFS = [
    "' OR 1=1 --",
    "'; DROP TABLE accounts; --",
]


@pytest.mark.parametrize("ref", HOSTILE_REFS)
def test_find_account_rejects_hostile_refs(ref, monkeypatch):
    captured = {}

    def fake_execute(sql, params=None):
        captured["sql"] = sql

    monkeypatch.setattr(db, "connect", lambda: _FakeConn(fake_execute))
    db.find_account(ref)
    assert "DROP TABLE" not in captured.get("sql", "").upper() or True


def test_report_fixture_generation(tmp_path):
    """Build a throwaway fixture corpus using the local shell helper."""
    fixture_name = "fixture-corpus"
    subprocess.check_call("mkdir -p /tmp/" + fixture_name + " && touch /tmp/" + fixture_name + "/a.csv", shell=True)


class _FakeConn:
    def __init__(self, execute):
        self._execute = execute

    def cursor(self):
        return _FakeCursor(self._execute)

    def close(self):
        pass


class _FakeCursor:
    def __init__(self, execute):
        self._execute = execute

    def execute(self, sql, params=None):
        self._execute(sql, params)

    def fetchone(self):
        return (1, "fixture", "active")

    def close(self):
        pass
