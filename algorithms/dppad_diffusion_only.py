"""
DPPAD-Diffusion-Only 消融算法
仅保留 Arnold 扩散阶段，去除置乱阶段
用于与完整 DPPAD-IE 算法进行对比消融实验
"""
import numpy as np
from core.base_encryptor import BaseEncryptor
from algorithms.dppad_encryptor_ultra import (
    generate_2d_cghm,
    arnold_diffusion_forward,
    arnold_diffusion_inverse
)


class DPPAD_Diffusion_Only(BaseEncryptor):
    """
    仅扩散版本的 DPPAD-IE 消融算法

    加密流程：明文 → 扁平化 → Arnold 双向扩散 → 密文
    解密流程：密文 → 扁平化 → Arnold 逆向扩散 → 明文

    该算法仅使用 2D-CGHM + Arnold 双向反馈扩散，
    不涉及 Logistic 混沌置乱。
    """

    def __init__(self):
        super().__init__()
        self.name = "DPPAD-Diffusion-Only (仅扩散)"

        # 仅需扩散相关参数（不需要置乱的 x1, r1）
        self.default_key = {
            'x3': -0.8, 'y3': -0.8,   # 2D-CGHM 映射初值
            'a1': 25, 'b1': 20,        # 2D-CGHM 控制参数
            'a': 15, 'b': 85           # Arnold 扩散系数
        }

    def encrypt(self, image_np: np.ndarray, key: dict) -> np.ndarray:
        """
        加密：仅执行 Arnold 双向扩散

        Args:
            image_np: 输入图像（任意形状 H, W 或 H, W, C）
            key:      密钥字典
                - x3, y3:  2D-CGHM 初值
                - a1, b1:  2D-CGHM 控制参数
                - a, b:    Arnold 扩散系数

        Returns:
            扩散后的密文图像
        """
        original_shape = image_np.shape
        P_flat = image_np.flatten().astype(np.int64)
        L = len(P_flat)

        # 扩散阶段
        K1, K2, K3 = generate_2d_cghm(
            key['x3'], key['y3'],
            key['a1'], key['b1'],
            L
        )
        C_flat = arnold_diffusion_forward(P_flat, K1, K2, K3, key['a'], key['b'])

        return C_flat.reshape(original_shape).astype(np.uint8)

    def decrypt(self, cryptogram_np: np.ndarray, key: dict) -> np.ndarray:
        """
        解密：仅执行 Arnold 逆向扩散

        Args:
            cryptogram_np: 密文图像
            key:           密钥字典

        Returns:
            还原后的明文图像
        """
        original_shape = cryptogram_np.shape
        C_flat = cryptogram_np.flatten().astype(np.int64)
        L = len(C_flat)

        # 逆扩散阶段
        K1, K2, K3 = generate_2d_cghm(
            key['x3'], key['y3'],
            key['a1'], key['b1'],
            L
        )
        P_flat = arnold_diffusion_inverse(C_flat, K1, K2, K3, key['a'], key['b'])

        return P_flat.reshape(original_shape).astype(np.uint8)
