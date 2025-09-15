import os 

def delete_file(file_path: str) -> None:
    """
    Delete provided file 
    """
    if not isinstance(file_path, str) or not file_path:
        raise ValueError("File path must be a non-empty string.")

    try:
        os.remove(file_path)
        return None

    except FileNotFoundError as e:
        raise FileNotFoundError(f"Error: The file at '{file_path}' was not found")
    except Exception as e:
        raise Exception(f"Error occured while deleting the file: {e}")