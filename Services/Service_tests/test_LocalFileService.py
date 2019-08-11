import unittest
from unittest.mock import patch, mock_open
from Services import LocalFileServiceClass


class LocalFileServiceTestClass(unittest.TestCase):

    def setUp(self):

        self.local_file_service = LocalFileServiceClass()
        self.testFileName = '/Cookbook/data/savedRecipes.json'

    def test_read_json_file(self):

        with patch('builtins.open', new_callable=mock_open()) as mockedOpen:
            with patch('LocalFileService.json.load') as mockedJsonLoad:

                testJsonData = {'Test Key': 'Test Value'}
                mockedJsonLoad.return_value = testJsonData
                retJsonData = self.local_file_service.read_json_file(self.testFileName)
                mockedOpen.assert_called_once_with(self.testFileName)
                self.assertEqual(retJsonData, testJsonData, 'Mocked data mismatch')

    def test_read_json_file_FileNotFound(self):

        with patch('builtins.open', new_callable=mock_open()) as mockedOpen:

            testJsonData = {}
            mockedOpen.side_effect = FileNotFoundError()
            retJsonData = self.local_file_service.read_json_file(self.testFileName)
            mockedOpen.assert_called_once_with(self.testFileName)
            self.assertEqual(retJsonData, testJsonData, 'Read Json Exception should return no data')

    def test_write_json_file(self):

        with patch('LocalFileService.os.makedirs') as mockedMakeDirs:
            with patch('builtins.open', new_callable=mock_open()) as mockedOpen:
                testJsonData = {'Test Key': 'Test Value'}
                self.local_file_service.write_json_file(self.testFileName, testJsonData)
                mockedOpen.assert_called_once_with(self.testFileName, 'w+')

    def test_get_filename(self):

        testFileName = self.local_file_service.get_filename(self.testFileName)
        expectedFileName = 'savedRecipes.json'
        self.assertEqual(testFileName, expectedFileName, 'File names do not match')

    def test_GetFileName_NoFilename(self):

        noFileNamePath = '/home/sjdan2003/Cookbook/data/'
        retFileName = self.local_file_service.get_filename(noFileNamePath)
        expectedFileName = None
        self.assertEqual(retFileName, expectedFileName, 'File names do not match for no file name')

    def test_get_file_type(self):

        testFileType = self.local_file_service.get_file_type(self.testFileName)
        expectedFileType = '.json'
        self.assertEqual(testFileType, expectedFileType, 'File types do not match')

    def test_GetFilieType_NoFilename(self):

        noFileTypePath = '/home/sjdan2003/Cookbook/data/savedRecipes'
        retFileName = self.local_file_service.get_file_type(noFileTypePath)
        expectedFileType = None
        self.assertEqual(retFileName, expectedFileType, 'File types do not match for no file type')