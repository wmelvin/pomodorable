import csv
import logging
from pathlib import Path

MRU_LIST_MAX = 20


class MRUList:
    """Most Recently Used List for tasks and reasons"""

    def __init__(self, data_path: Path) -> None:
        self.data_path = data_path
        self._mru_task = []
        self._mru_reason = []
        self._csv_file = data_path / "mru_lists.csv"

    # CSV file format: List,Text
    # Where:
    #   'List is the list name: 'task' or 'reason'
    #   'Text is from the respective input field'

    def load(self) -> None:
        if self._csv_file.exists():
            try:
                with self._csv_file.open(newline="") as file:
                    reader = csv.reader(file)
                    for row in reader:
                        if not row:
                            continue
                        if row[0] == "task":
                            self._mru_task.append(row[1])
                        elif row[0] == "reason":
                            self._mru_reason.append(row[1])
            except Exception:
                logging.exception("Error loading MRU list.")

    def save(self) -> None:
        with self._csv_file.open("w", newline="") as file:
            writer = csv.writer(file, quoting=csv.QUOTE_ALL)
            for item in self._mru_task:
                writer.writerow(["task", item])
            for item in self._mru_reason:
                writer.writerow(["reason", item])

    def add_task(self, task: str) -> None:
        if not task:
            return
        if task in self._mru_task:
            self._mru_task.remove(task)
        self._mru_task.insert(0, task)
        if len(self._mru_task) > MRU_LIST_MAX:
            self._mru_task = self._mru_task[:MRU_LIST_MAX]

    def add_reason(self, reason: str) -> None:
        if not reason:
            return
        if reason in self._mru_reason:
            self._mru_reason.remove(reason)
        self._mru_reason.insert(0, reason)
        if len(self._mru_reason) > MRU_LIST_MAX:
            self._mru_reason = self._mru_reason[:MRU_LIST_MAX]

    def get_tasks(self) -> str:
        return list(self._mru_task)

    def get_reasons(self) -> str:
        return list(self._mru_reason)
