import os 
from typing import List

def search_files(query: str, directory: str) -> List[str]:
    """
    Allow query on provided directory and returns the result
    """

    if not os.path.isdir(directory):
        raise ValueError(f"Provided directory '{directory}' is not valid")
    
    matching_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if query in file:
               matching_files.append(os.path.join(root, file))
        
    return matching_files
