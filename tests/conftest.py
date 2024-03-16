from __future__ import annotations

from datetime import datetime, timedelta

import pytest

from pomodorable.app_data import AppData


@pytest.fixture
def app_data_with_four_test_sessions(tmp_path) -> tuple[AppData, list[datetime]]:
    """Return an AppData instance with some test sessions written to it.
    The AppData instance is created with a temporary directory as the data path.
    A list of start times for the test sessions is also returned.
    There are four test sessions, each with a start, pause, and finish action.
    There are two sessions each day on two consecutive days.
    """

    app_data = AppData(init_data_path=tmp_path)
    assert str(app_data.data_path) == str(tmp_path)

    start_times = [
        datetime.fromisoformat("2024-01-02T08:30:01"),
        datetime.fromisoformat("2024-01-02T09:30:01"),
        datetime.fromisoformat("2024-01-03T08:05:01"),
        datetime.fromisoformat("2024-01-03T08:35:01"),
    ]

    for n, start_time in enumerate(start_times, start=1):
        app_data.write_start(start_time, f"Test session {n}", 10)
        app_data.write_pause(
            pause_time=start_time + timedelta(seconds=2),
            reason=f"Test pause {n}",
            pause_seconds=2,
            session_extended=False,
        )
        app_data.write_finish(
            finish_time=start_time + timedelta(seconds=10), start_time=start_time
        )

    return (app_data, start_times)


@pytest.fixture
def app_data_with_six_test_sessions(tmp_path) -> tuple[AppData, list[datetime]]:
    """Return an AppData instance with some test sessions written to it.
    The AppData instance is created with a temporary directory as the data path.
    A list of start times for the test sessions is also returned.
    There are six test sessions, each with a start, two pauses, and a finish
    or stop action.
    """

    app_data = AppData(init_data_path=tmp_path)
    assert str(app_data.data_path) == str(tmp_path)

    start_times = [
        datetime.fromisoformat("2024-02-01T08:30:01"),
        datetime.fromisoformat("2024-02-01T09:30:01"),
        datetime.fromisoformat("2024-02-01T10:05:01"),
        datetime.fromisoformat("2024-02-02T08:35:01"),
        datetime.fromisoformat("2024-02-02T09:05:01"),
        datetime.fromisoformat("2024-02-02T10:35:01"),
    ]

    for n, start_time in enumerate(start_times, start=1):
        app_data.write_start(start_time, f"Test session {n}", 300)
        app_data.write_pause(
            pause_time=start_time + timedelta(seconds=10),
            reason=f"Test pause {n}",
            pause_seconds=2,
            session_extended=False,
        )
        app_data.write_pause(
            pause_time=start_time + timedelta(seconds=20),
            reason=f"Test pause {n}",
            pause_seconds=10,
            session_extended=True,
        )
        if n in [2, 5]:
            app_data.write_stop(
                stop_time=start_time + timedelta(seconds=100), reason=f"Test STOP {n}"
            )
        else:
            app_data.write_finish(
                finish_time=start_time + timedelta(seconds=310), start_time=start_time
            )

    return (app_data, start_times)
