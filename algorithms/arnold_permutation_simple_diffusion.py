"""
Arnold 置乱 + 简单扩散
经典基础基线算法
前半部分: 经典二维 Arnold Cat Map 置乱
后半部分: 单轮链式模加扩散
"""
import numpy as np
from numba import njit
from core.base_encryptor import BaseEncryptor
from algorithms.dppad_encryptor_ultra import generate_2d_cghm


# =========================================================================
# Arnold 置乱
# =========================================================================

def arnold_transform(image: np.ndarray, a: int, b: int, c: int, d: int) -> np.ndarray:
    """
    单轮 Arnold Cat Map 变换

    变换矩阵 A = [[a, b], [c, d]]，要求 ad - bc = 1
    [x', y'] = A @ [x, y] mod [H, W]
    """
    H, W = image.shape[:2]
    result = np.empty_like(image)

    for y in range(H):
        for x in range(W):
            new_x = (a * x + b * y) % W
            new_y = (c * x + d * y) % H
            result[new_y, new_x] = image[y, x]

    return result


def arnold_inverse_transform(image: np.ndarray, a: int, b: int, c: int, d: int) -> np.ndarray:
    """
    Arnold Cat Map 逆变换

    逆矩阵 A_inv = [[d, -b], [-c, a]] mod [H, W]
    由于 det(A)=1，逆矩阵元素为整数
    """
    H, W = image.shape[:2]
    result = np.empty_like(image)

    for y in range(H):
        for x in range(W):
            new_x = (d * x - b * y) % W
            new_y = (-c * x + a * y) % H
            result[new_y, new_x] = image[y, x]

    return result


def arnold_n_rounds(image: np.ndarray, a: int, b: int, c: int, d: int, n: int) -> np.ndarray:
    """执行 n 轮 Arnold 置乱"""
    result = image.copy()
    for _ in range(n):
        result = arnold_transform(result, a, b, c, d)
    return result


def arnold_n_rounds_inverse(image: np.ndarray, a: int, b: int, c: int, d: int, n: int) -> np.ndarray:
    """执行 n 轮 Arnold 逆置乱"""
    result = image.copy()
    for _ in range(n):
        result = arnold_inverse_transform(result, a, b, c, d)
    return result


# =========================================================================
# 简单链式扩散 (numba 加速)
# =========================================================================

@njit(fastmath=True, cache=True)
def simple_chain_diffusion_forward(P_flat: np.ndarray, K1: np.ndarray) -> np.ndarray:
    """
    单轮链式扩散（前向）

    C[i] = (P[i] + K1[i] + C[i-1]) mod 256
    C[-1] = 0
    """
    L = len(P_flat)
    C = np.empty(L, dtype=np.int64)
    C[0] = (int(P_flat[0]) + int(K1[0])) & 255

    for i in range(1, L):
        C[i] = (int(P_flat[i]) + int(K1[i]) + C[i - 1]) & 255

    return C


@njit(fastmath=True, cache=True)
def simple_chain_diffusion_inverse(C_flat: np.ndarray, K1: np.ndarray) -> np.ndarray:
    """
    单轮链式扩散（逆向）

    P[i] = (C[i] - K1[i] - C[i-1]) mod 256
    C[-1] = 0
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

class Arnold_Permutation_Simple_Encryptor(BaseEncryptor):
    """
    Arnold 置乱 + 简单扩散

    加密流程: 明文 → Arnold 置乱(n轮) → 单轮链式扩散 → 密文
    解密流程: 密文 → 单轮链式逆向扩散 → Arnold 逆置乱(n轮) → 明文

    定位: 经典基础基线算法
    - 仅使用经典二维 Arnold Cat Map，无复杂 T 状态
    - 仅使用单轮链式扩散，无 K1/K2/K3 三重耦合
    - 无双向双轮改进结构
    - 结构明显比 DPPAD-IE 更基础、更简单
    """

    def __init__(self):
        super().__init__()
        self.name = "Arnold 置乱+简单扩散"

        self.default_key = {
            # Arnold 置乱参数 (ad-bc=1)
            'a': 1, 'b': 1, 'c': 1, 'd': 2, 'n': 3,
            # 2D-CGHM 参数（用于扩散序列）
            'x3': -0.8, 'y3': -0.8, 'a1': 25, 'b1': 20
        }

    def encrypt(self, image_np: np.ndarray, key: dict) -> np.ndarray:
        H, W = image_np.shape[:2]
        shape = image_np.shape

        # 分通道处理（灰度）或整体处理
        if len(shape) == 3 and shape[2] > 1:
            # 彩色图像：逐通道 Arnold + 扩散
            channels = []
            for ch in range(shape[2]):
                channel = image_np[:, :, ch]

                # Arnold 置乱
                permuted = arnold_n_rounds(
                    channel, key['a'], key['b'], key['c'], key['d'], key['n'])

                # 链式扩散
                L = permuted.size
                K1, _, _ = generate_2d_cghm(key['x3'], key['y3'], key['a1'], key['b1'], L)
                diffused = simple_chain_diffusion_forward(
                    permuted.flatten().astype(np.int64), K1)
                channels.append(diffused.reshape(H, W).astype(np.uint8))

            encrypted = np.stack(channels, axis=2)
        else:
            # 灰度图像
            # 阶段1: Arnold 置乱
            permuted = arnold_n_rounds(
                image_np, key['a'], key['b'], key['c'], key['d'], key['n'])

            # 阶段2: 链式扩散
            L = image_np.size
            K1, _, _ = generate_2d_cghm(key['x3'], key['y3'], key['a1'], key['b1'], L)
            encrypted = simple_chain_diffusion_forward(
                permuted.flatten().astype(np.int64), K1)
            encrypted = encrypted.reshape(shape).astype(np.uint8)

        return encrypted

    def decrypt(self, cryptogram_np: np.ndarray, key: dict) -> np.ndarray:
        H, W = cryptogram_np.shape[:2]
        shape = cryptogram_np.shape

        if len(shape) == 3 and shape[2] > 1:
            channels = []
            for ch in range(shape[2]):
                channel = cryptogram_np[:, :, ch]

                # 链式逆向扩散
                L = channel.size
                K1, _, _ = generate_2d_cghm(key['x3'], key['y3'], key['a1'], key['b1'], L)
                restored = simple_chain_diffusion_inverse(
                    channel.flatten().astype(np.int64), K1)
                restored = restored.reshape(H, W).astype(np.uint8)

                # Arnold 逆置乱
                restored = arnold_n_rounds_inverse(
                    restored, key['a'], key['b'], key['c'], key['d'], key['n'])
                channels.append(restored)

            decrypted = np.stack(channels, axis=2)
        else:
            # 链式逆向扩散
            L = cryptogram_np.size
            K1, _, _ = generate_2d_cghm(key['x3'], key['y3'], key['a1'], key['b1'], L)
            restored = simple_chain_diffusion_inverse(
                cryptogram_np.flatten().astype(np.int64), K1)

            # Arnold 逆置乱
            restored = restored.reshape(shape).astype(np.uint8)
            decrypted = arnold_n_rounds_inverse(
                restored, key['a'], key['b'], key['c'], key['d'], key['n'])

        return decrypted
