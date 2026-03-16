import pytest
import os
from tools.file_tools import list_files, read_file, write_file
from memory.long_term import LongTermMemory
from tools.task_tools import TaskTools

def test_file_tools(tmp_path):
    d = tmp_path / "test_dir"
    d.mkdir()
    f = d / "test.txt"
    
    # Test write_file
    res = write_file(str(f), "hello world")
    assert "Successfully" in res
    
    # Test read_file
    content = read_file(str(f))
    assert content == "hello world"
    
    # Test list_files
    files = list_files(str(d))
    assert "test.txt" in files

def test_task_tools(tmp_path):
    db_file = tmp_path / "test.db"
    mem = LongTermMemory(db_path=str(db_file))
    tools = TaskTools(mem)
    
    # Test add_task
    res = tools.add_task("Clean room")
    assert "ID: 1" in res
    
    # Test list_tasks
    tasks = tools.list_tasks()
    assert "Clean room" in tasks
    
    # Test complete_task
    res = tools.complete_task(1)
    assert "marked as completed" in res
    
    tasks = tools.list_tasks(status="completed")
    assert "Clean room" in tasks
