from pomodorable.app_config import AppConfig
from pomodorable.app_data import AppData


def test_app_config_load_creates_new_file(tmp_path):
    config_file = tmp_path / "pomodorable-config.toml"
    app_config = AppConfig(config_file)
    app_config.load()
    assert config_file.exists()


def test_app_config_load_reads_file(tmp_path):
    config_file = tmp_path / "pomodorable-config.toml"
    config_file.write_text(
        "daily_csv_dir = '/path/to/csv'\n" "daily_md_dir = '/path/to/md'\n"
    )
    app_config = AppConfig(config_file)
    app_config.load()
    assert app_config.daily_csv_dir == "/path/to/csv"
    assert app_config.daily_md_dir == "/path/to/md"


def test_app_config_save_load(tmp_path):
    config_file = tmp_path / "pomodorable-config.toml"
    app_config = AppConfig(config_file)
    app_data = AppData(app_config)
    app_data.set_daily_csv_dir("/path/to/csv")
    app_data.set_daily_md_dir("/path/to/md")
    app_config.daily_md_heading = "# Daily Markdown"
    app_config.daily_md_append = True
    app_config.log_retention_days = 7
    app_config.save()
    app_config.load()
    assert app_config.daily_csv_dir == "/path/to/csv"
    assert app_config.daily_md_dir == "/path/to/md"
    assert app_config.daily_md_heading == "# Daily Markdown"
    assert app_config.daily_md_append is True
    assert app_config.log_retention_days == 7
