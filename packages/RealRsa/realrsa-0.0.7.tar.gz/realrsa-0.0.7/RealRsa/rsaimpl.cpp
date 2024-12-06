#include "rsaimpl.hpp"
#include <openssl/rsa.h>
#include <openssl/pem.h>
#include <openssl/err.h>
#include <openssl/evp.h>
#include <vector>
#include <string>
#include <cstdlib>
#include <stdexcept>


std::string RsaImpl::RSAPubDecrypt(const std::string& data, const std::string& pub_key) {
    BIO* keybio = BIO_new_mem_buf(pub_key.c_str(), -1);
    RSA* rsa = PEM_read_bio_RSAPublicKey(keybio, NULL, NULL, NULL);
    if (!rsa) {
        BIO_free(keybio);
        throw std::runtime_error("加载私钥失败");
    }

    int rsa_size = RSA_size(rsa);
    std::vector<unsigned char> decrypted(rsa_size);
    int result = RSA_public_decrypt(data.size(), (unsigned char*)data.data(), decrypted.data(), rsa, RSA_PKCS1_PADDING);

    RSA_free(rsa);
    BIO_free(keybio);

    if (result == -1) {
        throw std::runtime_error("Decryption failed");
    }

    return std::string(reinterpret_cast<char*>(decrypted.data()), result);
}

std::string RsaImpl::RSAPriDecrypt(const std::string& data, const std::string&pri_key)
{
    BIO* keybio = BIO_new_mem_buf(pri_key.c_str(), -1);
    RSA* rsa = PEM_read_bio_RSAPrivateKey(keybio, NULL, NULL, NULL);
    if (!rsa) {
        BIO_free(keybio);
        throw std::runtime_error("加载私钥失败");
    }

    int rsa_size = RSA_size(rsa);
    std::vector<unsigned char> decrypted(rsa_size);
    int result = RSA_private_decrypt(data.size(), (unsigned char*)data.data(), decrypted.data(), rsa, RSA_PKCS1_PADDING);

    RSA_free(rsa);
    BIO_free(keybio);

    if (result == -1) {
        throw std::runtime_error("Decryption failed");
    }

    return  std::string(reinterpret_cast<char*>(decrypted.data()), result);
}

std::string RsaImpl::RSAPubEecrypt(const std::string& data, const std::string& pub_key)
{
    BIO* keybio = BIO_new_mem_buf(pub_key.c_str(), -1);
    RSA* rsa = PEM_read_bio_RSAPublicKey(keybio, NULL, NULL, NULL);
    if (!rsa) {
        BIO_free(keybio);
        throw std::runtime_error("加载公钥失败");
    }

    int rsa_size = RSA_size(rsa);
    std::vector<unsigned char> encrypted(rsa_size);
    int result = RSA_public_encrypt(data.length(), (unsigned char*)data.c_str(), encrypted.data(), rsa, RSA_PKCS1_PADDING);

    RSA_free(rsa);
    BIO_free(keybio);

    if (result == -1) {
        throw std::runtime_error("Encryption failed");
    }

    return  std::string(encrypted.begin(), encrypted.end());
}


std::string RsaImpl::RSAPriEecrypt(const std::string& data, const std::string& pri_key)
{
    BIO* keybio = BIO_new_mem_buf(pri_key.c_str(), -1);
    RSA* rsa = PEM_read_bio_RSAPrivateKey(keybio, NULL, NULL, NULL);
    if (!rsa) {
        BIO_free(keybio);
        throw std::runtime_error("加载公钥失败");
    }

    int rsa_size = RSA_size(rsa);
    std::vector<unsigned char> encrypted(rsa_size);
    int result = RSA_private_encrypt(data.length(), (unsigned char*)data.c_str(), encrypted.data(), rsa, RSA_PKCS1_PADDING);

    RSA_free(rsa);
    BIO_free(keybio);

    if (result == -1) {
        throw std::runtime_error("Encryption failed");
    }

    return  std::string(encrypted.begin(), encrypted.end());
}