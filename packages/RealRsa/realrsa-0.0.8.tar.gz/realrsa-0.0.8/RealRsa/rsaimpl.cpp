#include "rsaimpl.hpp"
#include <openssl/rsa.h>
#include <openssl/pem.h>
#include <openssl/err.h>
#include <openssl/evp.h>
#include <vector>
#include <string>
#include <cstdlib>
#include <stdexcept>



bool RsaImpl::generate_key_pairs(std::string& pubkey, std::string& prikey)
{
    RSA* rsa = RSA_generate_key(2048, RSA_F4, NULL, NULL);
    if (!rsa) {
        return false;
    }

    BIO* pri = BIO_new(BIO_s_mem());
    BIO* pub = BIO_new(BIO_s_mem());

    PEM_write_bio_RSAPrivateKey(pri, rsa, NULL, NULL, 0, NULL, NULL);
    PEM_write_bio_RSAPublicKey(pub, rsa);

    int pri_len = BIO_pending(pri);
    int pub_len = BIO_pending(pub);

    prikey.resize(pri_len, 0);
    pubkey.resize(pub_len, 0);

    BIO_read(pri, (void*)prikey.data(), pri_len);
    BIO_read(pub, (void*)pubkey.data(), pub_len);

    BIO_free(pri);
    BIO_free(pub);
    RSA_free(rsa);
    return true;
}


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