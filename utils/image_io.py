"""
图像IO工具
支持中文路径的图像读写
"""
import numpy as np
import cv2


def imread_chinese(filepath: str, flags=cv2.IMREAD_COLOR) -> np.ndarray:
    """
    读取图像（支持中文路径）
    
    Args:
        filepath: 图像文件路径
        flags: 读取标志（cv2.IMREAD_COLOR, cv2.IMREAD_GRAYSCALE等）
        
    Returns:
        图像数组，如果失败返回 None
    """
    try:
        # 读取文件为字节流
        with open(filepath, 'rb') as f:
            file_data = f.read()
        
        # 转换为 numpy 数组
        file_array = np.frombuffer(file_data, dtype=np.uint8)
        
        # 解码图像
        image = cv2.imdecode(file_array, flags)
        
        return image
    
    except Exception as e:
        print(f"读取图像失败 {filepath}: {e}")
        return None


def imwrite_chinese(filepath: str, image: np.ndarray) -> bool:
    """
    保存图像（支持中文路径）
    
    Args:
        filepath: 保存路径
        image: 图像数组
        
    Returns:
        是否成功
    """
    try:
        # 获取文件扩展名
        ext = filepath[filepath.rfind('.'):]
        
        # 编码图像
        success, encoded_image = cv2.imencode(ext, image)
        
        if success:
            # 写入文件
            with open(filepath, 'wb') as f:
                f.write(encoded_image.tobytes())
            return True
        else:
            return False
    
    except Exception as e:
        print(f"保存图像失败 {filepath}: {e}")
        return False
