# -*- coding: utf-8 -*-
"""
图像处理模块
"""
import numpy as np
from PIL import Image


class ImageProcessor:
    """图像处理器"""
    
    def load_image(self, file_path):
        """
        加载图像并转换为 numpy uint8 数组
        
        Args:
            file_path: 图像文件路径
            
        Returns:
            numpy.ndarray: 图像数组，灰度 (H,W) 或 RGB (H,W,3)
        """
        img = Image.open(file_path)
        
        # 根据图像模式进行转换
        if img.mode == 'L':
            # 灰度图像，保持灰度格式
            pass
        elif img.mode == 'RGBA':
            # RGBA 转 RGB
            img = img.convert('RGB')
        elif img.mode == 'RGB':
            # RGB 保持不变
            pass
        else:
            # 其他模式（如 P、1、CMYK 等）转为 RGB
            img = img.convert('RGB')
            
        # 转换为 numpy 数组
        img_array = np.array(img, dtype=np.uint8)
        
        return img_array
        
    def save_image(self, img_array, file_path):
        """
        保存图像数组为文件
        
        Args:
            img_array: numpy 图像数组
            file_path: 保存路径
        """
        img = Image.fromarray(img_array)
        img.save(file_path)
