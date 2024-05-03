import pytest

from pomodorable.app_data import AppData
from pomodorable.ui import PomodorableApp


async def test_app_is_created():
    app = PomodorableApp()
    async with app.run_test() as pilot:
        footer = pilot.app.query_one("Footer")
        assert footer


async def test_minus_button_stops_at_one(tmp_path):
    app_data = AppData(init_data_path=tmp_path)
    app = PomodorableApp(init_app_data=app_data)
    async with app.run_test() as pilot:
        countdown = pilot.app.query_one("#countdown")
        assert countdown.seconds == 25 * 60  # Should be 25 minutes by default.

        # Also check that plus 5 works.
        await pilot.click("#btn-plus-five")
        assert countdown.seconds == 30 * 60

        # Decrease down to five minutes.
        await pilot.click("#btn-minus-five")
        await pilot.click("#btn-minus-five")
        assert countdown.seconds == 20 * 60

        await pilot.click("#btn-minus-five")
        assert countdown.seconds == 15 * 60

        await pilot.click("#btn-minus-five")
        await pilot.click("#btn-minus-five")
        assert countdown.seconds == 5 * 60

        # Should stay at 5 minutes.
        await pilot.click("#btn-minus-five")
        assert countdown.seconds == 5 * 60

        # Use the minus one button.
        await pilot.click("#btn-minus-one")
        await pilot.click("#btn-minus-one")
        assert countdown.seconds == 3 * 60

        # Press 5 more times.
        await pilot.click("#btn-minus-one")
        await pilot.click("#btn-minus-one")
        await pilot.click("#btn-minus-one")
        await pilot.click("#btn-minus-one")
        await pilot.click("#btn-minus-one")

        # Should have stopped at one minute.
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
