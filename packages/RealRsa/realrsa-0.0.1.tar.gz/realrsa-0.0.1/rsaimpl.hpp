#ifndef _h_rsa_impl__
#define _h_rsa_impl__
#include <string>

class RsaImpl{
public:
    std::string RSAPubDecrypt(const char* data, const char* pub_key);
    std::string RSAPriDecrypt(const char* data, const char* pub_key);

    std::string RSAPubEecrypt(const std::string& data, const std::string& pub_key);
    std::string RSAPriEecrypt(const std::string& data, const std::string& pub_key);
};


#endif  // _h_rsa_impl__

