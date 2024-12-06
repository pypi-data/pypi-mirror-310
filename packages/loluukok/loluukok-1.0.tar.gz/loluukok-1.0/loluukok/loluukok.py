import os
import shutil

class File:
    def read(file_name):
        if not os.path.exists(file_name):
            raise FileNotFoundError(f"The file '{file_name}' can't be read because it doesn't exist.")
        with open(file_name, 'r') as file:
            return file.read()

    def write(file_name, text, mode='a'):
        if mode not in ['a', 'w']:
            raise ValueError("Mode must be 'a' (append) or 'w' (write).")
        with open(file_name, mode) as file:
            file.write(text)

    def exists(file_name):
        return os.path.exists(file_name)

    def delete(file_name):
        if os.path.exists(file_name):
            os.remove(file_name)
        else:
            raise FileNotFoundError(f"The file '{file_name}' doesn't exist and can't be deleted.")

    def rename(file_name, new_name):
        if os.path.exists(file_name):
            os.rename(file_name, new_name)
            return new_name
        else:
            raise FileNotFoundError(f"The file '{file_name}' doesn't exist and can't be renamed.")

class Directory:
    def listdir(path):
        if not os.path.exists(path):
            raise FileNotFoundError(f"The path '{path}' doesn't exist and its contents can't be listed.")
        return os.listdir(path)

    def isdir(path):
        return os.path.isdir(path)

    def mkdir(path):
        try:
            os.makedirs(path, exist_ok=True)
        except OSError as e:
            raise OSError(f"Something went wrong while creating the directory: {e}")

    def deldir(path):
        if os.path.isdir(path):
            try:
                shutil.rmtree(path)
            except OSError as e:
                raise OSError(f"Error while deleting directory '{path}' recursively: {e}")
        else:
            raise FileNotFoundError(f"The directory '{path}' doesn't exist and can't be removed.")
