from __future__ import annotations

from datetime import datetime


def sec_to_hms(seconds: int) -> str:
    """Convert seconds to a string in the form "HH:MM:SS" or "MM:SS" if less
    than an hour.
    """
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if hours > 0:
        return f"{hours:02}:{minutes:02}:{seconds:02}"
    return f"{minutes:02}:{seconds:02}"


def get_date_from_str(date_str: str) -> datetime | None:
    """Return a date (as datetime) from a string.
    The string may come from user input and should allow for several
    formats, including:
      "YYYY-MM-DD"
      "YY-MM-DD"
    If the string does not match any of the formats, return None.
    """
    date_formats = ["%Y-%m-%d", "%y-%m-%d"]
    for date_format in date_formats:
        try:
            return datetime.strptime(date_str, date_format)  # noqa: DTZ007
        except ValueError:
            pass
    return None


def q_text(text: str) -> str:
    """Return the text, preceded by a space and surrounded by single quotes,
    or an empty string if the text is empty.
    """
    s = text.strip()
    if s:
        return f" '{s}'"
    return ""


def str_true(s: str) -> bool:
    """Return True if the string represents a 'true' value.

    The following are considered 'true' (case-insensitive):
    '1', 'true', 'y', 'yes'.

    Otherwise return False.
    """
    return s.lower() in ["1", "true", "y", "yes"]
