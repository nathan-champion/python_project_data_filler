from sys import argv
from pathlib import Path
from sys import exit

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


def sanitize_directory_name(dir_name):
    sanitized = "".join([c for c in dir_name if c.isalnum() or c == ' ']).rstrip()
    return sanitized


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


def get_alphanumeric_input(prompt):
    approved = False
    while not approved:
        tested = input(prompt).strip() 
        approved = tested.isalnum()

    return tested


def get_name(prompt):
    approved = False
    while not approved:
        tested = input(prompt).strip()
        approved = all(c.isalpha() or c.isspace() for c in tested)

    return tested


def get_email(prompt):
    approved = False
    while not approved:
        tested = input(prompt).strip()
        try:
            approved = tested.index('@') != -1
        except:
            pass

    return tested


def gather_replacements(replacements):   
    replacements["$PACKAGE_NAME"] = get_alphanumeric_input("Enter package name:")
    replacements["$MY_NAME"] = get_name("Enter your real name:")
    replacements["$MY_EMAIL"] = get_email("Enter your email address:")
    replacements["$MODULE_NAME"] = get_alphanumeric_input("Enter your starting module name:")


def create_directories(root_dir, source_dir):
    make_path_or_die(root_dir)
    make_path_or_die(source_dir)
    make_path_or_die(root_dir / "tests")


def make_path_or_die(path):
    try:
        Path.mkdir(path, parents=True)
    except:
        print(f"Directory {path} already exists!  Exiting!")
        exit()


def create_files(root_dir, source_dir, blueprint:str, replacements:dict):
    global package_dir
    
    filled_blueprint = blueprint[:]
    for key, value in replacements.items():
        filled_blueprint = filled_blueprint.replace(key, value)
    
    file = open(root_dir / "pyproject.toml", 'x')
    file.write(filled_blueprint)
    file.close()

    make_empty_file(root_dir, "LICENSE")
    make_empty_file(root_dir, "README.md")

    module_path = source_dir
    module_file_name = "{}.py".format(replacements["$MODULE_NAME"])

    make_empty_file(module_path, "__init__.py")
    make_empty_file(module_path, module_file_name)


def make_empty_file(file_path, file_name):
    file = open(file_path / file_name, 'x') 
    file.close()



def run():
    try:
        project_path = sanitize_directory_name(argv[1])
        print(f"We've sanitized the string if necessary.  Your directory is {project_path}.")
    except:
        print(usage)
        exit()

    gather_replacements(replacements)

    root_directory = Path.cwd() / project_path
    source_directory = root_directory / replacements["$PACKAGE_NAME"]
    print(f"This will create your project at {root_directory}. Is this where you want it?")
    decision = get_defined_input("Y", "n")
    
    if decision == "Y":
        create_directories(root_directory, source_directory)
        create_files(root_directory, source_directory, toml_blueprint, replacements)


if __name__ == '__main__':
    run()