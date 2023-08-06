from . import _core
from . import errors
import hashlib
import os



class Config:
    extension = "nubx".encode()
    INDEX_KEY= 42

 
class _Nubcrypt(Config):
    
    def __init__(self, k):
        if not k:
            raise ValueError("Key cannot empty")
        self.key = str(k)

        __index_key = str(self.INDEX_KEY).encode()
        
        self.__signature = hashlib.sha256(self.key.encode() + __index_key).digest() + self.extension

    @classmethod
    def is_file_nubcrypted(cls, filename):
        filesize = os.path.getsize(filename)
        with open(filename,"rb") as f:
            f.seek(filesize - len(cls.extension),0)
            _ext  = f.read()
            return _ext == cls.extension

    @classmethod
    def is_bytes_nubcrypted(cls, bytes_data):
        return bytes_data.endswith(cls.extension)

    def encrypt_file(self,filename, outfile, progress_callback=None):
        _core.encrypt_file(filename, self.key, outfile, progress_callback)
        self.__append_file_sign(outfile)

    def decrypt_file(self, filename, outfile, progress_callback=None):
        self.__delete_file_sign(filename)
        _core.decrypt_file(filename, self.key,outfile, progress_callback)
        os.remove(filename)

    def encrypt_bytes(self, bytes_data,):
        _bytes = bytearray(bytes_data)
        _bytes = self.__append_bytes_sign(_bytes)
        _core.encrypt_bytes(_bytes, self.key)
        return _bytes

    def decrypt_bytes(self, bytes_data):
        _bytes = bytearray(bytes_data)
        _core.decrypt_bytes(_bytes, self.key)
        _bytes = self.__delete_bytes_sign(_bytes)
        return _bytes
    
    def __append_bytes_sign(self, bytes_data):
       return bytes_data + self.__signature

    def __append_file_sign(self, filename):
        with open(filename, "ab+") as f:
            f.write(self.__signature)

    def __get_bytes_sign(self, bytes_data):
        _sign = bytes_data[-len(self.__signature):]
        if _sign == self.__signature:
            return _sign
        
        raise errors.DecryptionError("Wrong decryption Key")

    def __delete_file_sign(self, filename):
        eof = os.path.getsize(filename)
        with open(filename, "rb+") as f:
            f.seek(eof - len(self.__signature),0)
            _sign = f.read()
            if _sign == self.__signature:
                f.seek(0)
                f.seek(eof - len(self.__signature),0)
                f.truncate(f.tell())
                return _sign

        raise errors.DecryptionError("Wrong decryption key")

    def __delete_bytes_sign(self, bytes_data):
        _sign = self.__get_bytes_sign(bytes_data)
        bytes_data = bytes_data[:-len(_sign)]
        return bytes_data
    

def encrypt_file(filename, key, outputfile=None):
    n = _Nubcrypt(key)

    if filename == outputfile:
        raise FileExistsError("Output file cannot same as target file")
    
    if os.path.isfile(outputfile):
        raise FileExistsError(f"File with name \"{outputfile}\" already exist")

    def progress_info(progress, filesize):
         print("PROGRESS: {:>3} / {:<3} bytes | {:.0f}% ".format(progress, filesize, progress/filesize * 100), end="\r")
    
    print(f"[ENCRYPTING] {filename}")
    n.encrypt_file(filename, outputfile, progress_callback=progress_info)
    print("")
    print("ENCRYPTING done!\n")

def decrypt_file(filename, key, outputfile):
    n = _Nubcrypt(key)

    
    if filename == outputfile:
        raise FileExistsError("Output file cannot same as target file")
    
    if os.path.isfile(outputfile):
        raise FileExistsError(f"File with name \"{outputfile}\" already exist")

    if not is_file_nubcrypted(filename):
        raise errors.DecryptionError(f"\"{filename}\" was not encrypted")

    

    def progress_info(progress, filesize):
         print("PROGRESS: {:>3} / {:<3} bytes | {:.0f}% ".format(progress, filesize, progress/filesize * 100), end="\r")
    print(f"[DECRYPTING] {filename}")
    try:
        n.decrypt_file(filename, outputfile, progress_callback=progress_info)
        print("")
        print("DECRYPTING done!\n")
    except errors.DecryptionError:
        print("DECRYPTING failed!")

def encrypt_bytes(bytes, key):
    n = _Nubcrypt(key)
    if not bytes:
        raise ValueError("bytes cannot empty")
    return n.encrypt_bytes(bytes)

def decrypt_bytes(bytes, key):
    n = _Nubcrypt(key)
    if not bytes:
        raise ValueError("bytes cannot empty")
    return n.decrypt_bytes(bytes)

def is_file_nubcrypted(filename):
    return _Nubcrypt.is_file_nubcrypted(filename)

def is_bytes_nubcrypted(bytes_data):
    return _Nubcrypt.is_bytes_nubcrypted(bytes_data)

