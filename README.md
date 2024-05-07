# pomodorable

A **pomodoro timer** built using Textual.

> Development work in progress.

<!-- ![Picture of a Pomodoro Timer](./readme_images/pomororo-timer-200.jpg) -->
<p align="center">
<a href="https://github.com/wmelvin/pomodorable/raw/main/readme_images/pomororo-timer-200.jpg">
<img src="https://github.com/wmelvin/pomodorable/raw/main/readme_images/pomororo-timer-200.jpg"
alt="Picture of a Pomodoro Timer"/></a></p>

## Screenshots

<!-- ![Screenshot animation](./readme_images/app-1.gif) -->
<p align="center">
<a href="https://github.com/wmelvin/pomodorable/raw/main/readme_images/app-1.gif">
<img src="https://github.com/wmelvin/pomodorable/raw/main/readme_images/app-1.gif"
alt="Screenshot animation"/></a></p>

## Using the Application

### Modes

1. **Ready**
    - Initial mode when the application starts.
    - Returned to when a session is *finished* or *stopped*.
2. **Running**
    - Entered when the *Start* button is pressed.
    - Returned to when *Extend* or *Resume* is chosen in *paused* mode.
3. **Paused**
    - Entered when the *Pause* button is pressed.
    - Ended by pressing *Extend*, *Resume* or *Stop*.

### Display and Inputs

#### Times Display

- **Countdown** display: Shows the time remaining in the current session.
- **Start Time** display: Shows the Start time of the current session. When a session is not *running* it shows the current time.
- **End Time** display: Shows the End time of the current session. When a session is not *running* it shows the current time plus the session length.

#### Settings Panel

- **Reset** button: Resets the *Countdown* to the configured session length (default setting is 25 minutes).
- **+5**, **+1**, **-1**, **-5** buttons: Increment or decrement the *Countdown* by minutes.
- **?** (About) button: Open the *About* screen.
- **Settings** button: Open the *Settings* screen.

#### Task Panel

- **Task description** input box: A brief description of the task at hand (optional). Press the **down arrow** key to open a list of recently used descriptions to pick from.
- **Start** button: Starts the session. Countdown begins. Time displays show Start and End times for the running session.

#### Pause Panel - Running

- **Pause** button: Pause the running session.
- **Reason description** input box: Disabled when *running*.

#### Pause Panel - Paused

- **Pause** button: Disabled when *paused*.
- **Reason description** input box: Enter the reason for pausing (optional). Press the **down arrow** key to open a list of recently used descriptions to pick from.
- **Extend** button: Return to *running*. Add the paused duration to the end-time to complete the full session length time-on-task.
- **Resume** button: Return to *running*. Resume the session from the current time. The pause duration is subtracted from the countdown, reducing the session's time-on-task.
- **Stop** button: Finish the session now. Return to *ready* mode.

#### Timer Bar

- Mimics the markings on a classic pomodoro (tomato-shaped) kitchen timer.
- Shows the current countdown minute at the pointer.

#### Log Panel

- Shows messages from the application with a timestamp.

## Reference

- [Pomodoro Technique - Wikipedia](https://en.wikipedia.org/wiki/Pomodoro_Technique)

### Packages used

- [Textual](https://textual.textualize.io/) - Textual User Interface framework
- [Click](https://palletsprojects.com/p/click/) - command-line options
- [platformdirs](https://github.com/platformdirs/platformdirs#readme) - common directories on different platforms
- [plyer](https://pypi.org/project/plyer/) - system notifications
- [python-dotenv](https://pypi.org/project/python-dotenv/) - override default settings during development
- [tomlkit](https://pypi.org/project/tomlkit/) - store configuration as TOML

### Project tools

- [Hatch](https://hatch.pypa.io/latest/) - Python project manager (environments, packaging, and more)
- [Ruff](https://docs.astral.sh/ruff/) - linter and code formatter (integrated with Hatch)
- [pytest](https://docs.pytest.org/en/stable/) - testing framework
- [Just](https://github.com/casey/just#readme) - command runner

#### Textual Development Tools

- Textual [Devtools](https://textual.textualize.io/guide/devtools/)
- [tcss-vscode-extension](https://github.com/Textualize/tcss-vscode-extension#readme): VS Code extension that enables syntax highlighting for Textual CSS files.
- [pytest-textual-snapshot](https://github.com/Textualize/pytest-textual-snapshot#readme): Snapshot testing for Textual applications
