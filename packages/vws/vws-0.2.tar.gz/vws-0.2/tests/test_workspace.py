# tests/test_workspace.py

import unittest
from vws.workspace import Workspace, Directory, File

class TestVirtualWorkspace(unittest.TestCase):

    def setUp(self):
        """Set up a new workspace for testing."""
        self.workspace = Workspace("Test Workspace")
        self.workspace.create_directory("Documents")
        self.workspace.create_file("test_file.txt", "This is a test file.")

    def test_create_file(self):
        """Test creating a file in the workspace."""
        self.workspace.create_file("another_file.txt", "Another test file content.")
        file_content = self.workspace.read_file_content("another_file.txt")
        self.assertEqual(file_content, "Another test file content.")

    def test_create_directory(self):
        """Test creating a directory in the workspace."""
        self.workspace.create_directory("Images")
        directory_contents = self.workspace.list_contents()
        self.assertIn("Images", directory_contents)

    def test_list_contents(self):
        """Test listing contents of the root directory."""
        contents = self.workspace.list_contents()
        self.assertIn("test_file.txt", contents)
        self.assertIn("Documents", contents)

    def test_read_file_content(self):
        """Test reading the content of a file."""
        content = self.workspace.read_file_content("test_file.txt")
        self.assertEqual(content, "This is a test file.")

    def test_list_directory_contents(self):
        """Test listing contents of a specific directory."""
        self.workspace.create_file("doc_file.docx", "Document content.")
        contents = self.workspace.list_directory_contents("Documents")
        self.assertIn("doc_file.docx", contents)

    def test_file_not_found(self):
        """Test handling of a file not found in the workspace."""
        content = self.workspace.read_file_content("non_existing_file.txt")
        self.assertEqual(content, "File 'non_existing_file.txt' not found in the root directory.")

    def test_directory_not_found(self):
        """Test handling of a directory not found in the workspace."""
        contents = self.workspace.list_directory_contents("NonExistingDir")
        self.assertEqual(contents, "Directory 'NonExistingDir' not found.")

if __name__ == '__main__':
    unittest.main()
    # make sure doing this once its installed if wanted