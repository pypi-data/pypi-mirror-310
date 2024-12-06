# distutils: sources = rsaimpl.cpp
from libcpp.string cimport string

cdef extern from "aesimpl.cpp":
    pass

cdef extern from "aesimpl.hpp":

    cdef enum AlgmType:
        evp_aes_128_cbc = 0
        evp_aes_192_cbc = 1
        evp_aes_256_cbc = 2

        evp_aes_128_ecb = 3
        evp_aes_192_ecb = 4
        evp_aes_256_ecb = 5

    cdef cppclass AesImpl:
        AesImpl() except +
        string aes_encrypt(const string& plaintext, AlgmType type, const string& key, const string& iv) except +
        string aes_decrypt(const string& plaintext, AlgmType type, const string& key, const string& iv) except +