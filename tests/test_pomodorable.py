from pomodorable.ui import PomodoroApp


async def test_app_is_created():
    app = PomodoroApp()
    async with app.run_test() as pilot:
        footer = pilot.app.query_one("Footer")
        assert footer
