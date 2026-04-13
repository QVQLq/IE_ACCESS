"""
AES-CTR 基线算法
工程上广泛应用的工业级标准密码算法，用于与图像专用加密算法对比。
"""
import numpy as np
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from core.base_encryptor import BaseEncryptor


class AES_CTR_BaselineEncryptor(BaseEncryptor):
    """
    AES-CTR 基线加密器

    加密流程: 图像 → 字节流 → AES-CTR 加密 → 密文字节流 → 恢复图像
    解密流程: 密文图像 → 字节流 → AES-CTR 解密 → 明文字节流 → 恢复图像

    定位: 工业标准基线算法，不针对图像特性优化
    """

    def __init__(self):
        super().__init__()
        self.name = "AES-CTR 基线算法"

        self.default_key = {
            # 128-bit 密钥 (16 bytes)，默认全零，生产环境请替换
            'key': bytes(16),
            # 16 字节 nonce，计数器自动递增，无需手动管理
            'nonce': bytes(16),
        }

    def encrypt(self, image_np: np.ndarray, key: dict) -> np.ndarray:
        shape = image_np.shape

        # 图像 → 字节流
        flat_bytes = image_np.tobytes()

        # AES-CTR 加密
        cipher = Cipher(
            algorithms.AES(key['key']),
            modes.CTR(key['nonce']),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()
        crypt_bytes = encryptor.update(flat_bytes) + encryptor.finalize()

        # 密文字节流 → 密文图像
        encrypted = np.frombuffer(crypt_bytes, dtype=np.uint8).copy()
        encrypted = encrypted.reshape(shape)

        return encrypted

    def decrypt(self, cryptogram_np: np.ndarray, key: dict) -> np.ndarray:
        shape = cryptogram_np.shape

        # 密文图像 → 密文字节流
        crypt_bytes = cryptogram_np.tobytes()

        # AES-CTR 解密
        cipher = Cipher(
            algorithms.AES(key['key']),
            modes.CTR(key['nonce']),
            backend=default_backend()
        )
        decryptor = cipher.decryptor()
        plain_bytes = decryptor.update(crypt_bytes) + decryptor.finalize()

        # 明文字节流 → 图像
        decrypted = np.frombuffer(plain_bytes, dtype=np.uint8).copy()
        decrypted = decrypted.reshape(shape)

        return decrypted
