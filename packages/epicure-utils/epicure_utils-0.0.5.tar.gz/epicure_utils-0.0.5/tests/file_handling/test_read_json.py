import json
import os

import pytest

from epicure.file_handling.json import read_json


@pytest.fixture
def valid_json_file(tmp_path):
    """Create a temporary valid JSON file."""
    content = {"name": "test", "value": 42}
    file_path = tmp_path / "valid.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(content, f)
    return str(file_path)


@pytest.fixture
def empty_json_file(tmp_path):
    """Create a temporary empty JSON file."""
    file_path = tmp_path / "empty.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump({}, f)
    return str(file_path)


@pytest.fixture
def invalid_json_file(tmp_path):
    """Create a temporary invalid JSON file."""
    file_path = tmp_path / "invalid.json"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("{invalid:json")
    return str(file_path)


def test_read_valid_json(valid_json_file):
    """Test reading a valid JSON file."""
    result = read_json(valid_json_file)
    assert result == {"name": "test", "value": 42}


def test_read_empty_json(empty_json_file):
    """Test reading an empty JSON file."""
    result = read_json(empty_json_file)
    assert result == {}


def test_file_not_found():
    """Test handling of non-existent file."""
    with pytest.raises(FileNotFoundError) as error:
        read_json("nonexistent.json")
    assert "File not found" in str(error.value)


def test_permission_error(valid_json_file):
    """Test handling of permission error."""
    os.chmod(valid_json_file, 0o000)
    try:
        with pytest.raises(PermissionError) as error:
            read_json(valid_json_file)
        assert "Permission denied" in str(error.value)
    finally:
        os.chmod(valid_json_file, 0o666)


def test_is_directory_error(tmp_path):
    """Test handling when path is a directory."""
    with pytest.raises(IsADirectoryError) as error:
        read_json(str(tmp_path))
    assert "Is a directory" in str(error.value)


def test_invalid_json_error(invalid_json_file):
    """Test handling of invalid JSON content."""
    with pytest.raises(json.JSONDecodeError) as error:
        read_json(invalid_json_file)
    assert "Invalid JSON file" in str(error.value)


def test_special_characters(tmp_path):
    """Test handling of special characters in JSON."""
    content = {"special": "!@#$%^&*()_+-=[]{}|;:,./<>?"}
    file_path = tmp_path / "special.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(content, f)
    result = read_json(str(file_path))
    assert result == content


def test_large_json(tmp_path):
    """Test handling of large JSON file."""
    content = {str(i): f"value_{i}" for i in range(1000)}
    file_path = tmp_path / "large.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(content, f)
    result = read_json(str(file_path))
    assert result == content


def test_special_chars_in_content(tmp_path):
    """Test reading JSON with special characters."""
    special_data = {"special": "!@#$%^&*()_+-=[]{}|;:,.<>?"}
    file_path = tmp_path / "special.json"
    with open(file_path, "w") as f:
        json.dump(special_data, f)

    result = read_json(str(file_path))
    assert result == special_data
