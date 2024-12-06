from pathlib import Path


def ask_overwrite_if_exists(file_path: Path) -> bool:
    if file_path.is_file():
        message = f"{file_path} is already exists, overwrite it? (y/n): "
        overwrite = input(message).lower() == "y"
    else:
        overwrite = True

    return overwrite
