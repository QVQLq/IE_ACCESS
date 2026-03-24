"""
Logistic 混沌加密算法
基于 Logistic 映射的简单图像加密算法
适合作为对比算法展示
"""
import numpy as np
from core.base_encryptor import BaseEncryptor


class LogisticChaosEncryptor(BaseEncryptor):
    """
    Logistic 混沌加密器
    
    算法原理:
    1. 使用 Logistic 映射生成混沌序列
    2. 将混沌序列转换为密钥流
    3. 通过 XOR 运算加密图像
    
    特点:
    - 简单易懂
    - 计算快速
    - 适合教学演示
    """
    
    def __init__(self):
        super().__init__()
        self.name = "Logistic 混沌加密"
        
        # 默认密钥参数
        self.default_key = {
            'r': 3.9999,      # Logistic 参数 (3.57 < r <= 4)
            'x0': 0.123456    # 初始值 (0 < x0 < 1)
        }
    
    def _generate_logistic_sequence(self, length: int, r: float, x0: float) -> np.ndarray:
        """
        生成 Logistic 混沌序列
        
        Logistic 映射: x(n+1) = r * x(n) * (1 - x(n))
        
        Args:
            length: 序列长度
            r: Logistic 参数
            x0: 初始值
            
        Returns:
            混沌序列 (0-255 整数)
        """
        sequence = np.zeros(length, dtype=np.uint8)
        x = x0
        
        # 预热 1000 次，消除瞬态效应
        for _ in range(1000):
            x = r * x * (1 - x)
        
        # 生成序列
        for i in range(length):
            x = r * x * (1 - x)
            # 转换为 0-255 整数
            sequence[i] = int((x * 10**10) % 256)
        
        return sequence
    
    def encrypt(self, image_np: np.ndarray, key: dict) -> np.ndarray:
        """
        加密图像
        
        Args:
            image_np: 输入图像
            key: 密钥字典 {'r': float, 'x0': float}
            
        Returns:
            加密后的图像
        """
        # 获取参数
        r = key.get('r', 3.9999)
        x0 = key.get('x0', 0.123456)
        
        # 展平图像
        original_shape = image_np.shape
        flat_image = image_np.flatten()
        length = len(flat_image)
        
        # 生成混沌密钥流
        key_stream = self._generate_logistic_sequence(length, r, x0)
        
        # XOR 加密
        encrypted_flat = np.bitwise_xor(flat_image, key_stream)
        
        # 重组为原始形状
        encrypted = encrypted_flat.reshape(original_shape)
        
        return encrypted.astype(np.uint8)
    
    def decrypt(self, cryptogram_np: np.ndarray, key: dict) -> np.ndarray:
        """
        解密图像
        
        XOR 是对称运算，加密和解密相同
        
        Args:
            cryptogram_np: 加密图像
            key: 密钥字典
            
        Returns:
            解密后的图像
        """
        return self.encrypt(cryptogram_np, key)


