# distutils: sources = rsaimpl.cpp
from libcpp.string cimport string

cdef extern from "rsaimpl.cpp":
    pass

cdef extern from "rsaimpl.hpp":
    cdef cppclass RsaImpl:
        RsaImpl() except +
        bint generate_key_pairs(string& pubkey, string& prikey) except +
        string RSAPubDecrypt(const string& data, const string& pub_key) except +
        string RSAPriDecrypt(const string& data, const string& pri_key) except +
        string RSAPubEecrypt(const string& data, const string& pub_key) except +
        string RSAPriEecrypt(const string& data, const string& pri_key) except +