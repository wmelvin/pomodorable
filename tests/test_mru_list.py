from pathlib import Path

from pomodorable.mru_list import MRUList


def test_mru_list(tmp_path: Path):
    mru_list1 = MRUList(tmp_path)
    mru_list1.add_task("task1")
    mru_list1.add_task("task2")
    mru_list1.add_task("task3")
    mru_list1.add_task("")
    mru_list1.add_task(None)
    mru_list1.add_reason("reason1")
    mru_list1.add_reason("reason2")
    mru_list1.add_reason("reason3")
    mru_list1.add_reason("")
    mru_list1.add_reason(None)
    mru_list1.add_reason("reason1")
    mru_list1.save()

    mru_list2 = MRUList(tmp_path)
    mru_list2.load()
    assert mru_list2.get_tasks() == ["task3", "task2", "task1"]
    assert mru_list2.get_reasons() == ["reason1", "reason3", "reason2"]
