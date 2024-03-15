import logging
from pathlib import Path

from tomlkit import document, dumps, parse

LOG_RETENTION_DEFAULT = 30
LOG_RETENTION_MIN = 5
SESSION_MINUTES_DEFAULT = 25

KEY_SESSION_MINUTES = "session_minutes"
KEY_DAILY_CSV_DIR = "daily_csv_dir"
KEY_DAILY_MD_DIR = "daily_md_dir"
KEY_DAILY_MD_HEADING = "daily_md_heading"
KEY_DAILY_MD_APPEND = "daily_md_append"
KEY_LOG_RETENTION_DAYS = "log_retention_days"


class AppConfig:
    def __init__(self, config_file: Path) -> None:
        self.config_file = config_file
        self.session_minutes: int = SESSION_MINUTES_DEFAULT
        self.daily_csv_dir: str = ""
        self.daily_md_dir: str = ""
        self.daily_md_heading: str = ""
        self.daily_md_append: bool = False
        self.log_retention_days: int = LOG_RETENTION_DEFAULT

    def _load_toml_doc(self) -> document:
        """Load the TOML document from the configuration file. If the file
        doesn't exist or there is an error parsing it, return an empty
        document. If there is an error parsing the file, rename it with a
        '.bad' extension before returning the empty document.
        """
        if self.config_file.exists():
            try:
                text = self.config_file.read_text()
                return parse(text)
            except Exception:
                logging.exception("Error parsing configuration.")
                bad_file = self.config_file.with_suffix(".bad")
                logging.info("Rename bad file to '%s'", bad_file)
                if bad_file.exists():
                    bad_file.unlink()
                self.config_file.rename(bad_file)
                return document()
        return document()

    def _fix_daily_md_heading(self):
        """If the daily markdown heading has a value, it needs to start with
        a '#' character. It can be configured as a heading at any level, but
        it will default to a top-level heading.
        """
        if not self.daily_md_heading:
            return
        if not self.daily_md_heading.startswith("#"):
            self.daily_md_heading = f"# {self.daily_md_heading}"

    def load(self) -> None:
        if self.config_file.exists():
            logging.info("Load '%s'", self.config_file)
            try:
                doc = self._load_toml_doc()
                self.session_minutes = doc.get(
                    KEY_SESSION_MINUTES, SESSION_MINUTES_DEFAULT
                )
                self.daily_csv_dir = doc.get(KEY_DAILY_CSV_DIR, "")
                self.daily_md_dir = doc.get(KEY_DAILY_MD_DIR, "")
                self.daily_md_heading = doc.get(KEY_DAILY_MD_HEADING, "")
                self.daily_md_append = doc.get(KEY_DAILY_MD_APPEND, False)
                self.log_retention_days = doc.get(
                    KEY_LOG_RETENTION_DAYS, LOG_RETENTION_DEFAULT
                )
                self._fix_daily_md_heading()
            except Exception:
                logging.exception("Error loading configuration.")
        else:
            # Save initial config.
            self.save()

    def save(self) -> None:
        logging.info("Save '%s'", self.config_file)
        try:
            if self.config_file.exists():
                logging.info("Save to existing file")
                doc = self._load_toml_doc()
            else:
                logging.info("Save to new file")
                doc = document()
            doc[KEY_SESSION_MINUTES] = self.session_minutes
            doc[KEY_DAILY_CSV_DIR] = self.daily_csv_dir
            doc[KEY_DAILY_MD_DIR] = self.daily_md_dir
            doc[KEY_DAILY_MD_HEADING] = self.daily_md_heading
            doc[KEY_DAILY_MD_APPEND] = self.daily_md_append
            doc[KEY_LOG_RETENTION_DAYS] = self.log_retention_days
            text = dumps(doc)
            self.config_file.write_text(text)
        except Exception:
            logging.exception("Error saving configuration.")

    @property
    def session_seconds(self) -> int:
        return self.session_minutes * 60
