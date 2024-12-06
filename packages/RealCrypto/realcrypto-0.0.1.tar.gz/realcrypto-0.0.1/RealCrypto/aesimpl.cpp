#include "aesimpl.hpp"
#include <openssl/err.h>
#include <openssl/aes.h>
#include <openssl/evp.h>
#include <stdexcept>
#include <vector>

const EVP_CIPHER * type_to_algmptr(AlgmType type){
    switch (type)
    {
    case AlgmType::evp_aes_128_cbc: return ::EVP_aes_128_cbc();
    case AlgmType::evp_aes_192_cbc: return ::EVP_aes_192_cbc();
    case AlgmType::evp_aes_256_cbc: return ::EVP_aes_256_cbc();
    case AlgmType::evp_aes_128_ecb: return ::EVP_aes_128_ecb();
    case AlgmType::evp_aes_192_ecb: return ::EVP_aes_192_ecb();
    case AlgmType::evp_aes_256_ecb: return ::EVP_aes_256_ecb();
    default:
        break;
    }
    throw std::runtime_error("Unsupported algorithm type.");
}

// AES encryption
std::string AesImpl::aes_encrypt(const std::string& plaintext, AlgmType type, const std::string& key, const std::string& iv) {
    EVP_CIPHER_CTX *ctx = EVP_CIPHER_CTX_new();
    
    // 使用AES256 CBC加密算法， 还可以切换其他的。 如EVP_aes_256_ecb EVP_aes_128_cbc 等
    if (!EVP_EncryptInit_ex(ctx, type_to_algmptr(type), NULL, (unsigned char*)key.data(), (unsigned char*)iv.data())){
        EVP_CIPHER_CTX_free(ctx);
        throw std::runtime_error("key loading failed, please check the key length");
    }

    std::vector<unsigned char> ciphertext(plaintext.size() + AES_BLOCK_SIZE);
    int len = 0, ciphertext_len = 0;

    EVP_EncryptUpdate(ctx, ciphertext.data(), &len, reinterpret_cast<const unsigned char*>(plaintext.data()), plaintext.size());
    ciphertext_len = len;

    EVP_EncryptFinal_ex(ctx, ciphertext.data() + len, &len);
    ciphertext_len += len;

    EVP_CIPHER_CTX_free(ctx);
    ciphertext.resize(ciphertext_len);
    return std::string(reinterpret_cast<char*>(ciphertext.data()), ciphertext_len);
}

// AES decryption
std::string AesImpl::aes_decrypt(const std::string& ciphertext, AlgmType type, const std::string& key, const std::string& iv) 
{
    EVP_CIPHER_CTX *ctx = EVP_CIPHER_CTX_new();

    if (!EVP_DecryptInit_ex(ctx, type_to_algmptr(type), NULL, (unsigned char*)key.data(), (unsigned char*)iv.data()))
    {
        EVP_CIPHER_CTX_free(ctx);
        throw std::runtime_error("key loading failed, please check the key length");
    }

    std::vector<unsigned char> plaintext(ciphertext.size());
    int len = 0, plaintext_len = 0;

    EVP_DecryptUpdate(ctx, plaintext.data(), &len, (unsigned char*)ciphertext.data(), ciphertext.size());
    plaintext_len = len;

    EVP_DecryptFinal_ex(ctx, plaintext.data() + len, &len);
    plaintext_len += len;

    EVP_CIPHER_CTX_free(ctx);
    return std::string(reinterpret_cast<char*>(plaintext.data()), plaintext_len);
}
