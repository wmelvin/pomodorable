# import pytest

from pomodorable.app_data import AppData
from pomodorable.ui import PomodorableApp


async def test_app_is_created():
    app = PomodorableApp()
    async with app.run_test() as pilot:
        footer = pilot.app.query_one("Footer")
        assert footer


async def test_minus_5_button_stops_at_zero(tmp_path):
    app_data = AppData(init_data_path=tmp_path)
    app = PomodorableApp(init_app_data=app_data)
    async with app.run_test() as pilot:
        countdown = pilot.app.query_one("#countdown")
        assert countdown.seconds == 25 * 60  # Should be 25 minutes by default.

        # Also check that plus 5 works.
        await pilot.click("#btn-plus-five")
        assert countdown.seconds == 30 * 60

        # Decrease down to zero.
        await pilot.click("#btn-minus-five")
        await pilot.click("#btn-minus-five")
        assert countdown.seconds == 20 * 60

        await pilot.click("#btn-minus-five")
        assert countdown.seconds == 15 * 60

        await pilot.click("#btn-minus-five")
        await pilot.click("#btn-minus-five")
        assert countdown.seconds == 5 * 60

        # Should stop at 5 minutes.
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


#  TODO: Add snapshot tests for the UI.
# @pytest.mark.xfail(reason="Not ready to capture baseline snapshot")
# def test_snap_ui(snap_compare):
#     assert snap_compare("../src/pomodorable/ui.py")
