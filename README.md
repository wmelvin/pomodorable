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

### About Screen

The *About* screen is a dialog box showing some information about the application.

- **Version** number of the application.
- **GitHub** button: Open the web browser and go to the source GitHub page.
- File locations:
    - **Data path** shows the directory where the application's data is stored. Output files are written to different locations as configured in the *Settings* screen.
    - **Configuration** shows the full path to the application's configuration file.
- **Close** button: Closes the dialog.

### Settings Screen

The *Settings* screen is where you configure the application. It has the following settings:

- **Session Minutes**: Initial *Countdown* setting on startup, finish, stop, or reset.
- **Running CSV Folder**: <!-- TODO -->
- **Running CSV File Name**: <!-- TODO -->
- **Daily CSV Folder**: <!-- TODO -->
- **Filter CSV Output**: <!-- TODO -->
- **Daily Markdown Folder**: <!-- TODO -->
- **Daily Markdown Heading**: <!-- TODO -->
- **Daily Markdown Append-only**: <!-- TODO -->
- **Filter Markdown Output**: <!-- TODO -->
- **Log Retention Days**: <!-- TODO -->

## Data

### Configuration File

The configuration file is `pomodorable-config.toml` and is stored in a folder named `pomodorable` under the *user config* folder for the operating system. Configuration settings are managed in the *Settings* screen, so do not need to be edited directly in the file.

### Data File

The main data file is `pomodorable-data.csv` and is stored in a folder named `pomodorable` under the *user data* folder for the operating system.

Each **action** (or *event*) recorded by the application is written to this file.

The columns in the CSV file are:

- **version**: The version of the CSV format.
- **date**: The date of the action.
- **time**: The time of the action.
- **action**: The *name* of the action.
- **message**: A message associated with the action.
- **duration**: The duration of the action.
- **notes**: Any notes associated with the action.

This file is not intended to be used directly (though being CSV format, that is easy to do). There are several output files that provide a log of pomodoro sessions for the user.

### Log Files

Log files are also written to the `pomodorable` folder under the system's *user data* folder. 
Each log file is named with the current date.
The number of files to keep is configured in the *Settings* screen.

## Outputs

### Daily and Running CSV

The **Daily CSV** output is for a single day. The folder it is written to can be configured in the *Settings* screen. The name of the file is the current date as *yyyy*-*mm*-*dd*.csv (`2024-04-30`, for example).

The **Running CSV** output spans multiple days (*running* vs *daily*). Both the folder it is written to, and the name of the file, can be configured in the *Settings* screen.

The following columns are in the CSV output files:

- **date**: Date of the action.
- **act**: Action code (see below). When exported via the `--export_csv` CLI option, *Start* actions will instead have the *session number* (daily sequence).
- **time**: Time of the action.
- **task**: Description of the task for *Start* actions, otherwise empty.
- **message**: Message associated with the action. Varies depending on the action.
- **notes**: Note associated with the action. Varies depending on the action.

Action codes:

- **S** - Start
- **E** - Extend (after Pause)
- **R** - Resume (after Pause)
- **F** - Finished session
- **X** - Stopped session

### Daily Markdown

- *TODO*

---

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
