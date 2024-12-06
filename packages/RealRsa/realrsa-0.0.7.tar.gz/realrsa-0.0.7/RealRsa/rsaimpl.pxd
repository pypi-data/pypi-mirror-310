# distutils: sources = rsaimpl.cpp
from libcpp.string cimport string

cdef extern from "rsaimpl.cpp":
    pass

cdef extern from "rsaimpl.hpp":
    cdef cppclass RsaImpl:
        RsaImpl() except +
        string RSAPubDecrypt(const string& data, const string& pub_key) 
        string RSAPriDecrypt(const string& data, const string& pri_key)
        string RSAPubEecrypt(const string& data, const string& pub_key);
        string RSAPriEecrypt(const string& data, const string& pri_key);