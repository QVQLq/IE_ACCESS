"""
DPPAD-Permutation-Only 消融算法
仅保留置乱阶段，去除扩散阶段
用于与完整 DPPAD-IE 算法进行对比消融实验
"""
import numpy as np
from core.base_encryptor import BaseEncryptor


class DPPAD_Permutation_Only(BaseEncryptor):
    """
    仅置乱版本的 DPPAD-IE 消融算法

    加密流程：明文 → 扁平化 → 全局混沌置乱 → 密文
    解密流程：密文 → 扁平化 → 全局混沌逆置乱 → 明文

    该算法仅使用 Logistic 混沌映射生成置乱索引，
    不涉及 2D-CGHM 序列生成和 Arnold 双向扩散。
    """

    def __init__(self):
        super().__init__()
        self.name = "DPPAD-Permutation-Only (仅置乱)"

        # 仅需置乱相关参数
        self.default_key = {
            'x1': -0.8,   # Logistic 映射初值
            'r1': 0.9     # Logistic 映射控制参数
        }

    def _get_permutation_indices(self, L: int, x1: float, r1: float) -> np.ndarray:
        """
        生成全局混沌置乱索引

        Args:
            L:        像素总数
            x1:       Logistic 映射初始值
            r1:       Logistic 映射控制参数

        Returns:
            置乱索引数组（np.argsort 结果）
        """
        seq = np.empty(L, dtype=np.float64)
        x = x1

        # 预热 1000 次，消除瞬态效应
        for _ in range(1000):
            x = np.cos(r1 / np.arcsin(x))

        # 生成混沌序列
        for i in range(L):
            x = np.cos(r1 / np.arcsin(x))
            seq[i] = x

        return np.argsort(seq)

    def encrypt(self, image_np: np.ndarray, key: dict) -> np.ndarray:
        """
        加密：仅执行置乱

        Args:
            image_np: 输入图像（任意形状 H, W 或 H, W, C）
            key:      密钥字典 {'x1': float, 'r1': float}

        Returns:
            置乱后的密文图像
        """
        original_shape = image_np.shape
        P_flat = image_np.flatten()
        L = len(P_flat)

        # 置乱阶段
        perm_indices = self._get_permutation_indices(L, key['x1'], key['r1'])
        C_flat = P_flat[perm_indices]

        return C_flat.reshape(original_shape).astype(np.uint8)

    def decrypt(self, cryptogram_np: np.ndarray, key: dict) -> np.ndarray:
        """
        解密：仅执行逆置乱

        Args:
            cryptogram_np: 密文图像
            key:           密钥字典

        Returns:
            还原后的明文图像
        """
        original_shape = cryptogram_np.shape
        C_flat = cryptogram_np.flatten()
        L = len(C_flat)

        # 逆置乱
        perm_indices = self._get_permutation_indices(L, key['x1'], key['r1'])
        P_flat = np.empty_like(C_flat)
        P_flat[perm_indices] = C_flat

        return P_flat.reshape(original_shape).astype(np.uint8)
