import logging
from pathlib import Path

import pytest

from pomodorable.app_data import AppData
from pomodorable.ui import CountdownDisplay, PomodorableApp


@pytest.mark.parametrize(
    ("wav_name", "expect_text"),
    [
        ("silent-second.wav", "countdown_finished: playsound called"),
        ("missing.wav", "Sound file not found"),
    ],
)
async def test_app_plays_wav_file_at_finish(tmp_path, wav_name, expect_text):
    app_data = AppData(init_data_path=tmp_path)
    app = PomodorableApp(init_app_data=app_data)

    wav_file = Path(__file__).parent / "data" / wav_name

    app.app_data.config.wav_file = str(wav_file)
    app.app_data.config.do_notify = False

    async with app.run_test() as pilot:
        # Check that the app UI is created.
        footer = pilot.app.query_one("Footer")
        assert footer

        # Set the countdown to 1 second and click Start.
        pilot.app.query_one(CountdownDisplay).seconds = 1
        await pilot.click("#btn-start")

        # Allow time for countdown finish and playsound.
        await pilot.pause(delay=2)

    # Remove the log handler so subsequent tests don't log to the same file.
    logger = logging.getLogger()
    logger.removeHandler(app.app_data._log_handler)  # noqa: SLF001

    # Check that a log file was created and read its contents.
    log_files = list(tmp_path.glob("pomodorable*.log"))
    assert log_files
    log_file = log_files[0]
    log_text = log_file.read_text()

    # Check for the log entry prior to calling playsound.
    # This entry is also prior to checking if the file exists.
    assert f"countdown_finished: playsound '{wav_file}'" in log_text

    # Check for the log entry expected after successfully calling playsound.
    assert expect_text in log_text


async def test_minus_button_stops_at_one(tmp_path):
    app_data = AppData(init_data_path=tmp_path)
    app = PomodorableApp(init_app_data=app_data)
    pause_secs = 0.2  # None
    async with app.run_test() as pilot:
        countdown = pilot.app.query_one("#countdown")
        assert countdown.seconds == 25 * 60  # Should be 25 minutes by default.

        # Also check that plus 5 works.
        logging.debug("CLICK 1")
        await pilot.click("#btn-plus-five")
        await pilot.pause(pause_secs)
        logging.debug("ASSERT 1")
        assert countdown.seconds == 30 * 60

        # Decrease down to five minutes.
        logging.debug("CLICK 2")
        await pilot.click("#btn-minus-five")
        await pilot.pause(pause_secs)
        logging.debug("ASSERT 2")
        assert countdown.seconds == 25 * 60

        logging.debug("CLICK 3")
        await pilot.click("#btn-minus-five")
        await pilot.pause(pause_secs)
        logging.debug("ASSERT 3")
        assert countdown.seconds == 20 * 60

        logging.debug("CLICK 4")
        await pilot.click("#btn-minus-five")
        await pilot.pause(pause_secs)
        logging.debug("ASSERT 4")
        assert countdown.seconds == 15 * 60

        logging.debug("CLICK 5a")
        await pilot.click("#btn-minus-five")
        await pilot.pause(pause_secs)

        logging.debug("CLICK 5b")
        await pilot.click("#btn-minus-five")
        await pilot.pause(pause_secs)
        logging.debug("ASSERT 5")
        assert countdown.seconds == 5 * 60

        # Should stay at 5 minutes.
        logging.debug("CLICK 6")
        await pilot.click("#btn-minus-five")
        await pilot.pause(pause_secs)
        logging.debug("ASSERT 6")
        assert countdown.seconds == 5 * 60

        # Use the minus one button.
        logging.debug("CLICK 7a")
        await pilot.click("#btn-minus-one")
        await pilot.pause(pause_secs)

        logging.debug("CLICK 7b")
        await pilot.click("#btn-minus-one")
        await pilot.pause(pause_secs)
        logging.debug("ASSERT 7")
        assert countdown.seconds == 3 * 60

        # Press 5 more times.
        logging.debug("CLICK 8a")
        await pilot.click("#btn-minus-one")
        await pilot.pause(pause_secs)

        logging.debug("CLICK 8b")
        await pilot.click("#btn-minus-one")
        await pilot.pause(pause_secs)

        logging.debug("CLICK 8c")
        await pilot.click("#btn-minus-one")
        await pilot.pause(pause_secs)

        logging.debug("CLICK 8d")
        await pilot.click("#btn-minus-one")
        await pilot.pause(pause_secs)

        logging.debug("CLICK 8e")
        await pilot.click("#btn-minus-one")
        await pilot.pause(pause_secs)

        # Should have stopped at one minute.
        logging.debug("ASSERT 8")
        assert countdown.seconds == 60


async def test_open_about_screen(tmp_path):
    app_data = AppData(init_data_path=tmp_path)
    app = PomodorableApp(init_app_data=app_data)
    async with app.run_test() as pilot:
        await pilot.pause()
        await pilot.click("#btn-about")
        await pilot.pause()
        close_btn = pilot.app.query_one("#about-close")
        assert close_btn


async def test_open_settings_screen(tmp_path):
    app_data = AppData(init_data_path=tmp_path)
    app = PomodorableApp(init_app_data=app_data)
    async with app.run_test() as pilot:
        await pilot.pause()
        await pilot.click("#btn-settings")
        await pilot.pause()
        settings_input = pilot.app.query_one("#set-log-ret")
        assert settings_input


async def test_bug_settings_screen_close_btn_press_down_arrow(tmp_path):
    """App crash when the Close button in the SettingsScreen has focus, and
    the down arrow key is pressed. This fired the down arrow binding in the
    main app, and it tried to query the CountdownTimer widget which is not
    in scope when the current screen is SettingsScreen. That caused a
    NoMatches exception in DOMQuery. The exception did not happen if the
    mru_list was empty.
    """
    app_data = AppData(init_data_path=tmp_path)

    # Put items in the mru_list.
    app_data.mru_list.add_task("get testy")
    app_data.mru_list.add_reason("feeling testy")
    app_data.mru_list.save()

    app = PomodorableApp(init_app_data=app_data)
    async with app.run_test() as pilot:
        await pilot.pause()
        # Open SettingsScreen.
        await pilot.click("#btn-settings")
        await pilot.pause()
        # Focus the Close button and press down.
        btn_close = pilot.app.query_one("#btn-close")
        assert btn_close
        btn_close.focus()
        await pilot.press("down")


# @pytest.mark.xfail(reason="Not ready to capture reference snapshot")
@pytest.mark.skip(reason="Not ready to capture reference snapshot")
def test_snap_settings_screen(snap_compare):
    async def focus_settings_screen(pilot):
        await pilot.pause()
        await pilot.click("#btn-settings")
        await pilot.pause()

    assert snap_compare("../src/pomodorable/ui.py", run_before=focus_settings_screen)


# @pytest.mark.xfail(reason="Not ready to capture reference snapshot")
@pytest.mark.skip(reason="Not ready to capture reference snapshot")
def test_snap_ui(snap_compare):
    assert snap_compare("../src/pomodorable/ui.py")
