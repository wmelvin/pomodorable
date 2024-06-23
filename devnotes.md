
# devnotes


## Initial Setup

Use Hatch to create project scaffold.

``` bash
mkdir -p ~/Projects/Pomodorable
cd ~/Projects/Pomodorable
hatch new pomodorable
```

Decided to change the name of the project root directory to `pomodorable-project`.

``` bash
mv pomodorable pomodorable-project
cd ~/Projects/Pomodorable/pomodorable-project
```

Created a git repository.

Edited some of the hatch boilerplate in the generated files prior to initial commit.

``` bash
git init -b main
git add .
git commit -m "Initial commit"
```

## Links and Commits

- [x] **Initial commit**
<sup>Commit [cc10a7c](https://github.com/wmelvin/pomodorable/commit/cc10a7ce15044ccebb59eb2eab4778dda3553df5) (2024-02-28 16:28:19)</sup>

- [x] **Add initial ui, test, and tcss files**
<sup>Commit [0265689](https://github.com/wmelvin/pomodorable/commit/02656890bc0bebd9100789e4f95ea46c60675dfd) (2024-02-28 16:59:03)</sup>

---

- Ready
    - Start (input: task description)
- Countdown
    - Pause (input: reason)
        - Resume -> Countdown
        - Extend -> (add duration of pause) -> Countdown
        - Stop

- [x] **Initial UI mock-up**
<sup>Commit [a5c4946](https://github.com/wmelvin/pomodorable/commit/a5c4946a5e95c77d5003585b509ef8a3390e562a) (2024-02-29 10:02:05)</sup>

- [x] **Add CountdownDisplay**
<sup>Commit [e257aef](https://github.com/wmelvin/pomodorable/commit/e257aefadd48403104595887ebb69a0ba7889a03) (2024-02-29 10:25:53)</sup>

- [x] **Add frame with buttons to set time. Rename ids**
<sup>Commit [0d10498](https://github.com/wmelvin/pomodorable/commit/0d1049863c00acef134be2f0ac50081a7403f955) (2024-03-01 10:45:20)</sup>

- [x] **Initial countdown and time display implementation**
<sup>Commit [12cbf40](https://github.com/wmelvin/pomodorable/commit/12cbf402fcf6bff41e28f8744c1d4c8f4c25950b) (2024-03-01 12:00:51)</sup>

---

Hatch: [persistent-config - Static analysis configuration](https://hatch.pypa.io/latest/config/internal/static-analysis/#persistent-config)

- [x] **Add ruff_defaults.toml for Hatch linting configuration**
<sup>Commit [b182147](https://github.com/wmelvin/pomodorable/commit/b182147c11ba2dd0f55de4bf2bc80f25753405de) (2024-03-01 12:21:41)</sup>

- [x] **Update line length and reformat**
<sup>Commit [01c6caa](https://github.com/wmelvin/pomodorable/commit/01c6caaee2ab080af2e4930ec1126cf4b5c34002) (2024-03-01 12:24:13)</sup>

---

- [x] **Add display control for different app states**
<sup>Commit [92f6048](https://github.com/wmelvin/pomodorable/commit/92f604801fc12768a9a987efedf39b1b74a0b524) (2024-03-01 12:59:00)</sup>

- [x] **Implement countdown and button functionality**
<sup>Commit [25f46b9](https://github.com/wmelvin/pomodorable/commit/25f46b90c694874d4a3dc89c158fd1365e214168) (2024-03-01 15:57:49)</sup>

- [x] **Keep time display in sync with countdown setting**
<sup>Commit [57cc053](https://github.com/wmelvin/pomodorable/commit/57cc0539d1f61e293a7be21c068fd620451767c8) (2024-03-01 16:37:59)</sup>

- [x] **Update version and hide header icon**
<sup>Commit [120736b](https://github.com/wmelvin/pomodorable/commit/120736b935c44eb1abc2a98a3e760a9137c54064) (2024-03-01 17:14:27)</sup>

- [x] **Add to README and add dependencies**
<sup>Commit [f1dbfd1](https://github.com/wmelvin/pomodorable/commit/f1dbfd1921715b5d977dc0967f7b224e4d745b72) (2024-03-01 17:47:51)</sup>

- [x] **Add AppData class to handle configuration and file output**
<sup>Commit [b896d77](https://github.com/wmelvin/pomodorable/commit/b896d7780522498c94e5138530258768c25e6915) (2024-03-01 22:10:41)</sup>

---

 Textual: [color-preview - Design System](https://textual.textualize.io/guide/design/#color-preview)

Package: [python-dotenv](https://pypi.org/project/python-dotenv/)

- [x] **Use dotenv to configure a development mode**
<sup>Commit [9335fb2](https://github.com/wmelvin/pomodorable/commit/9335fb2f74d67c853ab49fdc1a1d02b83c9d7704) (2024-03-02 09:50:31)</sup>

- [x] **Add logging**
<sup>Commit [2bdbb10](https://github.com/wmelvin/pomodorable/commit/2bdbb10a30f0f33c2099ac83c3001096549616cc) (2024-03-02 10:14:30)</sup>

- [x] **Add notification when session is finished**
<sup>Commit [cc44fb7](https://github.com/wmelvin/pomodorable/commit/cc44fb71c1883756ad7d85507fefa7d3ed4371ea) (2024-03-02 10:24:51)</sup>

- [x] **Add cli.py and __main__.py**
<sup>Commit [aa1cf78](https://github.com/wmelvin/pomodorable/commit/aa1cf78043459792fdd967a1679c3a87408065d5) (2024-03-02 11:41:15)</sup>

---

Ruff - [error-suppression](https://docs.astral.sh/ruff/linter/#error-suppression)

Click - Options - [boolean-flags](https://click.palletsprojects.com/en/8.1.x/options/#boolean-flags)

Package: [tomlkit](https://pypi.org/project/tomlkit/)

TOML Kit - [API Reference](https://tomlkit.readthedocs.io/en/latest/api/#module-tomlkit.toml_document)

- [x] **Add configuration options to CLI**
<sup>Commit [6d5b158](https://github.com/wmelvin/pomodorable/commit/6d5b15874f272105a2d4553296b66bbbd3256a0d) (2024-03-03 11:29:47)</sup>

- [x] **Add initial tests for CLI**
<sup>Commit [cb4c516](https://github.com/wmelvin/pomodorable/commit/cb4c51690c33393b049cf03857ac9ac0d35f69b2) (2024-03-03 14:20:51)</sup>

- [x] **Add AppConfig class and tests. Use TOML for config file**
<sup>Commit [39b0eaa](https://github.com/wmelvin/pomodorable/commit/39b0eaac5c1bfdc9d39e29b150f73a748be02f10) (2024-03-03 15:08:21)</sup>

- [x] **Fix parameter name and add another test**
<sup>Commit [51e92cc](https://github.com/wmelvin/pomodorable/commit/51e92cc7377f6b8bdd02db341243f024ce64703c) (2024-03-03 15:21:20)</sup>

---

- [x] **Add DataRow class and use for writing data to CSV**
<sup>Commit [82f767b](https://github.com/wmelvin/pomodorable/commit/82f767b283cefdd3a03337e910057c74abc40ff5) (2024-03-04 12:01:54)</sup>

---

- [x] **Add initial SettingsScreen**
<sup>Commit [0b62f01](https://github.com/wmelvin/pomodorable/commit/0b62f01cc476d3120cc1f3fcf3ef3ee728f58584) (2024-03-05 09:55:57)</sup>

- [x] **Add SettingInput widget and apply style**
<sup>Commit [50f320a](https://github.com/wmelvin/pomodorable/commit/50f320a3b1f2f7b765d15594ffd0e083adf9e9f0) (2024-03-05 11:33:39)</sup>

---

Textual - [Validating Input](https://textual.textualize.io/widgets/input/#validating-input)

Textual - API - [Validation](https://textual.textualize.io/api/validation/)


- [x] **Implement settings Input, validation, and save**
<sup>Commit [99a7d44](https://github.com/wmelvin/pomodorable/commit/99a7d447647fc5e9c88704acbff0f23920b1abb1) (2024-03-06 12:50:52)</sup>

- [x] **Move AppConfig data attributes to a dataclass**
<sup>Commit [0f091d9](https://github.com/wmelvin/pomodorable/commit/0f091d9c35a6ff90fa3a91788d3466a2bb6571af) (2024-03-06 15:34:33)</sup>

Python documentation - Logging handlers - [TimedRotatingFileHandler](https://docs.python.org/3/library/logging.handlers.html#timedrotatingfilehandler)

- [x] **Add log retention days to app configuration**
<sup>Commit [1e3d92e](https://github.com/wmelvin/pomodorable/commit/1e3d92e030c59c5b91479d0ffeea59456d3ad490) (2024-03-06 17:20:19)</sup>

Textual - Events and Messages - [Stopping bubbling](https://textual.textualize.io/guide/events/#stopping-bubbling)

- [x] **Stop button press event  from bubbling to SettingInput parent**
<sup>Commit [fdf0853](https://github.com/wmelvin/pomodorable/commit/fdf0853031ac096e07497e1eec88099ecde61c68) (2024-03-06 17:38:43)</sup>

- [x] **Remove CLI options now on SettingsScreen**
<sup>Commit [435a679](https://github.com/wmelvin/pomodorable/commit/435a6797fc85ff99de212e45e6603bc61175e093) (2024-03-06 19:21:05)</sup>

- [x] **Apply formatting**
<sup>Commit [4de7a87](https://github.com/wmelvin/pomodorable/commit/4de7a87ac5ca74058414d0440cf79a76de691fbc) (2024-03-06 19:23:07)</sup>

---

Ruff - [Error ssuppression](https://docs.astral.sh/ruff/linter/#error-suppression)

Python - Built-in Functions - [property](https://docs.python.org/3/library/functions.html#property)

Python - pathlib - [pathlib.Path.rename](https://docs.python.org/3/library/pathlib.html#pathlib.Path.rename)

Textual - Testing - [Simulating clicks](https://textual.textualize.io/guide/testing/#simulating-clicks)

- [x] **Refactor AppConfig load and save**
<sup>Commit [96e9811](https://github.com/wmelvin/pomodorable/commit/96e9811ede820ccf345b05733117bf90e6ece395) (2024-03-07 10:16:21)</sup>

- [x] **Add project script to pyproject.toml**
<sup>Commit [9a5974b](https://github.com/wmelvin/pomodorable/commit/9a5974b8f6989e11c918807027ec62e93ad58a66) (2024-03-07 11:44:53)</sup>

- [x] **Refactor AppConfig class to handle error cases when loading and saving**
<sup>Commit [476d675](https://github.com/wmelvin/pomodorable/commit/476d67533dd08d0d3ea98225690e9b40b6a35eb0) (2024-03-07 11:45:57)</sup>

- [x] **Reorg tests. New test for UI minus 5 button fails**
<sup>Commit [11ee07e](https://github.com/wmelvin/pomodorable/commit/11ee07e72e377801407a983ae912f890caa9f08f) (2024-03-07 14:47:36)</sup>

- [x] **Fix countdown finish condition**
<sup>Commit [335ae1b](https://github.com/wmelvin/pomodorable/commit/335ae1be3646a76f8dbf55a792ce068947328968) (2024-03-07 14:48:44)</sup>

---

- [x] **Refactor AppData initialization and data path handling**
<sup>Commit [8a5aff2](https://github.com/wmelvin/pomodorable/commit/8a5aff22b0e136377d50b6361e1d486aa8c2cf4e) (2024-03-08 10:17:41)</sup>

- [x] **Add test_app_data.py**
<sup>Commit [233c8d3](https://github.com/wmelvin/pomodorable/commit/233c8d3d73ec4eca3d428ed6a999c1458b5a6a29) (2024-03-08 10:19:06)</sup>

- [x] **Add method to retrieve latest session rows from CSV file**
<sup>Commit [b28cba6](https://github.com/wmelvin/pomodorable/commit/b28cba61f3fc57a80b9ea1db7b3f4feb034762ba) (2024-03-08 14:56:39)</sup>

- [x] **Add a pytest fixture to create test app_data**
<sup>Commit [8615b76](https://github.com/wmelvin/pomodorable/commit/8615b764e0fa5e54dec6ea3cd8258c82884607b7) (2024-03-08 17:00:22)</sup>

pytest documentation - [How to parametrize fixtures and test functions](https://docs.pytest.org/en/stable/how-to/parametrize.html#pytest-mark-parametrize-parametrizing-test-functions)

- [x] **Add get_session_rows_for_date to AppData class with test**
<sup>Commit [ea2cd1a](https://github.com/wmelvin/pomodorable/commit/ea2cd1a93975bab36589b9770bcaa38a6312dce7) (2024-03-08 18:37:46)</sup>

---

- [x] **Add handling non-UI options in cli.py**
<sup>Commit [e876416](https://github.com/wmelvin/pomodorable/commit/e876416ad9b3c5ae66bee44936be3d0316dfdc02) (2024-03-09 18:52:21)</sup>

---

- [x] **Add test and implement write_session_to_daily_csv**
<sup>Commit [aa7dbd1](https://github.com/wmelvin/pomodorable/commit/aa7dbd105fe8fb054a2fe4fdf904cbac10779064) (2024-03-11 18:59:18)</sup>

- [x] **Add to README**
<sup>Commit [84847a3](https://github.com/wmelvin/pomodorable/commit/84847a373414670d4bc6672501b74e9d1e44d392) (2024-03-11 19:20:36)</sup>

---

- [x] **Move AppConfig to new app_config.py**
<sup>Commit [49a312b](https://github.com/wmelvin/pomodorable/commit/49a312b7b03d9bb67cbf0e52b67f7631bf8dd2e6) (2024-03-12 09:32:29)</sup>

- [x] **Move utility functions to new app_utils module**
<sup>Commit [b5a14f8](https://github.com/wmelvin/pomodorable/commit/b5a14f8f05c99a7120bb15a0f625cfa3439749fb) (2024-03-12 09:53:55)</sup>

---

```
Layout of daily CSV.

Data CSV
version,date,time,action,message,duration,notes

Output CSV

action
------  date, time,     num,    task,   message, notes
start   date, time, (blank),    task,   (blank), (blank)
pause   date, time, (blank), (blank),   "Pause", reason
stop    date, time, (blank), (blank),    "STOP", reason
finish  date, time, (blank), (blank),  "pause*", (blank)

Num column is to match the layout I have been using in my Pomodori.ods
spreadsheet. I may want to keep using that spreadsheet, but just copy
in the day's entries from the daily CSV. In that case I'd fill in
the number manually. Perhaps when exporting a whole day the app can
fill in num.

Message for Pause includes "extend" or "resume".
```

Pytest - [How to use fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html)

Pytest - [How to monkeypatch/mock modules and environments](https://docs.pytest.org/en/stable/how-to/monkeypatch.html#monkeypatching-environment-variables)


- [x] **Add tests for expected CSV fields**
<sup>Commit [39c74f9](https://github.com/wmelvin/pomodorable/commit/39c74f901cd87a67717909c949488bd4c8d86033) (2024-03-12 10:55:06)</sup>

- [x] **Refactor write_session_to_daily_csv method and extract write_to_daily_csv method**
<sup>Commit [7405ec6](https://github.com/wmelvin/pomodorable/commit/7405ec6a46ecad66fcf7cf2bf84c524c8ed6a423) (2024-03-12 11:03:58)</sup>

- [x] **Extract write_to_daily_csv to function in new module**
<sup>Commit [8ecfdff](https://github.com/wmelvin/pomodorable/commit/8ecfdff5c5b53bc9fed67fbe8c016e62b136d1da) (2024-03-12 11:56:31)</sup>

- [x] **Move pytest fixture to new conftest.py**
<sup>Commit [0a99310](https://github.com/wmelvin/pomodorable/commit/0a99310ceb2fb94ed1bb45a898f48df71d2f747b) (2024-03-12 12:03:16)</sup>

- [x] **Add export_daily_csv method and test**
<sup>Commit [5124eea](https://github.com/wmelvin/pomodorable/commit/5124eea00007f9d63121bd41fdaf6d7fa7e18de1) (2024-03-12 16:41:45)</sup>

- [x] **Refactor write_to_daily_csv function to include session numbering**
<sup>Commit [acbe21b](https://github.com/wmelvin/pomodorable/commit/acbe21b9175c0ce3bc84ffebaa3cb41b15293ca4) (2024-03-12 16:52:57)</sup>

- [x] **Add support for writing daily Markdown files**
<sup>Commit [e049493](https://github.com/wmelvin/pomodorable/commit/e049493f1e851436fc9ade68828cd42fe7876be1) (2024-03-12 21:48:53)</sup>

---

- [x] **Log exception in settings screen path validation**
<sup>Commit [794611b](https://github.com/wmelvin/pomodorable/commit/794611b066b511d1ad5d4ddd83774087b7852e7b) (2024-03-13 10:46:03)</sup>

- [x] **Refactor AppConfig class to remove ConfigData dataclass**
<sup>Commit [0e430fe](https://github.com/wmelvin/pomodorable/commit/0e430fecc04e7d4ed61cb5402091aadf48ca6de3) (2024-03-13 11:29:10)</sup>

- [x] **Add markdown output settings to AppConfig**
<sup>Commit [75457a2](https://github.com/wmelvin/pomodorable/commit/75457a2b738dec491dc57e6f1a1e133e337e7c02) (2024-03-13 11:55:58)</sup>

Textual - [Switch](https://textual.textualize.io/widgets/switch/)

- [x] **Add SettingSwitch widget and implement setting for daily markdown append**
<sup>Commit [c34e87a](https://github.com/wmelvin/pomodorable/commit/c34e87ac1bda591adbba622ac60b18727bc11ebe) (2024-03-13 13:28:15)</sup>

---

- [x] **Show any errors queued by the AppData class**
<sup>Commit [272f5ae](https://github.com/wmelvin/pomodorable/commit/272f5ae0045505e8e5f5695de5e7a65f2654cb0f) (2024-03-14 10:39:38)</sup>

---

[markdown-guide/_basic-syntax/horizontal-rules.md](https://github.com/mattcone/markdown-guide/blob/master/_basic-syntax/horizontal-rules.md)

- [x] **Implement inserting section into existing markdown file**
<sup>Commit [4a07ef4](https://github.com/wmelvin/pomodorable/commit/4a07ef47b0d3731861d8b9dd6406b9626d138651) (2024-03-15 11:24:54)</sup>

- [x] **Add session_minutes to AppConfig and SettingsScreen**
<sup>Commit [401b3de](https://github.com/wmelvin/pomodorable/commit/401b3dec9cb407c0c844a2bb889be62139605baf) (2024-03-15 18:26:17)</sup>

- [x] **Use temp AppData in test_ui.py**
<sup>Commit [7fb8745](https://github.com/wmelvin/pomodorable/commit/7fb8745cd71052cb410a21c977d85413ff338c7d) (2024-03-15 18:35:10)</sup>

---

- [x] **Modify markdown output and related tests**
<sup>Commit [3011e3a](https://github.com/wmelvin/pomodorable/commit/3011e3a6da75e8bbc419d1a6221512cbc3674936) (2024-03-16 14:16:15)</sup>

- [x] **Modify methods used to add and subtract countdown**
<sup>Commit [3e352bf](https://github.com/wmelvin/pomodorable/commit/3e352bf4a536b7193ddf61f76c333c76a64a738c) (2024-03-16 16:14:34)</sup>

---

Note: The VSCode terminal does not handle all the TCSS color styling, so run the app in a separate terminal to see results.

Textual - Devtools - [Live editing](https://textual.textualize.io/guide/devtools/#live-editing)

[Geometric Shapes (Unicode block) - Wikipedia](https://en.wikipedia.org/wiki/Geometric_Shapes_(Unicode_block))

- [x] **Add TimerBar widget and update CountdownDisplay**
<sup>Commit [3f62014](https://github.com/wmelvin/pomodorable/commit/3f62014cf9584ba43730ddc3d6157579cf576af6) (2024-03-16 18:59:05)</sup>

---

Textual - Blog - [Textual 0.11.0 adds a beautiful Markdown widget](https://textual.textualize.io/blog/2023/02/15/textual-0110-adds-a-beautiful-markdown-widget/)

> You can generate these SVG screenshots for your app with
  `textual run my_app.py --screenshot 5`
  which will export a screenshot after 5 seconds.

- [x] **Add pytest-textual-snapshot and initial test stub**
<sup>Commit [bb200b5](https://github.com/wmelvin/pomodorable/commit/bb200b578d5ad791881e6b9db6d29e6031334567) (2024-03-17 13:06:46)</sup>

- [x] **Modify styles and timerbar**
<sup>Commit [92f7f8e](https://github.com/wmelvin/pomodorable/commit/92f7f8ea4cd4c39af0bb75a4afde6653e98acc90) (2024-03-17 16:43:54)</sup>

- [x] **Add buttons for 1 minute increments**
<sup>Commit [7025cd9](https://github.com/wmelvin/pomodorable/commit/7025cd9903d15d7f886b93838a03d5496aafb500) (2024-03-17 21:37:19)</sup>

- [x] **Update test and add screenshot to README**
<sup>Commit [5a4244b](https://github.com/wmelvin/pomodorable/commit/5a4244b29e9229161d5979661da10f3c61d3d91c) (2024-03-17 22:18:02)</sup>

---

- [x] **Enable/disable and focus widgets on state changes**
<sup>Commit [ece3b67](https://github.com/wmelvin/pomodorable/commit/ece3b67016de133d7b09bfc3da1295ab30bf2fd5) (2024-03-18 09:48:06)</sup>

- [x] **Add text to log display and new README image**
<sup>Commit [a23b313](https://github.com/wmelvin/pomodorable/commit/a23b313ba25a4443b6168e2d91d6269ad4d984e7) (2024-03-18 15:04:57)</sup>

---

- [x] **Add to README, set test.matrix python versions, and modify UI keybindings**
<sup>Commit [81ae71e](https://github.com/wmelvin/pomodorable/commit/81ae71e359690f0bef59183edb8d500a0ceba8fc) (2024-03-19 21:52:14)</sup>

- [x] **Modify daily-CSV layout and add act-code/num column**
<sup>Commit [118b133](https://github.com/wmelvin/pomodorable/commit/118b13357cf45196afbf5a0aa3e443d32c5e0666) (2024-03-20 08:51:26)</sup>

- [x] **Write to daily files on Stop, update version**
<sup>Commit [64c0755](https://github.com/wmelvin/pomodorable/commit/64c07550d4371aae51ff7167cd5fe6a47afa36c1) (2024-03-20 08:53:17)</sup>

Click documentation - [Help parameter customization](https://click.palletsprojects.com/en/8.0.x/documentation/#help-parameter-customization)

- [x] **Configure Click to also accept '-h' for help**
<sup>Commit [c1b8601](https://github.com/wmelvin/pomodorable/commit/c1b8601a2e4c4af372b146a78f18bcb8e69d337c) (2024-03-20 10:00:04)</sup>

- [x] **Modify UI message display**
<sup>Commit [327e634](https://github.com/wmelvin/pomodorable/commit/327e63493b5c359593316f7e389b04409db65755) (2024-03-20 11:50:20)</sup>

- [x] **Apply formatting**
<sup>Commit [b926253](https://github.com/wmelvin/pomodorable/commit/b92625345a48571f88446009bcb0cfbdf3f8aff3) (2024-03-20 11:53:52)</sup>

---

- [x] **Modify settings screen to return message**
<sup>Commit [c395c5a](https://github.com/wmelvin/pomodorable/commit/c395c5af9a96c5e72442cb16693047eb29e846d2) (2024-03-21 12:03:40)</sup>

- [x] **Add UI tests including (skipped) snapshot tests**
<sup>Commit [17fb92e](https://github.com/wmelvin/pomodorable/commit/17fb92e6b2e90ea8f133bf028f68759f14d68ecf) (2024-03-21 12:07:24)</sup>

- [x] **Modify countdown-finished process**
<sup>Commit [da0f025](https://github.com/wmelvin/pomodorable/commit/da0f02521f763d5ccef2fb9f7c10b8a5c39bffbc) (2024-03-21 21:26:03)</sup>

---

- [x] **Move actions from update_countdown to watch_seconds**
<sup>Commit [75279bf](https://github.com/wmelvin/pomodorable/commit/75279bfb58287a3140e9196858a825711316cca5) (2024-03-22 15:32:08)</sup>

- [x] **Add MRUList class for Most Recently Used text inputs**
<sup>Commit [f5135fa](https://github.com/wmelvin/pomodorable/commit/f5135fa1ed9bb2156bd220341408dc9e5ef79e2c) (2024-03-22 15:57:39)</sup>

Textual - Screens - [Modal screens](https://textual.textualize.io/guide/screens/#modal-screens)

- [x] **Add MRUScreen and implement MRUList**
<sup>Commit [18e257c](https://github.com/wmelvin/pomodorable/commit/18e257ca5fb47b1c56a3d7de0669f3775e9fdf0f) (2024-03-22 22:12:32)</sup>

---

- [x] **Add max length check to MRUList test**
<sup>Commit [021d825](https://github.com/wmelvin/pomodorable/commit/021d82514838c267e6d02a23af7bad45e1b338e7) (2024-03-23 18:41:37)</sup>

---

- [x] **Change SettingsScreen layout**
<sup>Commit [3e9a3d3](https://github.com/wmelvin/pomodorable/commit/3e9a3d3e967dcf16ab7d825b2252c837c5641046) (2024-03-24 20:00:59)</sup>

---

*TimedRotatingFileHandler* is not working as expected (perhaps mis-configured). Change to dated log file names and handle purging.

- [x] **Modify log file purge in AppData class**
<sup>Commit [46dbd6b](https://github.com/wmelvin/pomodorable/commit/46dbd6b64039406a326df0f5f241b4fae7a000ad) (2024-03-25 16:38:46)</sup>

- [x] **Correct a comment**
<sup>Commit [4d9330e](https://github.com/wmelvin/pomodorable/commit/4d9330e1b58b615870d3e90b38246398d4dda443) (2024-03-25 16:47:37)</sup>

---

- [x] **Modify action_select_input to fix bug**
<sup>Commit [d8fb1f7](https://github.com/wmelvin/pomodorable/commit/d8fb1f7c02d79cb01cde43026a8ff674bb87f89e) (2024-03-26 20:32:13)</sup>

---

- [x] **Add export for daily markdown and support custom export path**
<sup>Commit [8f9f875](https://github.com/wmelvin/pomodorable/commit/8f9f87560d7af9d7cd9eeca2b1beee24db418fe7) (2024-03-27 17:02:04)</sup>

---

- [x] **Print info to stdout from CLI export methods**
<sup>Commit [9b86106](https://github.com/wmelvin/pomodorable/commit/9b861061331329e00ae453fd613ab34722a0af41) (2024-03-28 16:20:54)</sup>

---

Textual - Guide - [Command Palette](https://textual.textualize.io/guide/command_palette/)

Textual - Styles - [Text opacity](https://textual.textualize.io/styles/text_opacity/)

- [x] **Make header icon invisible instead of not displaying it**
<sup>Commit [259af2c](https://github.com/wmelvin/pomodorable/commit/259af2c3a0218f2dab6369893c1f147021bc28a1) (2024-03-30 19:36:09)</sup>

---

- [x] **Add initial devnotes.md**
<sup>Commit [87edd7d](https://github.com/wmelvin/pomodorable/commit/87edd7deb3b9308dad5fba7f79a3158ea1045c56) (2024-03-30 19:37:33)</sup>

---

- [x] **Add AboutScreen**
<sup>Commit [0a2a40c](https://github.com/wmelvin/pomodorable/commit/0a2a40ce957a8eed4925a20c00d465ab21f47ea1) (2024-04-08 19:32:34)</sup>

---

- [x] **Refactor some variable names and docstrings**
<sup>Commit [cab47d8](https://github.com/wmelvin/pomodorable/commit/cab47d8c8760be36ddee689f5bb19cc8ef5b3ca2) (2024-04-10 12:04:08)</sup>

Python - Library - [webbrowser](https://docs.python.org/3/library/webbrowser.html)

- [x] **Add GitHub button to AboutScreen and update styles**
<sup>Commit [f218955](https://github.com/wmelvin/pomodorable/commit/f2189551a057403804408548d6e16fe7356303c8) (2024-04-10 15:09:13)</sup>

Textual - Guide - [Composing with context managers](https://textual.textualize.io/guide/layout/#composing-with-context-managers)

Python - Data model - [Context managers](https://docs.python.org/3/reference/datamodel.html#context-managers)

- [x] **Refactor AboutScreen compose method using context managers**
<sup>Commit [175d0a4](https://github.com/wmelvin/pomodorable/commit/175d0a4a8480e8e92aafd9a8b0fffdb303ce4f0c) (2024-04-10 17:57:16)</sup>

---

- [x] **Update version to 0.1.dev16**
<sup>Commit [72c7e43](https://github.com/wmelvin/pomodorable/commit/72c7e4353008b291e588c02fce165763133f6b1b) (2024-04-11 14:10:31)</sup>

---

```
Bug:

Pause -> Extend results in finishing immediately if the elapsed pause
time exceeded the original finish time.

It appears the problem is the reactive self.seconds, in the
CountdownDisplay class, is changed more than once in the
update_countdown method. The first change happens before
self.seconds_added are actually added so at that time the
value is <= 0 when watch_seconds is called.

Used a local 'secs' variable to get the new value and assign it to
self.seconds once. That seemed to fix the problem.

This is fairly obvious in hindsight. A watcher will be called
every time a reactive member is modified. I guess I'm not used to
thinking about this kind of reactivity.
```

- [x] **Only set reactive self.seconds once in update_countdown**
<sup>Commit [7180aa5](https://github.com/wmelvin/pomodorable/commit/7180aa552d2f78ca9ec8452ac6775e938e85644b) (2024-04-12 22:47:55)</sup>

---

- [x] **Update version to 0.1.dev18 and minor code reformat**
<sup>Commit [c7f56bc](https://github.com/wmelvin/pomodorable/commit/c7f56bc7b43183583cc60137be6f08438352dbe3) (2024-04-13 09:34:53)</sup>

---

Segfault.

Happened at finish. Wrote to log and data CSV before failing.

Add logging.debug at points in finish.

Set environment variable `POMODORABLE_DEBUG=Y` (or `Yes` or `True` or `1`) for `logger.setLevel(logging.DEBUG)`.

- [x] **Add debug logging, seeking point of intermittent failure**
<sup>Commit [820ec68](https://github.com/wmelvin/pomodorable/commit/820ec68c22793b8fb8e7a51cf9f0709c9aa787cc) (2024-04-16 18:00:51)</sup>

- [x] **Fix logging configuration for debug mode**
<sup>Commit [af5de04](https://github.com/wmelvin/pomodorable/commit/af5de0429a50e52a6b55a46aa3f69a09d4156e37) (2024-04-16 22:15:13)</sup>

- [x] **Fix the bad fix for debug logging**
<sup>Commit [1b53924](https://github.com/wmelvin/pomodorable/commit/1b53924cd50a931246085f070d48edfc6f2b727e) (2024-04-16 23:15:59)</sup>

---

Added `timer_resume` parameter to the `countdown.reset` method so when it's called in `countdown_finished` it will leave the timer paused.

- [x] **Add timer_resume parameter to CountdownDisplay.reset**
<sup>Commit [bd91a51](https://github.com/wmelvin/pomodorable/commit/bd91a514e79729654b911a329736e3419c3588cd) (2024-04-17 15:35:06)</sup>

- [x] **Refactor to remove unnecessary local vars**
<sup>Commit [cb265f4](https://github.com/wmelvin/pomodorable/commit/cb265f461a9d028c787bff5f7b967dde33981bbc) (2024-04-17 15:59:46)</sup>

---

- [x] **Update version to 0.1.dev20 and add testmx command to Justfile**
<sup>Commit [aa2a14c](https://github.com/wmelvin/pomodorable/commit/aa2a14c0850bd7ea43e76bd2801a8b57c03af825) (2024-04-20 11:16:34)</sup>

---

Textual - API - [Timer](https://textual.textualize.io/api/timer/)

- [x] **Reset TimerBar and CountdownDisplay last-value attrs**
<sup>Commit [1e87e00](https://github.com/wmelvin/pomodorable/commit/1e87e004b283411a198a13b83fe1671a72a5572d) (2024-04-23 17:56:01)</sup>

- [x] **Modify CountdownDisplay and TimerBar to fix timing issue**
<sup>Commit [a5dde36](https://github.com/wmelvin/pomodorable/commit/a5dde36dd9f20f9fcf68ee9dc7c3c832b0e4b2f0) (2024-04-23 19:34:57)</sup>

---

Add the option for a *Running* CSV, in addition to the *Daily* CSV output file. As I have been using the app I don't always copy from the daily CSV on a daily cadence. It would be easier to catch up from a single CSV file. For some reason, I'm not totally happy with the term "running" to make it distinct from the "daily" file, but I guess it will do for now.

- [x] **Add running (multi-day) CSV output and refactor some names**
<sup>Commit [64061c0](https://github.com/wmelvin/pomodorable/commit/64061c01d8e4f4ae343de94128953e115df0bab7) (2024-05-03 17:41:00)</sup>

- [x] **Add running_csv_name to AppConfig**
<sup>Commit [2d47345](https://github.com/wmelvin/pomodorable/commit/2d47345b3d2c6a45dd86b3ecf8bfa99f5738ae46) (2024-05-03 19:30:16)</sup>

- [x] **Update settings screen to include new CSV options**
<sup>Commit [b09be2b](https://github.com/wmelvin/pomodorable/commit/b09be2bda4286629c3a29bb5b40b8118b0ec7d3e) (2024-05-03 21:39:29)</sup>

---

Add `--end-date` CLI option to export a date range.

- [x] **Implement date range CSV export**
<sup>Commit [fd97e67](https://github.com/wmelvin/pomodorable/commit/fd97e67450f2196ef03ea54036ec1f9e84aca10d) (2024-05-05 14:56:03)</sup>

- [x] **Add details about the UI to README**
<sup>Commit [10948e1](https://github.com/wmelvin/pomodorable/commit/10948e15446d152956dd9aead11f0b2550b21a75) (2024-05-05 15:34:18)</sup>

---

Switches for actions (events) to **filter** (exclude) from CSV output.

- Default is to include all events.
- Filter out those you don't want.

Fiters:

- F = exclude Finish
- P = exclude Pause (any Extend or Resume event)
- R = exclude Pause-no-Reason (Extend or Resume with no reason text)
- X = exclude Stop

CLI `--filter` option - apply to the current export.

No warning if `--filter` is used without an `--export*` option. It's a `NOP`. Same with invalid filter codes passed. They will just do nothing.

Store in configuration file as strings (example):

``` toml
    filter_csv = "FR"
    filter_md = "F"
```

Settings Screen:

- Custom settings widget
- Use a SelectionList widget with a row for each filter
- Read and write as string of filter codes

 Textual - [SelectionList](https://textual.textualize.io/widgets/selection_list/)

- [x] **Add filter options for CSV and Markdown output to AppConfig**
<sup>Commit [f64e4e2](https://github.com/wmelvin/pomodorable/commit/f64e4e20c40d19a882abd2d3f2e2f7ed03be600c) (2024-05-06 13:47:58)</sup>

- [x] **Add SettingOutputFilter widget for CSV output filtering**
<sup>Commit [96c3531](https://github.com/wmelvin/pomodorable/commit/96c3531e90a216956e0f0e0b7cab9c6c4dbb57f7) (2024-05-06 13:48:41)</sup>

- [x] **Implement filter_csv and add test**
<sup>Commit [66e9aef](https://github.com/wmelvin/pomodorable/commit/66e9aefc665e568805e1522e22d94ccd459f459d) (2024-05-06 16:13:59)</sup>

- [x] **Update README with timer image and note re input MRU list**
<sup>Commit [195d6f2](https://github.com/wmelvin/pomodorable/commit/195d6f2052cc0729d7fd91884f241d9b59ee8cea) (2024-05-06 16:43:03)</sup>

- [x] **Update CLI export functions to accept filters as command line argument**
<sup>Commit [c0acdbe](https://github.com/wmelvin/pomodorable/commit/c0acdbe75ead1421671506b622b436aacba3327c) (2024-05-06 19:26:15)</sup>

---

Python - [faulthandler](https://docs.python.org/3/library/faulthandler.html)

- [x] **Add faulthandler, build for debugging, then comment out**
<sup>Commit [9efb5be](https://github.com/wmelvin/pomodorable/commit/9efb5be9e55eafb39272a3cf893585952c795a57) (2024-05-07 08:42:49)</sup>

- [x] **Implement date range export and filters for Markdown output**
<sup>Commit [417afd6](https://github.com/wmelvin/pomodorable/commit/417afd62a73f9f4209536d845de8ca094be65128) (2024-05-07 09:27:45)</sup>

- [x] **Add filters for Markdown output to Settings screen**
<sup>Commit [a50dacb](https://github.com/wmelvin/pomodorable/commit/a50dacb1f722eed3c3e2ea814d64a920e5618c79) (2024-05-07 10:35:23)</sup>

- [x] **Update README with links to images and more UI details**
<sup>Commit [29722a5](https://github.com/wmelvin/pomodorable/commit/29722a56708762fc623d7942dd7d5892d7c3eed2) (2024-05-07 11:16:32)</sup>

- [x] **Update version to 0.1.dev24**
<sup>Commit [05c60dc](https://github.com/wmelvin/pomodorable/commit/05c60dc6cfa2d14edd16a2e16ced93392aafc3fa) (2024-05-07 11:19:52)</sup>

---

- [x] **Bump version number and enable faulthandler for debugging**
<sup>Commit [3a51605](https://github.com/wmelvin/pomodorable/commit/3a516053fcedf941a6303cb1b0e1946df3293086) (2024-05-08 17:08:17)</sup>

- [x] **Add info about screens and files to README**
<sup>Commit [2f29050](https://github.com/wmelvin/pomodorable/commit/2f290504b66f3290aabe4714423111fd41463653) (2024-05-08 17:10:09)</sup>

- [x] **Remove seconds from time in Markdown outputs**
<sup>Commit [d3d1574](https://github.com/wmelvin/pomodorable/commit/d3d1574c3082bc70e5e1fce484bafe42b8300689) (2024-05-08 17:21:20)</sup>

---

- [x] **Add more info to README**
<sup>Commit [109c578](https://github.com/wmelvin/pomodorable/commit/109c57840679b8f2ffb6c633ac5bc7410067c6ac) (2024-05-09 11:28:13)</sup>

- [x] **Edit README**
<sup>Commit [6a65a72](https://github.com/wmelvin/pomodorable/commit/6a65a72950e03ac58690877079b9042bc9713396) (2024-05-09 11:44:08)</sup>

- [x] **Bump version number to 0.1.dev26**
<sup>Commit [9036722](https://github.com/wmelvin/pomodorable/commit/903672227380c50644cf9573d25a9144129686de) (2024-05-09 11:59:55)</sup>

- [x] **Minor edits to README**
<sup>Commit [fb4cbf5](https://github.com/wmelvin/pomodorable/commit/fb4cbf59f0597ed151add59e2fd5d1092d0434d6) (2024-05-09 15:45:25)</sup>

---

Manual testing on a Windows 11 VM (Azure).
Crash loading MRU list.

``` python
    mru_list.py line 28
    if row[0] == "task":
          ^^^
    list index out of range
```

I forgot about this detail when using the `csv` module (from [CSV File Reading and Writing](https://docs.python.org/3/library/csv.html)):

> "If csvfile is a file object, it should be opened with `newline=''`."

There were also some exceptions caught and logged due to the button events in the About screen flowing back to the UI app.

Added `event.stop()` in the AboutScreen.on_button_pressed method so those events do not flow back to the parent app.

- [x] **Fix problems with CSV files and events in AboutScreen**
<sup>Commit [0cabd24](https://github.com/wmelvin/pomodorable/commit/0cabd24c19fefa12efcbcc9dbced2b5c55a58791) (2024-05-10 15:52:45)</sup>

---

Add GitHub Actions workflow to run tests on push.

Install VS-Code extension [github/vscode-github-actions](https://github.com/github/vscode-github-actions).

[push - Events that trigger workflows](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#push)

[Manually running a workflow](https://docs.github.com/en/actions/using-workflows/manually-running-a-workflow)

Also added manual workflows to run test on Windows and Mac. Both ran and passed when launched from GitHub in web browser.

- [x] **Add GitHub Actions workflow for running tests**
<sup>Commit [ccbc4b3](https://github.com/wmelvin/pomodorable/commit/ccbc4b38e64097a7f67923ea631c3d6ce74172b3) (2024-05-11 12:54:13)</sup>

- [x] **Update setup-python action and try hatch test matrix**
<sup>Commit [be1e6ed](https://github.com/wmelvin/pomodorable/commit/be1e6edcafccc3fd4e5c6ae3fca570008af90ce6) (2024-05-11 13:08:11)</sup>

- [x] **Add manual trigger workflows for tests on Mac and Windows**
<sup>Commit [0a197bf](https://github.com/wmelvin/pomodorable/commit/0a197bff3039b6289f22bf74a5b78f69bb1e4e14) (2024-05-11 13:40:42)</sup>

- [x] **Bump version number to 0.1.dev28**
<sup>Commit [b28f911](https://github.com/wmelvin/pomodorable/commit/b28f911f0a1c724127990828893f2543e206523d) (2024-05-11 15:15:11)</sup>

---

Textual - API - App - [save_screenshot](https://textual.textualize.io/api/app/#textual.app.App.save_screenshot)

- [x] **Add actions and key bindings to take screenshots**
<sup>Commit [4cac6ba](https://github.com/wmelvin/pomodorable/commit/4cac6ba6c84ed82be9aa480ad3dcc7620a4707e7) (2024-05-19 11:01:01)</sup>

---

- [x] **Update keywords in pyproject.toml and bump version to 0.1.dev30**
<sup>Commit [0d73823](https://github.com/wmelvin/pomodorable/commit/0d73823b0616f7cc213578201462ed150efe8b4d) (2024-05-20 16:01:13)</sup>

---

- [x] **Add --ctrl-s arg to CLI to enable screenshots**
<sup>Commit [af48a1a](https://github.com/wmelvin/pomodorable/commit/af48a1a2e810be7999ddf04e72a985e55c4053a1) (2024-05-24 10:18:46)</sup>

---

Real Python - [Playing and Recording Sound in Python](https://realpython.com/playing-and-recording-sound-python/)

- [x] **Add setting and capacity to play a sound file at end of session**
<sup>Commit [47638f5](https://github.com/wmelvin/pomodorable/commit/47638f52b6aa62ff37ba2d265cad44bead1bcc14) (2024-05-25 08:36:54)</sup>

- [x] **Add setting to enable notification and option for test-key**
<sup>Commit [2babb04](https://github.com/wmelvin/pomodorable/commit/2babb04347ee76b0c8050d07c54d4e72866dcee6) (2024-05-25 11:20:00)</sup>

---

- [x] **Add descriptions of new settings to README**
<sup>Commit [c61a5c8](https://github.com/wmelvin/pomodorable/commit/c61a5c8b884f41fa34d53a7d879b3af452444e22) (2024-05-28 22:22:17)</sup>

---

Hatch was upgraded. Running `hatch fmt` produced warnings, including the following:

> warning: The top-level linter settings are deprecated in favour of their counterparts in the `lint` section. Please update the following options in `pyproject.toml`:
>  - 'extend-per-file-ignores' -> 'lint.extend-per-file-ignores'

Per Hatch documentation on [Persistent config](https://hatch.pypa.io/latest/config/internal/static-analysis/#persistent-config), ran this command:

`hatch fmt --check --sync`

That updates `ruff_defaults.toml` to match the new Hatch defaults.

Changed `line-length = 120` (the Hatch setting) back to `line-length = 88`.
IMO: The `black` line length of 79 seems too short, but 120 seems too long.


- [x] **Update Hatch linter ruff_defaults**
<sup>Commit [45d396e](https://github.com/wmelvin/pomodorable/commit/45d396ed229254a49489b9750ee9dd852640e113) (2024-05-29 15:34:27)</sup>

---

Ran the test matrix using `just testmx` and Python 3.12.3 failed at installing dependencies. The problem is in `setup.py` in the `playsound` package (which seems to be languishing).

Try using [playsound3](https://pypi.org/project/playsound3/).

[sjmikler/playsound3](https://github.com/sjmikler/playsound3): Cross platform library to play sound files in Python.

Replaced `playsound` with `playsound3` in pyproject.toml.

- [x] **Switch to playsound3 and add tests and wav files**
<sup>Commit [c2b0e96](https://github.com/wmelvin/pomodorable/commit/c2b0e963bc5fadfe97faef442fb0452a63f2e133) (2024-05-29 15:35:53)</sup>

- [x] **Actions: Install ffmpeg for playsound tests**
<sup>Commit [1c69889](https://github.com/wmelvin/pomodorable/commit/1c6988906d36cd4ad5f9ca424ebe86ca64ebebc2) (2024-05-29 15:50:45)</sup>

---

- [x] **Add new image and links to README**
<sup>Commit [131d785](https://github.com/wmelvin/pomodorable/commit/131d78572321428a432874a46429424f8c58bb74) (2024-06-03 12:21:02)</sup>

- [x] **Link to raw image on GitHub so it will appear on PyPI page**
<sup>Commit [ec4d556](https://github.com/wmelvin/pomodorable/commit/ec4d556ddd286fc91ae30144f93163ad91ac8a5f) (2024-06-03 12:26:38)</sup>

---

- [x] **Update version to 0.1**
<sup>Commit [905be5d](https://github.com/wmelvin/pomodorable/commit/905be5db50de7a9faba6c46de3b1e2507901c33d) (2024-06-03 14:00:42)</sup>

---

- [x] **Add link for Pomodoro Technique near top of README**
<sup>Commit [5866174](https://github.com/wmelvin/pomodorable/commit/58661741fbff2c829c489b6ee1d95cd82392a246) (2024-06-04 10:41:49)</sup>

---

- [x] **Expand devnotes.md**
<sup>Commit [0f34646](https://github.com/wmelvin/pomodorable/commit/0f34646d1265358de8f2e48e09a05bbc6a03219b) (2024-06-14 18:19:51)</sup>

---

Tests failed on GitHub yesterday evening when only changes to `devnotes.md` were commited.

Run tests locally.

`just test`
    
All passed. Try getting latest env.

``` bash
hatch env prune
pipx upgrade hatch
```
    
"hatch is already at latest version 1.12.0"
    
`just test`

Test `test_minus_button_stops_at_one` failed.

Debug in VS-Code. If I *debug* the test, it passes. If I *run* the test it fails. Race condition?

Try changing Textual version.

Most recent all tests passing on GitHub was 2024-06-04. Textual was probably at `0.64.0`.

Set in `pyproject.toml`: `textual==0.64.0`. 

``` bash
hatch env prune
just test
```

Tests pass.

Incrementally updated release version. Test started **hanging** at `textual==0.65.2` (had to `Ctrl+c`). Test started failing at `textual==0.67.0`.

- [x] **Pin textual version to check GH action test failed**
<sup>Commit [e9a90a4](https://github.com/wmelvin/pomodorable/commit/e9a90a44e59b5fce5760ff59dbdaf477feb27eb3) (2024-06-15 10:26:22)</sup>

---

Try using pip-compile (in pip-tools) to create a pinned requirements.txt.

[pip-tools](https://pip-tools.readthedocs.io/en/stable/#requirements-from-requirements-in)

There is a plugin for Hatch to use requirements.txt.

[Metadata hook plugins - Hatch](https://hatch.pypa.io/latest/plugins/metadata-hook/reference/)

[repo-helper/hatch-requirements-txt](https://github.com/repo-helper/hatch-requirements-txt): Hatchling plugin to read project dependencies from requirements.txt

- [x] **Use pip-tools to pin dependencies**
<sup>Commit [5423f46](https://github.com/wmelvin/pomodorable/commit/5423f46c5b8b3394d693d80c0888677c060fd09a) (2024-06-15 17:54:47)</sup>

---

- [x] **Add pip-compile to Justfile and update version number**
<sup>Commit [23ac3a0](https://github.com/wmelvin/pomodorable/commit/23ac3a06c4744cc3e40db43919d37e369cb9332b) (2024-06-19 19:21:43)</sup>

---
