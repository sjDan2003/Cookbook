import json
import os


class LocalFileServiceClass:

    def WriteJsonFile(self, filename, jsonData):
        """Function responsible for writting JSON or Dictionary formatted data
        to a JSON file somewhere on local storage

        Args:
            filename: The full file path and filename where
            the data should to be saved
            jsonData: Dictionary formatted data to be saved

        Returns:
            None
        """

        # Make sure the folder(s) exist before trying to save the file
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        with open(filename, 'w+') as writeFilePtr:
            json.dump(jsonData, writeFilePtr)

    def ReadJsonFile(self, filename):
        """Reads JSON formatted data into a dictionary object

        Args:
            filename: The full file path and file name of the data to be read

        Returns:
            A dictionary object of the file's contents
        """

        returnJsonData = {}
        try:
            with open(filename) as readFilePtr:
                returnJsonData = json.load(readFilePtr)
        except FileNotFoundError as fileError:
            print('File not found')

        return returnJsonData

    def GetFileName(self, filePath):
        """Gets the file name of the file being uploaded
        or downloaded

        Args:
            filePath: The full file path to get the file name for

        Returns:
            If the file path contains a valid filename, then
            the file name is returned.
            Else, if the file path is a folder or blank, then
            None is returned.
        """

        fileName = os.path.split(filePath)[1]

        if fileName is not '':
            return fileName
        else:
            return None

    def GetFileType(self, filePath):
        """Gets the file type from the file being uploaded
        or downloaded to the user's Google Drive Account

        Args:
            filePath: The file to get the file type for

        Returns:
            If the file has a file type, that file type is returned
            Else, this function returns None
        """

        fileType = os.path.splitext(filePath)[1]

        if fileType is not '':
            return fileType
        else:
            return None
