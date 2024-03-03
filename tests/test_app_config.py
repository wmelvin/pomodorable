from pomodorable.app_data import AppConfig


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
