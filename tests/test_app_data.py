from datetime import datetime, timedelta

from pomodorable.app_data import AppData


def test_get_latest_session_rows(tmp_path):
    app_data = AppData(init_data_path=tmp_path)
    assert str(app_data.data_path) == str(tmp_path)

    #  Write some fake sessions.
    start_time_1 = datetime(2024, 1, 2, 3, 5, 0)
    app_data.write_start(start_time_1, "Test session 1", 10)

    app_data.write_pause(
        pause_time=start_time_1 + timedelta(seconds=2),
        reason="Test pause 1",
        pause_seconds=2,
        session_extended=False
    )

    app_data.write_finish(
        finish_time=start_time_1 + timedelta(seconds=10),
        start_time=start_time_1
    )

    start_time_2 = datetime(2024, 1, 2, 4, 5, 0)
    app_data.write_start(start_time_2, "Test session 2", 10)

    app_data.write_pause(
        pause_time=start_time_2 + timedelta(seconds=2),
        reason="Test pause 2",
        pause_seconds=2,
        session_extended=False
    )

    app_data.write_finish(
        finish_time=start_time_2 + timedelta(seconds=10),
        start_time=start_time_2
    )

    rows = app_data.get_latest_session_rows()
    assert rows
    assert len(rows) == 3
    assert rows[0]["action"] == "Start"
    assert rows[0]["message"] == "Test session 2"
    assert rows[0]["time"] == "04:05:00"
    assert rows[1]["action"] == "Pause"
    assert rows[2]["action"] == "Finish"
