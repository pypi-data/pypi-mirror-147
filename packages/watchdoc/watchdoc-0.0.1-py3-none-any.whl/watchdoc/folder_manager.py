import os
import sys
from uuid import uuid4
import json
import fnmatch
import re
import time
from urllib.parse import quote

# Function for checking if the directory
# containes file or not

username = str(input("Github username: "))
repository = str(input("Github repository: "))


def dir_has_markdown_files(dir_path):
    dir_file_list = [os.path.join(dir_path, f) for f in os.listdir(
        dir_path) if os.path.isfile(os.path.join(dir_path, f))]
    return os.path.exists(dir_path) and len(os.listdir(dir_path)) > 0 and ".md" in dir_file_list


def path_to_dict(root_path: str, language: str) -> dict:

    includes = ['*.md']  # for files only
    excludes = ['.git', '.vscode', '.git', '*/__pycache__', '*/.ipynb_checkpoints', 'venv', 'pyvenv', 'tempvenv',
                'Books', 'Codes', 'Presentations', 'Temp']  # for dirs and files

    # transforms glob patterns to regular expressions
    includes = r'|'.join([fnmatch.translate(x) for x in includes])
    excludes = r'|'.join([fnmatch.translate(x) for x in excludes]) or r'$.'

    for root, dirs, files in os.walk(root_path, topdown=True):

        # exclude dirs
        dirs[:] = [os.path.join(root, d) for d in dirs]
        dirs[:] = [d for d in dirs if not re.match(
            excludes, d) and not dir_has_markdown_files(d)]

        # exclude/include files
        files = [os.path.join(root, f) for f in files]
        files = [f for f in files if not re.match(excludes, f)]
        files = [f for f in files if re.match(includes, f)]

        tree = {
            "name": os.path.basename(root),
            "id": str(uuid4()),
            "child": []
        }

        tree["child"].extend(
            [path_to_dict(os.path.join(root, d), language)
             for d in dirs if len(d) > 0]
        )

        tree["child"].extend(
            [{
                "name": os.path.basename(os.path.join(root, f)),
                "id": str(uuid4()),
                "icon": '''<img src={`/icons/${getIconForFile('index.md')}`} alt="markdown" className="icon" />''',
                "link": str(
                    "https://raw.githubusercontent.com/" + username +
                    "/" + repository + "/main/" + "Notebooks" + "/"
                    + language + "/" +
                    quote(os.path.basename(root)) +
                    "/" + quote(os.path.basename(f))
                ),
            } for f in files]
        )

        tree = {k: v for k, v in tree.items() if v}

        return tree


def path_to_json_string(file_path: str, language: str) -> str:
    return dict_to_json_string(path_to_dict(file_path, language))


def dict_to_json_string(dict_data: dict):
    return json.dumps(dict_data, default=lambda o: o.__dict__, sort_keys=False, indent=4)


def dict_to_json_file(dict_data):
    json_str = dict_to_json_string(dict_data)
    json_file = open("data.json", "w+")
    json_file.write(json_str)
    json_file.close()
    return os.path.abspath(json_file)


def notebook_file_paths(folder_path: str, file_type: str) -> list:
    paths = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(file_type.lower()):
                paths.append(os.path.join(root, file))

    return paths


if __name__ == "__main__":

    cwd = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()

    start = time.time()    # for testing purposes
    english = cwd + os.path.sep + "Notebooks" + os.path.sep + "English"
    dutch = cwd + os.path.sep + "Notebooks" + os.path.sep + "Nederlands"

    englishTree = path_to_dict(english, "English")
    dutchTree = path_to_dict(dutch, "Nederlands")

    pythonTutorials = [englishTree, dutchTree]
    dict_to_json_file(pythonTutorials)

    end = time.time()

    print("Conversion took " + str(round(end - start, 2)) + " milliseconds.")
