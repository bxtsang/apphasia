import unittest
from application import create_folders, search_all_folders

class TestCreateFolder (unittest.TestCase):
    def test_create_folder(self):
        # test that folder has been created
        folders = ["documents", "edms", "certificates"]

        for folder in create_folders(folders):
            self.assertIn(folder, search_all_folders())
            