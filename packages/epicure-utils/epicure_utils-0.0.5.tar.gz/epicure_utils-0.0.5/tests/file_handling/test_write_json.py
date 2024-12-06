import json
import os

import pytest

from epicure.file_handling.json import write_json


@pytest.fixture
def test_data():
    """Sample test data fixture."""
    return {"name": "test", "value": 42}


@pytest.fixture
def large_data():
    """Large test data fixture."""
    return {str(i): f"value_{i}" for i in range(1000)}


def test_write_json_success(tmp_path, test_data):
    """Test successful JSON file writing."""
    file_path = tmp_path / "test.json"
    assert write_json(str(file_path), test_data) is True

    with open(file_path, "r") as f:
        written_data = json.load(f)
    assert written_data == test_data


def test_write_empty_json(tmp_path):
    """Test writing empty dictionary."""
    file_path = tmp_path / "empty.json"
    assert write_json(str(file_path), {}) is True

    with open(file_path, "r") as f:
        written_data = json.load(f)
    assert written_data == {}


def test_write_json_directory_not_found():
    """Test writing to non-existent directory."""
    with pytest.raises(FileNotFoundError) as error:
        write_json("nonexistent/dir/test.json", {"test": "data"})
    assert "Directory not found" in str(error.value)


def test_write_json_permission_error(tmp_path, test_data):
    """Test writing with no permissions."""
    file_path = tmp_path / "test.json"
    file_path.touch()
    os.chmod(file_path, 0o444)  # Read-only

    try:
        with pytest.raises(PermissionError) as error:
            write_json(str(file_path), test_data)
        assert "Permission denied" in str(error.value)
    finally:
        os.chmod(file_path, 0o666)  # Restore permissions


def test_write_json_is_directory_error(tmp_path):
    """Test writing to a directory path."""
    with pytest.raises(IsADirectoryError) as error:
        write_json(str(tmp_path), {"test": "data"})
    assert "Is a directory" in str(error.value)


def test_write_json_special_characters(tmp_path):
    """Test writing JSON with special characters."""
    special_data = {"special": "!@#$%^&*()_+-=[]{}|;:,./<>?"}
    file_path = tmp_path / "special.json"

    assert write_json(str(file_path), special_data) is True

    with open(file_path, "r") as f:
        written_data = json.load(f)
    assert written_data == special_data


def test_write_large_json(tmp_path, large_data):
    """Test writing large JSON data."""
    file_path = tmp_path / "large.json"

    assert write_json(str(file_path), large_data) is True

    with open(file_path, "r") as f:
        written_data = json.load(f)
    assert written_data == large_data


def test_write_json_indent(tmp_path, test_data):
    """Test JSON is written with proper indentation."""
    file_path = tmp_path / "indent.json"

    assert write_json(str(file_path), test_data) is True

    with open(file_path, "r") as f:
        content = f.read()
    assert "    " in content  # Check for 4-space indentation


def test_write_json_file_overwrite(tmp_path, test_data):
    """Test overwriting existing JSON file."""
    file_path = tmp_path / "test.json"

    # Write initial data
    write_json(str(file_path), {"initial": "data"})

    # Overwrite with new data
    assert write_json(str(file_path), test_data) is True

    with open(file_path, "r") as f:
        written_data = json.load(f)
    assert written_data == test_data
