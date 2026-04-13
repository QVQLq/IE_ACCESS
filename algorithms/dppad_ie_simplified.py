"""
DPPAD-IE 简化密钥序列版
仅将 2D-CGHM 混沌序列替换为最简单的一维 Logistic Map，其余结构完全保留。
用于与完整 DPPAD-IE 对比，评估复杂混沌系统与简单密钥序列的差异。
"""
import numpy as np
import math
from numba import njit
from core.base_encryptor import BaseEncryptor

# 从 DPPAD-IE 完整版直接复用置乱和扩散的核心 numba 函数
from algorithms.dppad_encryptor_ultra import (
    get_permutation_indices_fast,
    arnold_diffusion_forward,
    arnold_diffusion_inverse,
)


# =========================================================================
# 替换: 用一维 Logistic Map 替代 2D-CGHM
# =========================================================================

@njit(fastmath=True, cache=True)
def generate_logistic_sequences(x_init: float, r: float, L: int) -> tuple:
    """
    最简单的一维 Logistic Map 生成 K1, K2, K3

    x_{n+1} = r * x_n * (1 - x_n)

    仅需 1 个初始值 + 1 个控制参数，与 2D-CGHM 的 4 参数形成对比。

    输出与 generate_2d_cghm 格式完全一致，保证接口兼容。
    """
    K1 = np.empty(L, dtype=np.int64)
    x = x_init

    # 预热，消除瞬态效应
    for _ in range(1000):
        x = r * x * (1 - x)

    # 生成序列，映射到 0-255
    for i in range(L):
        x = r * x * (1 - x)
        K1[i] = int(math.floor(x * 10**15)) & 255

    # K2, K3 与 DPPAD-IE 一致
    K2 = (K1 + 1) & 255
    K3 = (256 - K1) & 255

    return K1, K2, K3


# =========================================================================
# 插件类
# =========================================================================

class DPPAD_IE_Simplified_Encryptor(BaseEncryptor):
    """
    DPPAD-IE 简化密钥序列版

    加密流程: 明文 → Logistic Map 置乱 → Logistic Map 扩散 → 密文
    解密流程: 密文 → Logistic Map 逆扩散 → Logistic Map 逆置乱 → 明文

    定位: 与完整 DPPAD-IE 对比，评估复杂混沌 vs 简单密钥序列的差异
    """

    def __init__(self):
        super().__init__()
        self.name = "DPPAD-IE 简化密钥序列版"

        self.default_key = {
            # 置乱参数 (复用 DPPAD-IE 的 get_permutation_indices_fast)
            'x1': -0.8, 'r1': 0.9,
            # Logistic Map 参数 (替换 2D-CGHM)
            'x_init': 0.5, 'r': 3.9,
            # Arnold 扩散系数 (与 DPPAD-IE 一致)
            'a': 15, 'b': 85,
        }

    def encrypt(self, image_np: np.ndarray, key: dict) -> np.ndarray:
        original_shape = image_np.shape
        P_flat = image_np.flatten().astype(np.int64)
        L = len(P_flat)

        # 1. 置乱
        perm_indices = get_permutation_indices_fast(L, key['x1'], key['r1'])
        P_permuted = P_flat[perm_indices]

        # 2. 扩散 (Logistic Map 生成 K1/K2/K3)
        K1, K2, K3 = generate_logistic_sequences(key['x_init'], key['r'], L)
        C_flat = arnold_diffusion_forward(P_permuted, K1, K2, K3, key['a'], key['b'])

        # 3. 重组
        return C_flat.reshape(original_shape).astype(np.uint8)

    def decrypt(self, cryptogram_np: np.ndarray, key: dict) -> np.ndarray:
        original_shape = cryptogram_np.shape
        C_flat = cryptogram_np.flatten().astype(np.int64)
        L = len(C_flat)

        # 1. 逆扩散
        K1, K2, K3 = generate_logistic_sequences(key['x_init'], key['r'], L)
        P_permuted = arnold_diffusion_inverse(C_flat, K1, K2, K3, key['a'], key['b'])

        # 2. 逆置乱
        perm_indices = get_permutation_indices_fast(L, key['x1'], key['r1'])
        P_flat = np.empty_like(P_permuted)
        P_flat[perm_indices] = P_permuted

        # 3. 重组
        return P_flat.reshape(original_shape).astype(np.uint8)
