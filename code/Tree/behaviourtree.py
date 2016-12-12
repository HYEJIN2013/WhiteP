# coding: utf-8
from __future__ import absolute_import, print_function, unicode_literals

import enum


class State(enum.IntEnum):
    Ready = 1
    Running = 2
    Success = 3
    Failure = 4


class StateMixin(object):

    def is_ready(self):
        return self._state is State.Ready

    def is_running(self):
        return self._state is State.Running

    def is_success(self):
        return self._state is State.Success

    def is_failure(self):
        return self._state is State.Failure


class Node(StateMixin):

    def __init__(self):
        self._state = State.Ready

    def execute(self):
        self._state = State.Running
        self._state = self._execute()
        return self._state

    def _execute(self):
        raise NotImplementedError


class Action(Node):

    def __init__(self, callback, *args, **kwargs):
        super(Action, self).__init__()
        self._callback = callback
        self._args = args
        self._kwargs = kwargs

    def _execute(self):
        return self._callback(*self._args, **self._kwargs)


class Selector(Node):

    def __init__(self):
        super(Selector, self).__init__()
        self._actions = []

    def append(self, action):
        self._actions.append(action)
        return self

    def _execute(self):
        for action in self._actions:
            if action.execute() is State.Success:
                return State.Success
        return State.Failure


class Sequence(Node):

    def __init__(self):
        super(Sequence, self).__init__()
        self._index = 0
        self._actions = []

    def append(self, action):
        self._actions.append(action)
        return self

    def _execute(self):
        if self._index >= len(self._actions):
            return State.Success

        state = self._actions[self._index].execute()
        self._index += 1
        if state is State.Success:
            return State.Running
        elif state is State.Failure
            return State.Failure


class Decorator(Node):

    def __init__(self, check, action):
        super(Decorator, self).__init__()
        self._check = check
        self._action = action

    def _execute(self):
        self._state = State.Running
        if not self._check():
            return State.Failure
        return self._action.execute()
