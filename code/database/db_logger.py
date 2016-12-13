# -*- coding: utf-8 -*-


from __future__ import absolute_import, division, print_function

import os
import os.path
import sqlite3
import time
import uuid

import ansible.plugins.callback as callback


DB_SCHEMA = """
CREATE TABLE log (
    id INTEGER PRIMARY KEY,
    request_id TEXT NOT NULL,
    task TEXT NOT NULL,
    role TEXT,
    playbook TEXT NOT NULL,
    host_name TEXT NOT NULL,
    time_start INTEGER NOT NULL,
    time_finish INTEGER,
    result INTEGER,
    error_message TEXT,
    UNIQUE(request_id, playbook, task, host_name)
);
""".strip()
"""Schema of database."""

DB_FILENAME = "execution.sqlite"
"""Database filename."""

TASK_RESULT_OK = 0
TASK_RESULT_FAILED = 1
TASK_RESULT_UNREACHABLE = 2
TASK_RESULT_SKIPPED = 3
"""Task complete status codes."""


class CallbackModule(callback.CallbackBase):

    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = "notification"
    CALLBACK_NAME = "db_logger"

    @staticmethod
    def ensure_db_created(database=DB_FILENAME):
        need_to_create = os.path.exists(database)

        connection = sqlite3.connect(database)
        if need_to_create:
            connection.executescript(DB_SCHEMA)
            connection.commit()

        return connection

    def __init__(self, display=None):
        super(CallbackModule, self).__init__(display)

        self.connection = self.ensure_db_created()
        self.request_id = os.getenv("REQUEST_ID", str(uuid.uuid4()))
        self.time_of_start = {}
        self.playbook = None

    def add_task_result(self, result, result_code):
        self.connection.execute(
            "INSERT INTO log(request_id, task, role, playbook, host_name, "
            "time_start, time_finish, result, error_message) "
            "VALUES (:request_id, :task, :role, :playbook, :host_name, "
            ":time_start, :time_finish, :result, :error_message)",
            {
                "request_id": self.request_id,
                "task": result._task.get_name(),
                "role": result._task._role.get_name(),
                "playbook": self.playbook.name,
                "host_name": result._host.name,
                "time_start": self.time_of_start[result._task._uuid],
                "time_finish": int(time.time()),
                "result": result_code,
                "error_message": ""
            }
        )
        self.connection.commit()

    def v2_playbook_on_play_start(self, play):
        self.playbook = play

    def v2_playbook_on_task_start(self, task, is_conditional):
        self.time_of_start[task._uuid] = int(time.time())

    def v2_runner_on_ok(self, result, **kwargs):
        self.add_task_result(result, TASK_RESULT_OK)

    def v2_runner_on_failed(self, result, **kwargs):
        self.add_task_result(result, TASK_RESULT_FAILED)

    def v2_runner_on_unreachable(self, result, **kwargs):
        self.add_task_result(result, TASK_RESULT_UNREACHABLE)

    def v2_runner_on_skipped(self, result, **kwargs):
        self.add_task_result(result, TASK_RESULT_SKIPPED)
