#ifndef _h_aes_impl__
#define _h_aes_impl__
#include <string>

enum AlgmType{
    evp_aes_128_cbc = 0,
    evp_aes_192_cbc,
    evp_aes_256_cbc,

    evp_aes_128_ecb,
    evp_aes_192_ecb,
    evp_aes_256_ecb
};

class AesImpl{
public:



    std::string aes_encrypt(const std::string& plaintext, AlgmType type, const std::string& key, const std::string& iv);
    std::string aes_decrypt(const std::string& plaintext, AlgmType type, const std::string& key, const std::string& iv);
};


#endif // _h_aes_impl__