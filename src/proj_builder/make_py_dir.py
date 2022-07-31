from operator import index
from sys import argv
from pathlib import Path
from sys import exit
import os

usage = """
Using this tool requires the command line arguments below:
1. A root directory name for your project

"""


toml_blueprint = """
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "$PACKAGE_NAME"
version = "$VERSION_MAJOR.$VERSION_MINOR.$VERSION_REVISION"
authors = [
    { name="$MY_NAME", email="$MY_EMAIL" },
]
description = "$DESCRIPTION"
readme = "README.md"
license = { file="LICENSE" }
requires-python = ">=$REQ_PYTHON_VER"
classifiers = [
    
]

[project.urls]
"Homepage" = "$PROJECT_HOMEPAGE"
"Bug Tracker" = "$PROJECT_BUGS_PAGE"
"""

replacements = {
    "$PACKAGE_NAME": "",
    "$USER_NAME": "",
    "$VERSION_MAJOR": "0",
    "$VERSION_MINOR": "1",
    "$VERSION_REVISION": "0",
    "$MY_NAME": "",
    "$MY_EMAIL": "",
    "$REQ_PYTHON_VER": "$REQ_PYTHON_VER",
    "$PROJECT_HOMEPAGE": "$PROJECT_HOMEPAGE",
    "$PROJECT_BUGS_PAGE": "$PROJECT_BUGS_PAGE",
}

package_dir = ""


def get_defined_input(*choices):
    prompt = "/".join(choices) + ":"
    
    approved_choice = False
    while not approved_choice:
        selection = input(prompt)
    
        try:
            choices.index(selection)
            approved_choice = True
        except:
            print(f"{selection} is not an available option from prompt.")

    return selection


def gather_data(replacements):
    
    replacements["$PACKAGE_NAME"] = input("Enter package name:").strip()
    replacements["$USER_NAME"] = input("Enter your user name:").strip()
    replacements["$MY_NAME"] = input("Enter your real name:").strip()
    replacements["$MY_EMAIL"] = input("Enter your email address:").strip()
    replacements["$MODULE_NAME"] = input("Enter your starting module name:").strip()


def create_directories(root_dir):
    global package_dir

    try:
        Path.mkdir(root_dir)
    except:
        print(f"Directory {root_dir} already exists!  Please try again and choose a new name for your directory!")
        exit()
    
    package_dir = "{}_{}".format(replacements["$PACKAGE_NAME"], replacements["$USER_NAME"])
    Path.mkdir(root_dir / "src" / package_dir, parents=True)
    Path.mkdir(root_dir / "tests")


def create_files(root_dir, blueprint:str, replacements:dict):
    global package_dir
    
    filled_blueprint = blueprint[:]
    for key, value in replacements.items():
        filled_blueprint = filled_blueprint.replace(key, value)
    
    file = open(root_dir / "pyproject.toml", 'x')
    file.write(filled_blueprint)
    file.close()

    make_empty_file(root_dir, "LICENSE")
    make_empty_file(root_dir, "README.md")

    module_path = root_dir / "src" / package_dir
    module_file_name = "{}.py".format(replacements["$MODULE_NAME"])

    make_empty_file(module_path, "__init__.py")
    make_empty_file(module_path, module_file_name)


def make_empty_file(file_path, file_name):
    file = open(file_path / file_name, 'x') 
    file.close()


def run():
    try:
        project_path = argv[1]
    except:
        print(usage)
        exit()

    gather_data(replacements)

    root_directory = Path.cwd() / project_path
    print(f"This will create your project at {root_directory}. Is this where you want it?")
    decision = get_defined_input("Y", "n")
    
    if decision == "Y":
        create_directories(root_directory)
        create_files(root_directory, toml_blueprint, replacements)


if __name__ == '__main__':
    run()