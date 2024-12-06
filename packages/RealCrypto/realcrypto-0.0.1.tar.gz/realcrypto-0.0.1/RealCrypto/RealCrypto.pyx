# distutils: language = c++
# cython: language_level=3

from rsaimpl cimport RsaImpl
from aesimpl cimport AesImpl
from aesimpl cimport AlgmType
from enum import Enum
from libcpp.string cimport string

cdef class Rsa:
    cdef RsaImpl *thisptr

    def __cinit__(self):
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


class AesType(Enum):
    evp_aes_128_cbc = 0
    evp_aes_192_cbc = 1
    evp_aes_256_cbc = 2

    evp_aes_128_ecb = 3
    evp_aes_192_ecb = 4
    evp_aes_256_ecb = 5


def aes_type_to_algmtype(t:AesType):
    if t == AesType.evp_aes_128_cbc:
        return AlgmType.evp_aes_128_cbc
    elif t == AesType.evp_aes_192_cbc:
        return AlgmType.evp_aes_192_cbc
    elif t == AesType.evp_aes_256_cbc:
        return AlgmType.evp_aes_256_cbc
    elif t == AesType.evp_aes_128_ecb:
        return AlgmType.evp_aes_128_ecb
    elif t == AesType.evp_aes_192_ecb:
        return AlgmType.evp_aes_192_ecb
    elif t == AesType.evp_aes_256_ecb:
        return AlgmType.evp_aes_256_ecb

cdef class Aes:
    cdef AesImpl *thisptr

    def __cinit__(self):
        self.thisptr = new AesImpl()

    def __dealloc__(self):
        del self.thisptr

    def encrypt(self, data, type:AesType, key,iv):
        return self.thisptr.aes_encrypt(data.encode("utf-8"),aes_type_to_algmtype(type), key.encode("utf-8"), iv.encode("utf-8"))

    def decrypt(self, data, type:AesType, key,iv):
        return self.thisptr.aes_decrypt(data, aes_type_to_algmtype(type),key.encode("utf-8"), iv.encode("utf-8"))
