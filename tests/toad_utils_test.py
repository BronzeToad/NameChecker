import pytest


@pytest.fixture
def tracked_files(toad_utils, project_root):
    return toad_utils.get_git_tracked_files(project_root)

@pytest.fixture
def structured_lines(toad_utils, project_root, tracked_files):
    return toad_utils.generate_structured_lines(project_root, tracked_files)


def test_find_project_root(toad_utils):
    project_name = 'NameChecker'
    project_root = toad_utils.find_project_root(project_name)
    assert project_root.name == project_name

def test_find_invalid_project_root(toad_utils):
    with pytest.raises(NotADirectoryError):
        toad_utils.find_project_root('BadProjectName')

def test_get_git_tracked_files(toad_utils, project_root):
    tracked_files = toad_utils.get_git_tracked_files(project_root)
    assert len(tracked_files) > 0

def test_generate_structured_lines(toad_utils, project_root, tracked_files):
    structured_lines = toad_utils.generate_structured_lines(project_root, tracked_files)
    assert len(structured_lines) > 0

def test_format_structured_str(toad_utils, project_root, structured_lines):
    structured_str = toad_utils.format_structured_str(project_root, structured_lines)
    assert len(structured_str) > 0

def test_get_project_structure(toad_utils, project_root):
    toad_utils.get_project_structure(project_root.name, 'test_project_structure.txt')
    assert (project_root / 'test_project_structure.txt').exists()
    (project_root / 'test_project_structure.txt').unlink()
