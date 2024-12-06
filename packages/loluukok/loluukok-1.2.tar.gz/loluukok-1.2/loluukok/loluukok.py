import os
import shutil

# File Operations
class File:
    def read(file_name):
        if not os.path.exists(file_name):
            raise FileNotFoundError(f"The file '{file_name}' can't be read because it doesn't exist.")
        with open(file_name, 'r') as file:
            return file.read()

    def readlines(file_name):
        if not os.path.exists(file_name):
            raise FileNotFoundError(f"The file '{file_name}' can't be read because it doesn't exist.")
        with open(file_name, 'r') as file:
            return file.readlines()

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

    def filesize(file_name):
        if os.path.exists(file_name):
            return os.path.getsize(file_name)
        raise FileNotFoundError(f"The file '{file_name}' doesn't exist.")

    def copy(src_file, dest_file):
        if not os.path.exists(src_file):
            raise FileNotFoundError(f"The source file '{src_file}' doesn't exist.")
        shutil.copy(src_file, dest_file)

# Directory Operations
class Directory:
    def lsdir(path):
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

    def move(src_dir, dest_dir):
        if os.path.isdir(src_dir):
            shutil.move(src_dir, dest_dir)
        else:
            raise FileNotFoundError(f"The directory '{src_dir}' doesn't exist.")

    def rmdir(path):
        if os.path.isdir(path):
            shutil.rmtree(path)
        elif os.path.isfile(path):
            os.remove(path)
        else:
            raise FileNotFoundError(f"The path '{path}' doesn't exist.")
