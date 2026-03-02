# -*- coding: utf-8 -*-
"""
加密模块
"""
import time
import numpy as np


class CipherEngine:
    """可复现的图像加密引擎"""
    
    def encrypt(self, image, params):
        """
        使用 XOR 加密图像（可复现）
        
        加密规则：
        1. 使用 seed 生成与 image 同 shape 的 uint8 随机密钥流
        2. cipher = image XOR key_stream（逐元素按位异或）
        3. 支持灰度 (H,W) 和 RGB (H,W,3)
        
        Args:
            image: 明文图像 numpy 数组 (H,W) 或 (H,W,3)
            params: 加密参数字典，必须包含 "seed"
            
        Returns:
            numpy.ndarray: 密文图像，与输入同 shape 和 dtype
        """
        # 使用 numpy 新版随机数生成器确保可复现性
        rng = np.random.default_rng(params["seed"])
        
        # 生成与输入同 shape 的 uint8 随机密钥流
        key_stream = rng.integers(0, 256, size=image.shape, dtype=np.uint8)
        
        # 逐元素按位异或
        cipher = np.bitwise_xor(image, key_stream)
        
        return cipher


class Encryptor:
    """图像加密器（封装 CipherEngine）"""
    
    def __init__(self):
        self.cipher_engine = CipherEngine()
    
    def encrypt(self, plain_image, params):
        """
        加密图像并计时
        
        Args:
            plain_image: 明文图像 numpy 数组
            params: 加密参数字典
            
        Returns:
            dict: 包含 cipher 和 enc_time_ms
        """
        # 只计时加密本体
        start_time = time.time()
        cipher = self.cipher_engine.encrypt(plain_image, params)
        end_time = time.time()
        
        enc_time_ms = (end_time - start_time) * 1000
        
        return {
            "cipher": cipher,
            "enc_time_ms": enc_time_ms
        }
