import os

def create_file(filename: str, content: str) -> None:
    """
    Creates file with provided arguments: [1]filename, [2]content
    """
    try:
        if filename is None:
            print(f"No file name provided")
            return
        if not check_exe(filename):
            return
        current_directory = os.getcwd()
        abs_path = os.path.join(current_directory, filename)
        if not os.path.isfile(abs_path):
            with open(abs_path, "w", encoding="utf-8") as file:
                file.write(content)
        else:
            print(f"File name already exists: {filename} with directory: {abs_path}")
            return
        
        print(f"New file created with name: {filename}")
        return None
    except OSError as e:
        raise OSError(f"Error ocurred while creating the file: {e}")

def check_exe(filename: str) -> bool:
    """
    Check whether filename has '.exe' extension. Returns true or false depends on provided filename.
    """
    if filename.endswith(".exe"):
        print("Files with .exe are not allowed") 
        return False
    elif not filename.endswith(".exe"):
        return True