"""
DPPAD-IE 加密算法
基于双向扩散和置乱的图像加密算法
"""
import numpy as np
import math
# Numba 库能将 Python 的 for 循环编译为机器码，解决纯 Python 加密速度慢的瓶颈。
# 如果尚未安装，请在终端运行: pip install numba
from numba import njit
from core.base_encryptor import BaseEncryptor


# =========================================================================
# 核心加速计算区 (使用 @njit 装饰器极大提升运行速度)
# =========================================================================

@njit(fastmath=True, cache=True)
def generate_2d_cghm(x3_init, y3_init, a1, b1, L):
    """
    利用 2D-CGHM 生成扩散所需的 K1, K2, K3 混沌序列
    对应 MATLAB 中 Function_anuode.m 的序列生成逻辑
    """
    L_half = L // 2
    xn = np.empty(L_half, dtype=np.float64)
    yn = np.empty(L_half, dtype=np.float64)
    
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
        
        # 按照论文公式转换为 0-255 整数，使用位运算加速
        xn[i] = int(math.floor(x * 10**15)) & 255
        yn[i] = int(math.floor(x * 10**10)) & 255
    
    # 序列拼接与变换
    K1 = np.empty(L, dtype=np.int64)
    K1[:L_half] = xn
    K1[L_half:] = yn
    
    K2 = (K1 + 1) & 255
    K3 = (256 - K1) & 255
    
    return K1, K2, K3


@njit(fastmath=True, cache=True)
def get_permutation_indices_fast(L, x1, r1):
    """
    改进版置乱索引生成：使用 Numba 加速混沌序列计算
    """
    seq = np.empty(L, dtype=np.float64)
    x = x1
    
    # 预热
    for _ in range(1000):
        x = math.cos(r1 / math.asin(x))
    
    # 生成
    for i in range(L):
        x = math.cos(r1 / math.asin(x))
        seq[i] = x
    
    return np.argsort(seq)


@njit(fastmath=True, cache=True)
def arnold_diffusion_forward(P_flat, K1, K2, K3, a, b):
    """
    改进版前向扩散：0内存浪费，位运算加速
    """
    L = len(P_flat)
    # 使用 empty 替代 zeros，因为我们马上会覆写所有位置
    C = np.empty(L, dtype=np.int64)
    ab1 = a * b + 1  # 提取循环不变量
    
    # ================= 第一轮：从左到右 =================
    C[0] = (P_flat[0] + a * K1[0] + K2[0]) & 255
    T_curr = (b * P_flat[0] + ab1 * K1[0] + K3[0]) & 255
    
    for i in range(1, L):
        S_i = (T_curr + P_flat[i]) & 255
        C[i] = (S_i + a * K1[i] + K2[i]) & 255
        T_curr = (b * S_i + ab1 * K1[i] + K3[i]) & 255
    
    # ================= 第二轮：从右到左 (原地覆写) =================
    C_last = C[L-1]
    # 原地覆写 C[L-1]，不再申请 C1 数组
    C[L-1] = (C_last + a * K1[0] + K2[0]) & 255
    T_curr = (b * C_last + ab1 * K1[0] + K3[0]) & 255
    
    for i in range(L-2, -1, -1):
        idx = L - i - 1
        S_i = (T_curr + C[i]) & 255
        # 计算下一步的 T_curr 时使用 S_i（S_i 依赖于被覆盖前的旧 C[i]）
        T_curr_next = (b * S_i + ab1 * K1[idx] + K3[idx]) & 255
        # 覆写现在的 C[i]
        C[i] = (S_i + a * K1[idx] + K2[idx]) & 255
        T_curr = T_curr_next
    
    return C


