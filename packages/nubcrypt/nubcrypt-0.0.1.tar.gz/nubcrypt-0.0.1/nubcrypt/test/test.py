import unittest
import os
import hashlib
import nubcrypt as nbx


class TestNubcrypt2(unittest.TestCase):

    def setUp(self) -> None:
       self.key = "secret"
       self.dir = os.path.dirname(__file__)

    def __hashfile(self,filename):
        # BUF_SIZE is totally arbitrary, change for your app!
        BUF_SIZE = 65536  # lets read stuff in 64kb chunks!

        md5 = hashlib.md5()
        sha1 = hashlib.sha1()

        with open(filename, 'rb') as f:
            while True:
                data = f.read(BUF_SIZE)
                if not data:
                    break
                md5.update(data)
                sha1.update(data)

        return md5.hexdigest()

    def test_file_integrity(self):
        file = self.dir + os.sep + "test.txt"
        outfile = file + ".nubc"
        
        if os.path.isfile(outfile):
            os.remove(outfile)

        filehash = self.__hashfile(file)
        nbx.encrypt_file(file, self.key, outfile)
        dec_file = outfile + "_dec"
        if os.path.isfile(dec_file):
            os.remove(dec_file)

        nbx.decrypt_file(outfile,self.key, dec_file )
        dec_file_hash = self.__hashfile(dec_file)
        os.remove(dec_file)
        self.assertEqual(filehash, dec_file_hash, "File hash isn't match")

    def test_random_string(self):
        rand_bytes =os.urandom(1024)
        x = nbx.encrypt_bytes(rand_bytes, self.key)
        dx = nbx.decrypt_bytes(x, self.key)
        self.assertEqual(rand_bytes, dx, "random string doesn't match")

    def test_random_key(self):
        rand_bytes = os.urandom(1024)
        rand_keys = os.urandom(10).decode("latin")
        x = nbx.encrypt_bytes(rand_bytes, rand_keys)
        dx = nbx.decrypt_bytes(x, rand_keys)
        self.assertEqual(rand_bytes, dx, "random string doesn't match")

    def test_string(self):
        rand_bytes = "nubcrypt file encryption".encode()
        x = nbx.encrypt_bytes(rand_bytes,self.key)
        dx = nbx.decrypt_bytes(x, self.key)
        self.assertEqual(rand_bytes, dx, "string doesn't match")


    def test_key_error(self):
        rand_bytes =os.urandom(1024)
        x = nbx.encrypt_bytes(rand_bytes, self.key)
        status = False
        try:
            dx = nbx.decrypt_bytes(x, "wrong key")
        except nbx.errors.DecryptionError as e:
                status = True
        self.assertEqual(True, status, "Key wrong doesn't detected")
        

if __name__ == '__main__':
    unittest.main()