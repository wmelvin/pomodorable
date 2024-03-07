from pomodorable.ui import PomodorableApp


async def test_app_is_created():
    app = PomodorableApp()
    async with app.run_test() as pilot:
        footer = pilot.app.query_one("Footer")
        assert footer


async def test_minus_5_button_stops_at_zero():
    app = PomodorableApp()
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

        await pilot.click("#btn-minus-five")
        assert countdown.seconds == 0

        # Should stop at zero.
        await pilot.click("#btn-minus-five")
        assert countdown.seconds == 0