@njit(fastmath=True, cache=True)
def arnold_diffusion_inverse(C1_flat, K1, K2, K3, a, b):
    """
    改进版逆向扩散
    """
    L = len(C1_flat)
    C = np.empty(L, dtype=np.int64)
    ab1 = a * b + 1
    
    # ================= 逆转第二轮：从右到左 =================
    C[L-1] = (C1_flat[L-1] - a * K1[0] - K2[0]) & 255
    T_curr = (b * C[L-1] + ab1 * K1[0] + K3[0]) & 255
    
    for i in range(L-2, -1, -1):
        idx = L - i - 1
        S_i = (C1_flat[i] - a * K1[idx] - K2[idx]) & 255
        C[i] = (S_i - T_curr) & 255
        T_curr = (b * S_i + ab1 * K1[idx] + K3[idx]) & 255
    
    # ================= 逆转第一轮：从左到右 (原地覆写) =================
    C_0 = C[0]
    # 我们用 C 数组来直接存储还原后的明文 P，不单独申请 P 数组
    C[0] = (C_0 - a * K1[0] - K2[0]) & 255
    T_curr = (b * C[0] + ab1 * K1[0] + K3[0]) & 255
    
    for i in range(1, L):
        S_i = (C[i] - a * K1[i] - K2[i]) & 255
        C_i_old = C[i]  # 暂存原来的 C[i]
        C[i] = (S_i - T_curr) & 255  # 覆写为明文 P[i]
        T_curr = (b * S_i + ab1 * K1[i] + K3[i]) & 255
    
    return C


# =========================================================================
# 面向系统 UI 的插件类
# =========================================================================

class DPPAD_Encryptor_Ultra(BaseEncryptor):
    """
    DPPAD-IE 加密算法插件 (改进版)
    适配系统：支持任意维度的图像 (H, W, C)
    优化：Numba JIT + 位运算 + 内存优化
    """
    
    def __init__(self):
        super().__init__()
        self.name = "DPPAD-IE 改进版 (Ultra Optimized)"
        
        # 包含所有的混沌初始参数，以便 UI 系统能动态修改它们做密钥敏感性测试
        self.default_key = {
            'x1': -0.8, 'r1': 0.9,     # 扫描置乱参数 (当前版本简化为生成全局置乱索引)
            'x3': -0.8, 'y3': -0.8,    # 2D-CGHM 映射初值
            'a1': 25, 'b1': 20,        # 2D-CGHM 控制参数
            'a': 15, 'b': 85           # 阿诺德映射扩散系数
        }
    

    
    def encrypt(self, image_np: np.ndarray, key: dict) -> np.ndarray:
        """
        加密接口：被测评系统的 Evaluator 模块调用
        """
        # 1. 扁平化图像获取长度
        original_shape = image_np.shape
        P_flat = image_np.flatten().astype(np.int64)
        L = len(P_flat)
        
        # 2. 置乱阶段 (Permutation) - 使用改进版本
        perm_indices = get_permutation_indices_fast(L, key['x1'], key['r1'])
        P_permuted = P_flat[perm_indices]
        
        # 3. 扩散阶段 (Diffusion)
        K1, K2, K3 = generate_2d_cghm(key['x3'], key['y3'], key['a1'], key['b1'], L)
        C_flat = arnold_diffusion_forward(P_permuted, K1, K2, K3, key['a'], key['b'])
        
        # 4. 重组为原尺寸密文
        cryptogram = C_flat.reshape(original_shape).astype(np.uint8)
        return cryptogram
    
    def decrypt(self, cryptogram_np: np.ndarray, key: dict) -> np.ndarray:
        """
        解密接口：被测评系统的图像比对与还原模块调用
        """
        original_shape = cryptogram_np.shape
        C_flat = cryptogram_np.flatten().astype(np.int64)
        L = len(C_flat)
        
        # 1. 逆扩散阶段 (Inverse Diffusion)
        K1, K2, K3 = generate_2d_cghm(key['x3'], key['y3'], key['a1'], key['b1'], L)
        P_permuted = arnold_diffusion_inverse(C_flat, K1, K2, K3, key['a'], key['b'])
        
        # 2. 逆置乱阶段 (Inverse Permutation) - 使用改进版本
        perm_indices = get_permutation_indices_fast(L, key['x1'], key['r1'])
        
        # 恢复原位置：创建一个空数组，按原索引映射放回像素
        P_flat = np.empty_like(P_permuted)
        P_flat[perm_indices] = P_permuted
        
        # 3. 重组为明文图
        decrypted_img = P_flat.reshape(original_shape).astype(np.uint8)
        return decrypted_img
