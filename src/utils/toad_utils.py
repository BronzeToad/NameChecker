import subprocess
import os
from pathlib import Path

def get_git_project_structure(root_path, output_filename):
    """
    Write the project structure from the root path to a txt file, 
    only including files and directories tracked by Git (i.e., not .gitignored).
    
    Parameters:
    - root_path (str): The root directory of the project.
    - output_filename (str): The name of the output file.
    """
    
    # Get the list of files tracked by Git
    result = subprocess.run(['git', 'ls-files'], cwd=root_path, stdout=subprocess.PIPE)
    tracked_files = result.stdout.decode('utf-8').splitlines()

    # Create a set to hold the directories we've already processed
    processed_dirs = set()
    
    structure_lines = []
    
    for file in tracked_files:
        parts = file.split('/')
        current_path = root_path
        for i, part in enumerate(parts):
            current_path = os.path.join(current_path, part)
            if i == len(parts) - 1:
                # It's a file
                structure_lines.append(current_path)
            else:
                # It's a directory
                if current_path not in processed_dirs:
                    structure_lines.append(current_path)
                    processed_dirs.add(current_path)

    # Now, we'll format the structure
    structure_str = ""
    for line in sorted(structure_lines, key=lambda s: s.lower()):
        relative_path = os.path.relpath(line, root_path)
        depth = relative_path.count(os.sep)
        indent_str = '|   ' * depth
        name = os.path.basename(line)
        if os.path.isdir(line):
            structure_str += f"{indent_str}|-- {name}/\n"
        else:
            structure_str += f"{indent_str}|-- {name}\n"
    
    print(f"Generating structure for Git-tracked files in project at path: {root_path}")
    # Write the structure to the specified output file
    with open(output_filename, 'w') as file:
        file.write(structure_str)
    
    print(f"Project structure written to: {output_filename}")

def find_project_root(project_name: str, tests: bool = False) -> Path:
    cwd = Path.cwd()
    while cwd.name.lower() != project_name.lower():
        if cwd == cwd.parent:
            raise NotADirectoryError(f"Could not find project root for project: {project_name}")
        cwd = cwd.parent
    return cwd / 'tests' if tests else cwd


if __name__ == "__main__":
    # get_git_project_structure(
    #     root_path='/Users/ajp/Documents/Projects/NameChecker', 
    #     output_filename='project_structure.txt')

    print(find_project_root('namechecker', tests=True))