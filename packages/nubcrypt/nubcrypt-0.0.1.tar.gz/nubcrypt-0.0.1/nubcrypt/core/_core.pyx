from libc.stdio cimport FILE, fopen, fread, fwrite, fclose, printf
from libc.stdint cimport uint64_t
from libc.stdlib cimport malloc, free
from libc.string cimport strncpy, strlen

import cython
import os
import hashlib
import copy
import base64

import array
from cpython cimport array

DEF BUFF_SIZE = 320


hk_gen = lambda x : hashlib.sha512(x).digest()
b64_gen = lambda x : base64.encodebytes(x)

cdef void reverseBuffer(char* buffer, size_t bufferSize):
    cdef int isOdd = bufferSize % 2
    cdef size_t loop_range = 0
    if not isOdd: loop_range = bufferSize / 2
    else: loop_range = (bufferSize - 1) / 2
	
    cdef size_t i
    cdef size_t dest_idx
    cdef char dest
    for i in range(loop_range):
        dest_idx = bufferSize -i -1 
        dest = buffer[dest_idx]
        buffer[dest_idx] = buffer[i]
        buffer[i] = dest


cdef void encrypt_buffer(char* buffer, size_t count,array.array seeds, size_t seeds_size, char* b64key):
    cdef size_t i
    cdef size_t buffer_i
    for i in range(seeds_size):
        buffer_i = seeds[i] % (count + 1)
        reverseBuffer(buffer, buffer_i)

    # CBC XOR BUFFER
    cdef size_t b64_i
    cdef size_t b64key_len = strlen(b64key)
    for i in range(count):
        b64_i = i % (b64key_len + 1) 
        if i == 0:
            buffer[i] ^= b64key[b64_i]
        else:
            buffer[i] ^= buffer[i-1] ^ b64key[b64_i]

cdef void decrypt_buffer(char* buffer, size_t count, array.array seeds, size_t seeds_size, char* b64key):
    
    cdef size_t i
    cdef size_t buffer_i
    cdef size_t b64_i
    cdef size_t b64key_len = strlen(b64key)

    # CBC XOR BUFFER
    for i in reversed(range(count)):
        b64_i = i  % (b64key_len + 1) 
        if i == 0:
            buffer[i] ^= b64key[b64_i]
        else:
            buffer[i] ^= buffer[i-1] ^ b64key[b64_i]
    
    
    for i in range(seeds_size):
        buffer_i = seeds[i] % (count + 1)
        reverseBuffer(buffer, buffer_i)



def decrypt_file(filename, key, outfile, progress_callback=None):
    cdef FILE* istream
    cdef FILE* ostream

    _filesize = os.path.getsize(filename)
    key = key + str(_filesize)

    cdef uint64_t filesize = _filesize
    cdef uint64_t read_total = 0

    cdef char buffer[BUFF_SIZE]

    istream = fopen(filename.encode(), "rb")
    ostream = fopen(outfile.encode(), "ab")
  
    cdef array.array seeds
    seeds = generate_seeds(key, BUFF_SIZE)[::-1]
    cdef size_t count;
    cdef bytes py_bytes = b64_gen(hk_gen(key.encode())) 
    cdef char* b64key = py_bytes
    while (read_total < filesize):
        count = fread(buffer, cython.sizeof(cython.char), BUFF_SIZE, istream)
        read_total += count
        decrypt_buffer(buffer, count, seeds, len(seeds), b64key)
        fwrite(buffer, cython.sizeof(cython.char), count, ostream)
        if progress_callback:
                # progress_bar.UpdateBar(progress, n.filesize)
                progress_callback(read_total, filesize)

            # print(read_total, filesize)
    fclose(istream)
    fclose(ostream)


def encrypt_file(filename, key, outfile, progress_callback=None):
    cdef FILE* istream
    cdef FILE* ostream

    _filesize = os.path.getsize(filename)
    cdef uint64_t filesize = _filesize
    key = key + str(_filesize)

    cdef uint64_t read_total = 0

    cdef char buffer[BUFF_SIZE]

    istream = fopen(filename.encode(), "rb")
    ostream = fopen(outfile.encode(), "ab")


    cdef array.array seeds
    seeds = generate_seeds(key, BUFF_SIZE)
    cdef size_t count;
    cdef bytes py_bytes = b64_gen(hk_gen(key.encode())) 
    cdef char* b64key = py_bytes
    
    while (read_total < filesize):
        count = fread(buffer, cython.sizeof(cython.char), BUFF_SIZE, istream)
        read_total += count
        encrypt_buffer(buffer, count, seeds, len(seeds), b64key)
        fwrite(buffer, cython.sizeof(cython.char), count, ostream)
        if progress_callback:
                # progress_bar.UpdateBar(progress, n.filesize)
                progress_callback(read_total, filesize)
        
    fclose(istream)
    fclose(ostream)


cdef array.array _reverse_seeds(array.array a, Py_ssize_t n):
    cdef int isOdd = n % 2
    cdef size_t loop_range = 0
    if not isOdd: loop_range = n / 2
    else: loop_range = (n - 1) / 2
	
    cdef size_t i
    cdef size_t dest_idx
    cdef int dest
    for i in range(loop_range):
        dest_idx = n -i -1 
        dest = a[dest_idx]
        a[dest_idx] = a[i]
        a[i] = dest
    return a

cdef array.array _shuffle_seeds(array.array hkey, array.array seeds):
    cdef Py_ssize_t seeds_i
    cdef Py_ssize_t hkey_i
    cdef int hkey_v
    cdef Py_ssize_t n
    cdef Py_ssize_t hkey_size = len(hkey)
    for seeds_i in range(len(seeds)):
        for hkey_i in range(hkey_size):
            n = (seeds_i  +  hkey[hkey_i]) % (len(seeds) + 1)
            _reverse_seeds(seeds, n)
    return seeds

cdef array.array generate_seeds(key, bound):
    hkey_digest = hk_gen(key.encode())
    cdef array.array hkey = array.array("I",[h for h in hkey_digest])
    cdef array.array seeds = array.array("I",  [i for i in range(bound)])
    seeds = _shuffle_seeds(hkey, seeds)
    return seeds


def encrypt_bytes(bytes_data, key):
    cdef char* buffer = bytes_data
    key = key + str(len(bytes_data))
    cdef array.array seeds = generate_seeds(key, len(bytes_data))
    cdef bytes py_bytes = b64_gen(hk_gen(key.encode())) 
    cdef char* b64key = py_bytes
    encrypt_buffer(buffer, len(bytes_data), seeds, len(seeds), b64key)
    

def decrypt_bytes(bytes_data, key):
    cdef char* buffer = bytes_data
    key = key + str(len(bytes_data))
    cdef array.array seeds = generate_seeds(key, len(bytes_data))[::-1]
    cdef bytes py_bytes = b64_gen(hk_gen(key.encode())) 
    cdef char* b64key = py_bytes
    decrypt_buffer(buffer, len(bytes_data), seeds, len(seeds),b64key)




