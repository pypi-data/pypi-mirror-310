from typing import Tuple


class Rsa:
    """RSA加解密
    """

    def __init__(self) -> None:
        ...

    def genkey(self)->Tuple[tuple, None]:
        """生成公司钥
        """
        ...

    def pub_decrypt(self, data:bytes,pub_key:str) -> bytes:
        """公钥解密

        Args:
            data (bytes): 二进制数据
            pub_key (str): 公钥字符串
        Returns:
            bytes: 解密后的二进制
        """
        ...
        
    def pri_decrypt(self, data:bytes,pri_key:str) -> bytes:
        """私钥解密

        Args:
            data (bytes): 二进制数据
            pri_key (str): 私钥字符串
        Returns:
            bytes: 解密后的二进制
        """
        ...

    def pub_encrypt(self, data:str,pub_key:str) -> bytes:
        """公钥加密

        Args:
            data (bytes): 二进制数据
            pub_key (str): 公钥字符串
        Returns:
            bytes: 加密后的二进制
        """
        ...
        
    def pri_encrypt(self, data:str,pri_key:str) -> bytes:
        """私钥加密

        Args:
            data (bytes): 二进制数据
            pri_key (str): 私钥字符串
        Returns:
            bytes: 加密后的二进制
        """
        ...
        