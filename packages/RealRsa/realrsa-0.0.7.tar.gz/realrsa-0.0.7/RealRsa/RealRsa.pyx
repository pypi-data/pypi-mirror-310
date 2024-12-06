# distutils: language = c++
# cython: language_level=3

from rsaimpl cimport RsaImpl

cdef class Rsa:
    cdef RsaImpl *thisptr

    def __cinit__(self):
        self.thisptr = new RsaImpl()

    def __dealloc__(self):
        del self.thisptr

    def pub_decrypt(self, data, pub_key):
        return self.thisptr.RSAPubDecrypt(data, pub_key.encode("utf-8"))

    def pri_decrypt(self, data, pri_key):
        return self.thisptr.RSAPriDecrypt(data, pri_key.encode("utf-8"))

    def pub_encrypt(self, data, pub_key):
        return self.thisptr.RSAPubEecrypt(data.encode("utf-8"), pub_key.encode("utf-8"))

    def pri_encrypt(self, data, pri_key):
        return self.thisptr.RSAPriEecrypt(data.encode("utf-8"), pri_key.encode("utf-8"))