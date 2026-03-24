"""
加密器抽象基类
所有加密算法必须继承此类
"""
from abc import ABC, abstractmethod
import numpy as np
from typing import Any


class BaseEncryptor(ABC):
    """加密器抽象基类"""
    
    def __init__(self):
        self.default_key = None  # 默认密钥，由子类设置
    
    @abstractmethod
    def encrypt(self, image_np: np.ndarray, key: Any) -> np.ndarray:
        """
        加密图像
        
        Args:
            image_np: 输入图像的NumPy数组
            key: 加密密钥
            
        Returns:
            加密后的图像NumPy数组
        """
        pass
    
    @abstractmethod
    def decrypt(self, cryptogram_np: np.ndarray, key: Any) -> np.ndarray:
        """
        解密图像
        
        Args:
            cryptogram_np: 加密图像的NumPy数组
            key: 解密密钥
            
        Returns:
            解密后的图像NumPy数组
        """
        pass
    
    def get_default_key(self) -> Any:
        """
        获取默认密钥
        
        Returns:
            默认密钥
        """
        return self.default_key
