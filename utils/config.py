# -*- coding: utf-8 -*-
"""
配置管理模块
"""
import json
import hashlib
import numpy as np

# 默认参数
DEFAULT_PARAMS = {
    "seed": 42,
    "rounds": 10,
    "corr_sample_k": 5000,
    "npcr_mode": "single_pixel_plus1",
    "output_dir": "outputs",
    "show_cipher_md5": True  # 是否在日志中显示密文 MD5
}


def save_config(params, file_path):
    """
    保存配置到 JSON 文件
    
    Args:
        params: 参数字典
        file_path: 保存路径
    """
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(params, f, indent=2, ensure_ascii=False)


def load_config(file_path):
    """
    从 JSON 文件加载配置
    
    Args:
        file_path: 配置文件路径
        
    Returns:
        dict: 参数字典
    """
    with open(file_path, "r", encoding="utf-8") as f:
        params = json.load(f)
    return params


def compute_md5(image_array):
    """
    计算图像数组的 MD5 哈希值
    
    Args:
        image_array: numpy 数组
        
    Returns:
        str: MD5 哈希值（十六进制字符串）
    """
    # 将 numpy 数组转换为字节流
    image_bytes = image_array.tobytes()
    md5_hash = hashlib.md5(image_bytes).hexdigest()
    return md5_hash
