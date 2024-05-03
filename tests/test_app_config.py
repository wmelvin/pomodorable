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
    config_to_save = AppConfig(config_file)
    app_data = AppData(config_to_save)
    app_data.set_daily_csv_dir("/path/to/csv")
    app_data.set_running_csv_dir("/path/to/csv2")
    app_data.set_running_csv_name("running.csv")
    app_data.set_daily_md_dir("/path/to/md")
    config_to_save.daily_md_heading = "# Daily Markdown"
    config_to_save.daily_md_append = True
    config_to_save.log_retention_days = 7
    config_to_save.save()

    config_loaded = AppConfig(config_file)
    config_loaded.load()
    assert config_loaded.daily_csv_dir == "/path/to/csv"
    assert config_loaded.running_csv_dir == "/path/to/csv2"
    assert config_loaded.daily_md_dir == "/path/to/md"
    assert config_loaded.daily_md_heading == "# Daily Markdown"
    assert config_loaded.daily_md_append is True
    assert config_loaded.log_retention_days == 7
    assert config_loaded.running_csv_name == "running.csv"
