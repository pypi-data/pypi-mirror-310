# distutils: language = c++
# cython: language_level=3

from rsaimpl cimport RsaImpl
from libcpp.string cimport string
import warnings

cdef class Rsa:
    cdef RsaImpl *thisptr

    def __cinit__(self):
        warnings.warn("\n----------------------------------------------------------------------\n"
                      "RealRsa is deprecated. Please migrate to the RealCrypto project.\n" 
                      "The link is https://pypi.org/project/RealCrypto.\n"
                      "Install it with the command: pip install RealCrypto.\n"
                      "----------------------------------------------------------------------\n",DeprecationWarning)
        self.thisptr = new RsaImpl()

    def __dealloc__(self):
        del self.thisptr

    def genkey(self):
        cdef string pub
        cdef string pri
        if self.thisptr.generate_key_pairs(pub,pri):
            return pub.decode("utf-8"),pri.decode("utf-8")
        return None

    def pub_decrypt(self, data, pub_key):
        return self.thisptr.RSAPubDecrypt(data, pub_key.encode("utf-8"))

    def pri_decrypt(self, data, pri_key):
        return self.thisptr.RSAPriDecrypt(data, pri_key.encode("utf-8"))

    def pub_encrypt(self, data, pub_key):
        return self.thisptr.RSAPubEecrypt(data.encode("utf-8"), pub_key.encode("utf-8"))

    def pri_encrypt(self, data, pri_key):
        return self.thisptr.RSAPriEecrypt(data.encode("utf-8"), pri_key.encode("utf-8"))