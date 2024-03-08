from datetime import datetime, timedelta

from pomodorable.app_data import AppData


def test_get_latest_session_rows(tmp_path):
    app_data = AppData(init_data_path=tmp_path)
    assert str(app_data.data_path) == str(tmp_path)
    #  Write some fake sessions.
    dt = datetime(2024, 1, 2, 3, 4, 56)
    app_data.write_start(dt, "Test session 1", 10)
    dt = dt + timedelta(seconds=2)
    app_data.write_pause(
        pause_time=dt,
        reason="Test pause 1",
        pause_seconds=2,
        session_extended=False
    )
    dt = dt + timedelta(seconds=8)
    app_data.write_finish(
        finish_time=dt,
        start_time=dt - timedelta(seconds=10)
    )
    rows = app_data.get_latest_session_rows()
    assert rows