class LogisticPermutationEncryptor(BaseEncryptor):
    """
    Logistic 置乱加密器
    
    算法原理:
    1. 使用 Logistic 映射生成混沌序列
    2. 根据序列排序生成置乱索引
    3. 按索引重排像素位置
    4. 使用混沌序列进行扩散
    
    特点:
    - 包含置乱和扩散两个阶段
    - 比纯 XOR 更安全
    - 仍然保持简单易懂
    """
    
    def __init__(self):
        super().__init__()
        self.name = "Logistic 置乱扩散加密"
        
        self.default_key = {
            'r1': 3.9999,     # 置乱参数
            'x1': 0.123456,   # 置乱初始值
            'r2': 3.8888,     # 扩散参数
            'x2': 0.654321    # 扩散初始值
        }
    
    def _generate_logistic_sequence(self, length: int, r: float, x0: float) -> np.ndarray:
        """生成 Logistic 混沌序列"""
        sequence = np.zeros(length, dtype=np.float64)
        x = x0
        
        # 预热
        for _ in range(1000):
            x = r * x * (1 - x)
        
        # 生成
        for i in range(length):
            x = r * x * (1 - x)
            sequence[i] = x
        
        return sequence
    
    def _permute(self, data: np.ndarray, r: float, x0: float) -> np.ndarray:
        """置乱操作"""
        length = len(data)
        
        # 生成混沌序列
        chaos_seq = self._generate_logistic_sequence(length, r, x0)
        
        # 生成置乱索引
        indices = np.argsort(chaos_seq)
        
        # 置乱
        return data[indices]
    
    def _inverse_permute(self, data: np.ndarray, r: float, x0: float) -> np.ndarray:
        """逆置乱操作"""
        length = len(data)
        
        # 生成相同的混沌序列
        chaos_seq = self._generate_logistic_sequence(length, r, x0)
        
        # 生成置乱索引
        indices = np.argsort(chaos_seq)
        
        # 创建逆索引
        inverse_indices = np.zeros_like(indices)
        inverse_indices[indices] = np.arange(length)
        
        # 逆置乱
        return data[inverse_indices]
    
    def _diffuse(self, data: np.ndarray, r: float, x0: float) -> np.ndarray:
        """扩散操作"""
        length = len(data)
        
        # 生成混沌密钥流
        x = x0
        for _ in range(1000):
            x = r * x * (1 - x)
        
        # 扩散
        result = np.zeros(length, dtype=np.int32)
        result[0] = int((int(data[0]) ^ int((x * 10**10) % 256)) % 256)
        
        for i in range(1, length):
            x = r * x * (1 - x)
            key_byte = int((x * 10**10) % 256)
            result[i] = int((int(data[i]) ^ key_byte ^ int(result[i-1])) % 256)
        
        return result.astype(np.uint8)
    
    def _inverse_diffuse(self, data: np.ndarray, r: float, x0: float) -> np.ndarray:
        """逆扩散操作"""
        length = len(data)
        
        # 生成相同的混沌密钥流
        x = x0
        for _ in range(1000):
            x = r * x * (1 - x)
        
        # 逆扩散
        result = np.zeros(length, dtype=np.int32)
        result[0] = int((int(data[0]) ^ int((x * 10**10) % 256)) % 256)
        
        for i in range(1, length):
            x = r * x * (1 - x)
            key_byte = int((x * 10**10) % 256)
            result[i] = int((int(data[i]) ^ key_byte ^ int(data[i-1])) % 256)
        
        return result.astype(np.uint8)
    
    def encrypt(self, image_np: np.ndarray, key: dict) -> np.ndarray:
        """
        加密图像
        
        流程: 原图 → 置乱 → 扩散 → 密文
        """
        # 获取参数
        r1 = key.get('r1', 3.9999)
        x1 = key.get('x1', 0.123456)
        r2 = key.get('r2', 3.8888)
        x2 = key.get('x2', 0.654321)
        
        # 展平图像
        original_shape = image_np.shape
        flat_image = image_np.flatten()
        
        # 阶段1: 置乱
        permuted = self._permute(flat_image, r1, x1)
        
        # 阶段2: 扩散
        encrypted = self._diffuse(permuted, r2, x2)
        
        # 重组
        return encrypted.reshape(original_shape)
    
    def decrypt(self, cryptogram_np: np.ndarray, key: dict) -> np.ndarray:
        """
        解密图像
        
        流程: 密文 → 逆扩散 → 逆置乱 → 原图
        """
        # 获取参数
        r1 = key.get('r1', 3.9999)
        x1 = key.get('x1', 0.123456)
        r2 = key.get('r2', 3.8888)
        x2 = key.get('x2', 0.654321)
        
        # 展平图像
        original_shape = cryptogram_np.shape
        flat_encrypted = cryptogram_np.flatten()
        
        # 阶段1: 逆扩散
        diffused = self._inverse_diffuse(flat_encrypted, r2, x2)
        
        # 阶段2: 逆置乱
        decrypted = self._inverse_permute(diffused, r1, x1)
        
        # 重组
        return decrypted.reshape(original_shape)
