import json
import os


class LocalFileServiceClass:

    @staticmethod
    def write_json_file(filename, json_data):
        """Function responsible for writting JSON or Dictionary formatted data
        to a JSON file somewhere on local storage

        Args:
            filename: The full file path and filename where
            the data should to be saved
            json_data: Dictionary formatted data to be saved

        Returns:
            None
        """

        # Make sure the folder(s) exist before trying to save the file
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        with open(filename, 'w+') as write_file_ptr:
            json.dump(json_data, write_file_ptr)

    @staticmethod
    def read_json_file(filename):
        """Reads JSON formatted data into a dictionary object

        Args:
            filename: The full file path and file name of the data to be read

        Returns:
            A dictionary object of the file's contents
        """

        return_json_data = {}
        try:
            with open(filename) as read_file_ptr:
                return_json_data = json.load(read_file_ptr)
        except FileNotFoundError:
            print('File not found')

        return return_json_data

    @staticmethod
    def get_filename(file_path):
        """Gets the file name of the file being uploaded
        or downloaded

        Args:
            file_path: The full file path to get the file name for

        Returns:
            If the file path contains a valid filename, then
            the file name is returned.
            Else, if the file path is a folder or blank, then
            None is returned.
        """

        file_name = os.path.split(file_path)[1]

        if file_name is '':
            file_name = None

        return file_name

    @staticmethod
    def get_file_type(file_path):
        """Gets the file type from the file being uploaded
        or downloaded to the user's Google Drive Account

        Args:
        file_path: The file to get the file type for

        Returns:
            If the file has a file type, that file type is returned
            Else, this function returns None
        """

        file_type = os.path.splitext(file_path)[1]

        if file_type is '':
            file_type = None

        return file_type
