import os 

def rename_file(file_path: str, new_file_name: str) -> str:
    """
    Rename provided file to new
    """
    if not isinstance(file_path, str) or not file_path:
        raise ValueError("Original file path must be a non-empty string.")
    if not isinstance(new_file_name, str) or not new_file_name:
        raise ValueError("New file name must be a non-empty string.")

    try: 
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"The file at '{file_path}' was not found.")

        current_directory = os.path.dirname(file_path)
        new_path = os.path.join(current_directory, new_file_name)

        os.rename(file_path, new_path)

        return new_file_name
    except FileNotFoundError:
        raise FileNotFoundError(f"File: The file at '{file_path}' not found.")
    except FileExistsError:
        raise FileExistsError(f"A file with the name '{new_file_name}' already exists in the target directory.")
    except Exception as e:
        raise Exception(f"Error occured while renaming file at '{file_path}': {e}.")