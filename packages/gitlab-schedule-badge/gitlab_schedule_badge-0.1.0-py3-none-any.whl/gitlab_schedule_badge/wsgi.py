# SPDX-License-Identifier: BSD-2-Clause
# Copyright jdknight

from concurrent.futures import ThreadPoolExecutor
from flask import Flask
from gitlab_schedule_badge.httpd import build_httpd
from gitlab_schedule_badge.state import State


def main() -> Flask:
    """
    mainline (wsgi)

    The mainline for gitlab-schedule-badge when managed by a web service.
    """
    executor = ThreadPoolExecutor()

    state = State(executor)
    state.setup()

    return build_httpd(state)
