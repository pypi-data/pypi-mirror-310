import os
import shutil

# File Operations
class File:
    @staticmethod
    def read(file_name):
        if not os.path.exists(file_name):
            raise FileNotFoundError(f"The file '{file_name}' cannot be read because it does not exist.")
        with open(file_name, 'r') as file:
            return file.read()

    @staticmethod
    def readlines(file_name):
        if not os.path.exists(file_name):
            raise FileNotFoundError(f"The file '{file_name}' cannot be read because it does not exist.")
        with open(file_name, 'r') as file:
            return file.readlines()

    @staticmethod
    def write(file_name, text, mode='a'):
        if mode not in ['a', 'w']:
            raise ValueError("Mode must be 'a' (append) or 'w' (write).")
        with open(file_name, mode) as file:
            file.write(text)

    @staticmethod
    def exists(file_name):
        return os.path.exists(file_name)

    @staticmethod
    def delete(file_name):
        if os.path.exists(file_name):
            os.remove(file_name)
        else:
            raise FileNotFoundError(f"The file '{file_name}' does not exist and cannot be deleted.")

    @staticmethod
    def rename(file_name, new_name):
        if os.path.exists(file_name):
            os.rename(file_name, new_name)
            return new_name
        else:
            raise FileNotFoundError(f"The file '{file_name}' does not exist and cannot be renamed.")

    @staticmethod
    def filesize(file_name):
        if os.path.exists(file_name):
            return os.path.getsize(file_name)
        raise FileNotFoundError(f"The file '{file_name}' does not exist.")

    @staticmethod
    def copy(src_file, dest_file):
        if not os.path.exists(src_file):
            raise FileNotFoundError(f"The source file '{src_file}' does not exist.")
        shutil.copy(src_file, dest_file)

# Directory Operations
class Directory:
    @staticmethod
    def lsdir(path):
        if not os.path.exists(path):
            raise FileNotFoundError(f"The path '{path}' does not exist and its contents cannot be listed.")
        return os.listdir(path)

    @staticmethod
    def isdir(path):
        return os.path.isdir(path)

    @staticmethod
    def mkdir(path):
        try:
            os.makedirs(path, exist_ok=True)
        except OSError as e:
            raise OSError(f"Error while creating the directory '{path}': {e}")

    @staticmethod
    def move(src_dir, dest_dir):
        if os.path.isdir(src_dir):
            shutil.move(src_dir, dest_dir)
        else:
            raise FileNotFoundError(f"The directory '{src_dir}' does not exist.")

    @staticmethod
    def rmdir(path):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            raise FileNotFoundError(f"The directory '{path}' does not exist or is not a directory.")
