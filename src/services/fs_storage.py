from src.utils.defaults import default_directory_creator


class FileSystemStorage:
    def __init__(self, directory_creator, base_directory):
        self._base_directory = base_directory
        directory_creator(self._base_directory)

    def save(self, filename, content):
        with open(
            "/".join([self._base_directory, filename]), "w", encoding="utf-8"
        ) as file:
            file.write(content)


def fs_storage_factory(base_directory):
    return FileSystemStorage(default_directory_creator, base_directory)
