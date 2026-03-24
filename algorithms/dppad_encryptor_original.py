"""
DPPAD-IE 加密算法 (原始版本)
基于双向扩散和置乱的图像加密算法
"""
import numpy as np
import math
from numba import njit
from core.base_encryptor import BaseEncryptor


# =========================================================================
# 核心计算区 (原始版本 - 未优化)
# =========================================================================

@njit
def generate_2d_cghm_original(x3_init, y3_init, a1, b1, L):
    """
    利用 2D-CGHM 生成扩散所需的 K1, K2, K3 混沌序列
    原始版本：使用 np.zeros 和模运算
    """
    L_half = L // 2
    xn = np.zeros(L_half, dtype=np.float64)
    yn = np.zeros(L_half, dtype=np.float64)
    
    x, y = x3_init, y3_init
    
    # 预热 1000 次，消除瞬态效应
    for _ in range(1000):
        x_next = a1 * math.cos(math.exp(x**2) + y)
        y = b1 * math.cos(y * (1 - x**2))
        x = x_next
    
    # 生成混沌序列
    for i in range(L_half):
        x_next = a1 * math.cos(math.exp(x**2) + y)
        y = b1 * math.cos(y * (1 - x**2))
        x = x_next
        
        # 按照论文公式转换为 0-255 整数
        xn[i] = math.floor(x * 10**15) % 256
        yn[i] = math.floor(x * 10**10) % 256
    
    # 序列拼接与变换
    K1 = np.empty(L, dtype=np.int64)
    K1[:L_half] = xn
    K1[L_half:] = yn
    
    K2 = (K1 + 1) % 256
    K3 = (256 - K1) % 256
    
    return K1, K2, K3


@njit
def arnold_diffusion_forward_original(P_flat, K1, K2, K3, a, b):
    """
    加密扩散过程 (原始版本)
    包含前向与后向两轮反馈
    """
    L = len(P_flat)
    C = np.zeros(L, dtype=np.int64)
    T = np.zeros(L, dtype=np.int64)
    
    # 第一轮：从左到右
    C[0] = (P_flat[0] + a * K1[0] + K2[0]) % 256
    T[0] = (b * P_flat[0] + (a * b + 1) * K1[0] + K3[0]) % 256
    
    for i in range(1, L):
        S_i = (T[i-1] + P_flat[i]) % 256
        C[i] = (S_i + a * K1[i] + K2[i]) % 256
        T[i] = (b * S_i + (a * b + 1) * K1[i] + K3[i]) % 256
    
    # 第二轮：从右到左
    C1 = np.zeros(L, dtype=np.int64)
    C1[L-1] = (C[L-1] + a * K1[0] + K2[0]) % 256
    T[L-1] = (b * C[L-1] + (a * b + 1) * K1[0] + K3[0]) % 256
    
    for i in range(L-2, -1, -1):
        idx = L - i - 1
        S_i = (T[i+1] + C[i]) % 256
        C1[i] = (S_i + a * K1[idx] + K2[idx]) % 256
        T[i] = (b * S_i + (a * b + 1) * K1[idx] + K3[idx]) % 256
    
    return C1


@njit
def arnold_diffusion_inverse_original(C1_flat, K1, K2, K3, a, b):
    """
    解密扩散过程 (原始版本)
    严格逆转前向与后向过程
    """
    L = len(C1_flat)
    C = np.zeros(L, dtype=np.int64)
    T = np.zeros(L, dtype=np.int64)
    
    # 逆转第二轮：从右到左
    C[L-1] = (C1_flat[L-1] - a * K1[0] - K2[0]) % 256
    T[L-1] = (b * C[L-1] + (a * b + 1) * K1[0] + K3[0]) % 256
    
    for i in range(L-2, -1, -1):
        idx = L - i - 1
        S_i = (C1_flat[i] - a * K1[idx] - K2[idx]) % 256
        C[i] = (S_i - T[i+1]) % 256
        T[i] = (b * S_i + (a * b + 1) * K1[idx] + K3[idx]) % 256
    
    # 逆转第一轮：从左到右
    P = np.zeros(L, dtype=np.int64)
    P[0] = (C[0] - a * K1[0] - K2[0]) % 256
    T[0] = (b * P[0] + (a * b + 1) * K1[0] + K3[0]) % 256
    
    for i in range(1, L):
        S_i = (C[i] - a * K1[i] - K2[i]) % 256
        P[i] = (S_i - T[i-1]) % 256
        T[i] = (b * S_i + (a * b + 1) * K1[i] + K3[i]) % 256
    
    return P


# =========================================================================
# 插件类 (原始版本)
# =========================================================================

class DPPAD_Encryptor_Original(BaseEncryptor):
    """
    DPPAD-IE 加密算法插件 (原始版本)
    适配系统：支持任意维度的图像 (H, W, C)
    """
    
    def __init__(self):
        super().__init__()
        self.name = "DPPAD-IE 算法 (原始版本)"
        
        self.default_key = {
            'x1': -0.8, 'r1': 0.9,
            'x3': -0.8, 'y3': -0.8,
            'a1': 25, 'b1': 20,
            'a': 15, 'b': 85
        }
    
    def _get_permutation_indices(self, L, x1, r1):
        """
        向量化实现基于混沌序列的置乱索引 (原始版本 - 纯Python)
        """
        seq = np.zeros(L, dtype=np.float64)
        x = x1
        
        # 预热
        for _ in range(1000):
            x = math.cos(r1 / math.asin(x))
        
        # 生成
        for i in range(L):
            x = math.cos(r1 / math.asin(x))
            seq[i] = x
        
        return np.argsort(seq)
    
    def encrypt(self, image_np: np.ndarray, key: dict) -> np.ndarray:
        """
        加密接口 (原始版本)
        """
        original_shape = image_np.shape
        P_flat = image_np.flatten().astype(np.int64)
        L = len(P_flat)
        
        # 置乱阶段
        perm_indices = self._get_permutation_indices(L, key['x1'], key['r1'])
        P_permuted = P_flat[perm_indices]
        
        # 扩散阶段
        K1, K2, K3 = generate_2d_cghm_original(key['x3'], key['y3'], key['a1'], key['b1'], L)
        C_flat = arnold_diffusion_forward_original(P_permuted, K1, K2, K3, key['a'], key['b'])
        
        cryptogram = C_flat.reshape(original_shape).astype(np.uint8)
        return cryptogram
    
    def decrypt(self, cryptogram_np: np.ndarray, key: dict) -> np.ndarray:
        """
        解密接口 (原始版本)
        """
        original_shape = cryptogram_np.shape
        C_flat = cryptogram_np.flatten().astype(np.int64)
        L = len(C_flat)
        
        # 逆扩散阶段
        K1, K2, K3 = generate_2d_cghm_original(key['x3'], key['y3'], key['a1'], key['b1'], L)
        P_permuted = arnold_diffusion_inverse_original(C_flat, K1, K2, K3, key['a'], key['b'])
        
        # 逆置乱阶段
        perm_indices = self._get_permutation_indices(L, key['x1'], key['r1'])
        P_flat = np.zeros_like(P_permuted)
        P_flat[perm_indices] = P_permuted
        
        decrypted_img = P_flat.reshape(original_shape).astype(np.uint8)
        return decrypted_img
