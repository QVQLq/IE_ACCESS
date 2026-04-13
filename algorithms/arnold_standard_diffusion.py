"""
Arnold 标准扩散加密算法
使用 2D-CGHM 混沌序列 + 全局置乱 + 单轮链式 Arnold 扩散
作为 DPPAD-IE 改进版的对比基线算法
"""
import numpy as np
import math
from numba import njit
from core.base_encryptor import BaseEncryptor
from algorithms.dppad_encryptor_ultra import (
    generate_2d_cghm,
    get_permutation_indices_fast
)


# =========================================================================
# 普通 Arnold 扩散函数（使用 @njit 装饰器加速）
# =========================================================================

@njit(fastmath=True, cache=True)
def arnold_standard_forward(P_flat, K1):
    """
    单轮链式 Arnold 扩散（前向）

    公式: C[i] = (P[i] + K1[i] + C[i-1]) mod 256
    其中 C[-1] = 0

    仅依赖 K1 序列，链式传播使单个像素变化影响所有后续密文。
    """
    L = len(P_flat)
    C = np.empty(L, dtype=np.int64)
    C[0] = (int(P_flat[0]) + int(K1[0])) & 255

    for i in range(1, L):
        C[i] = (int(P_flat[i]) + int(K1[i]) + C[i - 1]) & 255

    return C


@njit(fastmath=True, cache=True)
def arnold_standard_inverse(C_flat, K1):
    """
    单轮链式 Arnold 扩散（逆向）

    公式: P[i] = (C[i] - K1[i] - C[i-1]) mod 256
    其中 C[-1] = 0
    """
    L = len(C_flat)
    P = np.empty(L, dtype=np.int64)
    P[0] = (int(C_flat[0]) - int(K1[0])) & 255

    for i in range(1, L):
        P[i] = (int(C_flat[i]) - int(K1[i]) - C_flat[i - 1]) & 255

    return P


# =========================================================================
# 插件类
# =========================================================================

class Arnold_Standard_Encryptor(BaseEncryptor):
    """
    Arnold 标准扩散加密器

    加密流程: 明文 → 全局置乱 → 单轮链式 Arnold 扩散 → 密文
    解密流程: 密文 → 单轮链式 Arnold 逆向扩散 → 逆置乱 → 明文

    对比说明:
    - 与 DPPAD-IE 改进版相比，此算法仅使用单轮链式扩散（无双向双轮耦合）
    - 保留了 2D-CGHM 混沌序列生成和全局置乱的核心框架
    - 算法结构简洁、可逆，适合作为扩散效果的对比基线
    """

    def __init__(self):
        super().__init__()
        self.name = "Arnold 标准扩散"

        self.default_key = {
            'x1': -0.8, 'r1': 0.9,     # 全局置乱参数
            'x3': -0.8, 'y3': -0.8,    # 2D-CGHM 映射初值
            'a1': 25, 'b1': 20         # 2D-CGHM 控制参数
        }

    def encrypt(self, image_np: np.ndarray, key: dict) -> np.ndarray:
        """
        加密接口

        Args:
            image_np: 输入图像（任意形状 H, W 或 H, W, C）
            key:      密钥字典

        Returns:
            加密后的密文图像
        """
        original_shape = image_np.shape
        P_flat = image_np.flatten().astype(np.int64)
        L = len(P_flat)

        # 阶段1: 全局置乱
        perm_indices = get_permutation_indices_fast(L, key['x1'], key['r1'])
        P_permuted = P_flat[perm_indices]

        # 阶段2: 单轮链式 Arnold 扩散
        K1, _, _ = generate_2d_cghm(key['x3'], key['y3'], key['a1'], key['b1'], L)
        C_flat = arnold_standard_forward(P_permuted, K1)

        return C_flat.reshape(original_shape).astype(np.uint8)

    def decrypt(self, cryptogram_np: np.ndarray, key: dict) -> np.ndarray:
        """
        解密接口

        Args:
            cryptogram_np: 密文图像
            key:           密钥字典

        Returns:
            还原后的明文图像
        """
        original_shape = cryptogram_np.shape
        C_flat = cryptogram_np.flatten().astype(np.int64)
        L = len(C_flat)

        # 阶段1: 单轮链式 Arnold 逆向扩散
        K1, _, _ = generate_2d_cghm(key['x3'], key['y3'], key['a1'], key['b1'], L)
        P_permuted = arnold_standard_inverse(C_flat, K1)

        # 阶段2: 逆置乱
        perm_indices = get_permutation_indices_fast(L, key['x1'], key['r1'])
        P_flat = np.empty_like(P_permuted)
        P_flat[perm_indices] = P_permuted

        return P_flat.reshape(original_shape).astype(np.uint8)
