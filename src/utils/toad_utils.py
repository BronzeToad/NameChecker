import subprocess

from pathlib import Path


# =============================================================================================== #

def find_project_root(project_name: str, test_mode: bool = False) -> Path:
    cwd = Path.cwd()
    while cwd.name.lower() != project_name.lower():
        if cwd == cwd.parent:
            raise NotADirectoryError(f"Could not find project root for project: {project_name}")
        cwd = cwd.parent
    return cwd / 'tests' if test_mode else cwd


def get_git_tracked_files(root_path: Path) -> list:
    result = subprocess.run(['git', 'ls-files'], cwd=root_path, stdout=subprocess.PIPE)
    return result.stdout.decode('utf-8').splitlines()

def generate_structured_lines(root_path: Path, tracked_files: list) -> list:
    processed_dirs = set()
    structure_lines = []
    for file in tracked_files:
        parts = Path(file).parts
        current_path = root_path
        for i, part in enumerate(parts):
            current_path = current_path / part
            if i == len(parts) - 1:
                structure_lines.append(str(current_path))
            else:
                if current_path not in processed_dirs:
                    structure_lines.append(str(current_path))
                    processed_dirs.add(current_path)
    return sorted(structure_lines, key=lambda s: s.lower())

def format_structured_str(root_path: Path, structure_lines: list) -> str:
    structure_str = ""
    for line in structure_lines:
        line_path = Path(line)
        relative_path = line_path.relative_to(root_path)
        depth = len(relative_path.parts) - 1
        indent_str = '|   ' * depth
        name = line_path.name
        if line_path.is_dir():
            structure_str += f"{indent_str}|-- {name}/\n"
        else:
            structure_str += f"{indent_str}|-- {name}\n"
    return structure_str

def get_project_structure(project_name: str, output_filename: str = 'project_structure.txt'):
    root_path = find_project_root(project_name)
    tracked_files = get_git_tracked_files(root_path)
    structure_lines = generate_structured_lines(root_path, tracked_files)
    structure_str = format_structured_str(root_path, structure_lines)
    print(f"Generating structure for Git-tracked files in project at path: {root_path}")
    with open(root_path / output_filename, 'w') as file:
        file.write(structure_str)
    print(f"Project structure written to: {output_filename}")


# =============================================================================================== #

if __name__ == "__main__":
    get_project_structure('NameChecker')
