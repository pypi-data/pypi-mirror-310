import json


def read_json(file_path: str) -> dict:
    """
    Read a JSON file and return its content as a dictionary.

    :param file_path: The path to the JSON file.
    :type file_path: str
    :return: The content of the JSON file as a dictionary.
    :rtype: dict

    :raises: FileNotFoundError: If the file is not found.
    :raises: PermissionError: If read permission is denied.
    :raises: IsADirectoryError: If file_path is a directory.
    :raises: JSONDecodeError: If the file is not a valid JSON file.

    :examples:
        >>> users = read_json("users.json")
        >>> users
        {
            "users": [
                {
                    "id": 1,
                    "name": "John Doe",
                    "email": "
                },
                {
                    "id": 2,
                    "name": "Jane Doe",
                    "email": "
                }
            ]
        }

        >>> read_json("invalid/path/to/file/users.json")
        FileNotFoundError: [Errno 2]
        No such file or directory: 'invalid/path/to/file/users.json'
    """
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except PermissionError:
        raise PermissionError(f"Permission denied: {file_path}")
    except IsADirectoryError:
        raise IsADirectoryError(f"Is a directory: {file_path}")
    except json.JSONDecodeError as error:
        raise json.JSONDecodeError(
            f"Invalid JSON file: {file_path}", error.doc, error.pos
        )


def write_json(file_path: str, data: dict) -> None:
    """
    Write a dictionary to a JSON file.

    :param file_path: The path to the JSON file.
    :type file_path: str
    :param data: The dictionary to write to the file.
    :type data: dict
    :return: True if the file was written successfully.
    :rtype: bool

    :raises: FileNotFoundError: If the directory doesn't exist
    :raises: PermissionError: If write permission is denied
    :raises: IsADirectoryError: If file_path is a directory

    :examples:
        >>> users = {
        ...     "users": [
        ...         {
        ...             "id": 1,
        ...             "name": "John Doe",
        ...             "email": "
        ...         },
        ...         {
        ...             "id": 2,
        ...             "name": "Jane Doe",
        ...             "email": "
        ...         }
        ...     ]
        ... }
        >>> write_json("users.json", users)
        # The content of the file "users.json" will be:
        {
            "users": [
                {
                    "id": 1,
                    "name": "John Doe",
                    "email": "
                },
                {
                    "id": 2,
                    "name": "Jane Doe",
                    "email": "
                }
            ]
        }

        >>> write_json("invalid/path/to/file/users.json", users)
        FileNotFoundError: [Errno 2]
        No such file or directory: 'invalid/path/to/file/users.json'
    """
    try:
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
            return True
    except FileNotFoundError:
        raise FileNotFoundError(f"Directory not found: {file_path}")
    except PermissionError:
        raise PermissionError(f"Permission denied: {file_path}")
    except IsADirectoryError:
        raise IsADirectoryError(f"Is a directory: {file_path}")
