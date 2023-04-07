from os import mkdir
from os.path import exists
from shutil import rmtree


class __FilesManager:

    def __init__(self, dir_path: str) -> None:
        if not exists(dir_path):
            mkdir(dir_path)

        self.__dir_path: str = dir_path
        self.__paths: dict = {}

    def add_path(self, file_name: str, file_path: str) -> None:
        self.__paths[file_name] = file_path

    def get_path(self, file_name: str) -> str:
        path: str = self.__paths.get(file_name)

        if path is not None:
            self.__paths.pop(file_name)

        return path

    def __del__(self):
        rmtree(self.__dir_path)


files_manager: __FilesManager = __FilesManager(dir_path='assets/tempfiles')
