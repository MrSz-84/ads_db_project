import os


def find(path: str) -> str:
    """
    Main function calling other in this module. The module purpose is to scan given directory via
    other scripts.

    :param path: Path to a folder which is going to be searched for files, represented as a string.
    :raise OSError: If given path isn't a directory.
    :return: Path to the file which is the newest according to ctime parameter.
    :rtype: str
    """

    files_in_dir = create_elements_list(path)
    latest_radio_file = return_newest_path(files_in_dir)
    return latest_radio_file


def create_elements_list(path: str) -> list[dict]:
    """
    Creates the list containing every file in given directory. Files are represented as dicts,
    containing numerous elements. Those elements are:
    1. name -> name of the file
    2. timestamp -> timestamp taken by os.getctime()
    3. path -> path to the file according to os.path()
    4. is_dir -> True for directories, False for files. Using os.isdir()
    5. is_file -> Contrary to point number 4. Using os.isfile()
    6. newest -> placeholder for setting a flag for the newest file in given directory

    :param path: Path to a folder which is going to be searched for files, represented as a string.
    :raise OSError: If given path isn't a directory.
    :return: List of dicts containing information as stated above about every file in given
    directory
    :rtype: list[dict]
    """
    
    scanned = os.scandir(path=path)
    keys = ['name', 'timestamp', 'path', 'is_dir', 'is_file', 'newest']
    files = []
    for item in scanned:
        map_values = {
            'name': lambda: item.name,
            'timestamp': lambda: os.path.getctime(item.path),
            'path': lambda: item.path,
            'is_dir': lambda: item.is_dir(),
            'is_file': lambda: item.is_file(),
            'newest': lambda: item.is_symlink()
        }
        files.append({key: method() for key, method in zip(keys, map_values.values())})
    newest = get_newest(files)[0]
    files[newest['idx']]['newest'] = True
    return files


def get_newest(lst: list[dict]) -> list[dict]:
    """
    Creates the list containing every .xlsx file in given directory. Binds index based on entry
    object, and dicts containing complete information about distinct files.

    :param lst: List containing information about files present inside scanned directory
    :raise KeyError: If somehow keys don't match used nomenclature
    :return: New sorted list of dicts for separate files being the representation of files present
    in the directory
    :rtype: list[dict]
    """

    enumerated = []
    for idx, item in list(enumerate(lst)):
        if item['name'].endswith('.xlsx') and ('TV' in item['name'] or 'Radio' in item['name']):
            enumerated.append({'idx': idx, "item": item})
    return sorted(enumerated, key=lambda x: x['item']['timestamp'], reverse=True)


def return_newest_path(lst: list[dict]) -> str:
    """
    Loops over every item, and returns the one flagged as the newest.

    :param lst: List containing information about files present inside scanned directory
    :raise KeyError: If somehow keys don't match used nomenclature
    :return: path to the newest file in given directory
    :rtype: str
    """

    for item in lst:
        if item['newest']:
            return item['path']
