from typing import Tuple

class AesType:
    evp_aes_128_cbc = 0
    evp_aes_192_cbc = 1
    evp_aes_256_cbc = 2

    evp_aes_128_ecb = 3
    evp_aes_192_ecb = 4
    evp_aes_256_ecb = 5

class Aes:
    """Aes加解密
    """

    def __init__(self) -> None:
        ...


    def encrypt(self, data:str, type:AlgmType, key:str, iv:str) -> bytes:
        """加密

        Args:
            data (str): 二进制数据
            key (str): 密钥
            iv (str): 初始化向量
        Returns:
            bytes: 加密后的二进制
        """
        ...


    def decrypt(self, data:bytes, type:AlgmType, key:str, iv:str) -> bytes:
        """解密

        Args:
            data (bytes): 二进制数据
            key (str): 密钥
            iv (str): 初始化向量
        Returns:
            bytes: 解密后的二进制
        """
        ...
        


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
            data (str): 二进制数据
            pub_key (str): 公钥字符串
        Returns:
            bytes: 加密后的二进制
        """
        ...
        
    def pri_encrypt(self, data:str,pri_key:str) -> bytes:
        """私钥加密

        Args:
            data (str): 二进制数据
            pri_key (str): 私钥字符串
        Returns:
            bytes: 加密后的二进制
        """
        ...
        