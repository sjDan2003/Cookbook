import unittest
from unittest.mock import patch
import sys
import os.path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from GoogleDrive import GoogleDriveClass

class GoogleDriveTestClass(unittest.TestCase):

    # The constructor of GoogleDriveClass gets the credentials of the user.
    # Since we don't want to do this in test, we'll mock this out.
    @patch('GoogleDrive.GoogleDriveClass.__init__', unittest.mock.Mock(return_value=None))
    def setUp(self):

        self.googleDrive = GoogleDriveClass()
        self.dummyFileName = '/home/sjdan2003/Cookbook/data/savedRecipes.json'


    def test_GetFileName(self):

        testFileName = self.googleDrive.GetFileName(self.dummyFileName)
        expectedFileName = 'savedRecipes.json'
        self.assertEqual(testFileName, expectedFileName, 'File names do not match')

        noFileNamePath = '/home/sjdan2003/Cookbook/data/'
        testFileName = self.googleDrive.GetFileName(noFileNamePath)
        expectedFileName = None
        self.assertEqual(testFileName, expectedFileName, 'File names do not match for no file name')


    def test_GetFileType(self):

        testFileType = self.googleDrive.GetFileType(self.dummyFileName)
        expectedFileType = '.json'
        self.assertEqual(testFileType, expectedFileType, 'File types do not match')

        noFileTypePath = '/home/sjdan2003/Cookbook/data/savedRecipes'
        testFileType = self.googleDrive.GetFileType(noFileTypePath)
        expectedFileType = None
        self.assertEqual(testFileType, expectedFileType, 'File types do not match for no file type')


    def test_ListFiles(self):

        pass


if __name__ == "__main__":
    unittest.main()