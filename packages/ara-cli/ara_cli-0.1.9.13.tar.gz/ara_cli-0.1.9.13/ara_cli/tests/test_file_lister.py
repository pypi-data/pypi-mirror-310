import os
import tempfile
import shutil
import pytest
from unittest.mock import MagicMock, patch
from ara_cli.file_lister import generate_markdown_listing, list_files_in_directory

@pytest.fixture
def setup_test_environment():
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()

    # Create nested directories and files
    os.makedirs(os.path.join(temp_dir, 'dir1'))
    os.makedirs(os.path.join(temp_dir, 'dir2', 'subdir1'))

    # Create files
    open(os.path.join(temp_dir, 'file1.py'), 'a').close()
    open(os.path.join(temp_dir, 'file2.txt'), 'a').close()
    open(os.path.join(temp_dir, 'dir1', 'file3.py'), 'a').close()
    open(os.path.join(temp_dir, 'dir2', 'file4.py'), 'a').close()
    open(os.path.join(temp_dir, 'dir2', 'subdir1', 'file5.py'), 'a').close()

    yield temp_dir

    # Cleanup
    shutil.rmtree(temp_dir)


def test_generate_markdown_listing_multiple_directories(setup_test_environment):
    temp_dir = setup_test_environment
    another_temp_dir = tempfile.mkdtemp()

    try:
        os.makedirs(os.path.join(another_temp_dir, 'dir3'))
        open(os.path.join(another_temp_dir, 'file6.py'), 'a').close()

        output_file_path = os.path.join(temp_dir, "output_multiple_dirs.md")

        expected_content = [
            f"# {os.path.basename(temp_dir)}",
            " - [] file1.py",
            "## dir1",
            "     - [] file3.py",
            "## dir2",
            "     - [] file4.py",
            "### subdir1",
            "         - [] file5.py",
            f"# {os.path.basename(another_temp_dir)}",
            " - [] file6.py",
            "## dir3"
        ]

        generate_markdown_listing([temp_dir, another_temp_dir], ['*.py'], output_file_path)

        with open(output_file_path, 'r') as f:
            output_content = f.read().splitlines()

        assert output_content == expected_content

    finally:
        shutil.rmtree(another_temp_dir)


@pytest.mark.parametrize("directory, files_in_directory", [
    ("test_dir", ["file1.txt", "file2.py"]),
    ("single_file_dir", ["single_file.md"]),
])
def test_list_files_in_directory(directory, files_in_directory, capsys):
    with patch('os.scandir') as mock_scandir:
        mock_entries = []
        for file_name in files_in_directory:
            mock_entry = MagicMock()
            mock_entry.is_file.return_value = True
            mock_entry.name = file_name
            mock_entries.append(mock_entry)

        mock_scandir.return_value.__enter__.return_value = mock_entries

        list_files_in_directory(directory)

        captured = capsys.readouterr()

        expected_output = "\n".join(f"- {directory}/{file_name}" for file_name in files_in_directory) + "\n"

        assert captured.out == expected_output


def test_list_files_in_directory_empty_dir(capsys):
    with patch('os.scandir') as mock_scandir:
        mock_scandir.return_value.__enter__.return_value = []

        list_files_in_directory("empty_dir")

        captured = capsys.readouterr()

        assert captured.out == ""
