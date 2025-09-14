def read_file(file_path: str) -> str:
    """
    Read content from provided file path
    """

    if not isinstance(file_path, str) or not file_path:
        raise ValueError("File path must be a non-empty string.")
    
    if file_path.endswith(".exe"):
        raise ValueError("Files with '.exe' extensions are not allowed to read")

    try:
        # for safety
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    except FileNotFoundError as e:
        raise FileNotFoundError(f"Error: The file at '{file_path}' was not found")
    except Exception as e:
        raise Exception(f"Error occured while reading the file: {e}")
        