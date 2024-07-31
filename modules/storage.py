import os

class Storage:
    chunk_size = 0
    storage_path = ""

    @classmethod
    def configure(cls, SETTINGS):
        cls.chunk_size = SETTINGS["CHUNK_SIZE"]
        cls.storage_path = SETTINGS["STORAGE_PATH"]

    @staticmethod
    def get_path():
        return Storage.storage_path
    
    @staticmethod
    def upload(file):
        filename = os.path.basename(file.filename)
        file_path = os.path.join(Storage.storage_path, filename)

        if not Storage.is_safe_path(file_path):
            return False

        if os.path.exists(file_path):
            return False

        with open(file_path, "wb") as f:
            while True:
                chunk = file.stream.read(Storage.chunk_size)
                if not chunk:
                    break
                f.write(chunk)

        return True
    
    def get_file_size(file):
        file_path = os.path.join(Storage.storage_path, os.path.basename(file))
        if not Storage.is_safe_path(file_path):
            return -1
        
        return os.path.getsize(file_path)
    
    @staticmethod
    def exists(file):
        file_path = os.path.join(Storage.storage_path, os.path.basename(file))
        if not Storage.is_safe_path(file_path):
            return False
        
        return os.path.exists(file_path)

    @staticmethod
    def delete(file):
        file_path = os.path.join(Storage.storage_path, os.path.basename(file))
        if not Storage.is_safe_path(file_path):
            return False
        
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        
        return False
    
    @staticmethod
    def get(file):
        file_path = os.path.join(Storage.storage_path, os.path.basename(file))
        if not Storage.is_safe_path(file_path):
            raise FileNotFoundError(f"File not found: {file}")
        
        with open(file_path, "rb") as f:
            while True:
                chunk = f.read(Storage.chunk_size)
                if not chunk:
                    break
                yield chunk
    
    @staticmethod
    def is_safe_path(file_path):
        return os.path.abspath(file_path).startswith(os.path.abspath(Storage.storage_path))
