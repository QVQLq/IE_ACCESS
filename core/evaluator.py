# -*- coding: utf-8 -*-
"""
测评模块
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')  # 使用 Agg 后端，不显示窗口
import matplotlib.pyplot as plt
from pathlib import Path


class EvaluationEngine:
    """测评引擎"""
    
    def run(self, plain, cipher, params, settings=None):
        """
        运行测评
        
        Args:
            plain: 明文图像
            cipher: 密文图像
            params: 加密参数
            settings: 测评设置（可选）
            
        Returns:
            dict: 测评指标（包含 eval_time_ms）
        """
        import time
        start_time = time.time()
        
        output_dir = Path(params.get("output_dir", "outputs"))
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # 获取采样数 K
        corr_sample_k = params.get("corr_sample_k", 5000)
        
        # 生成直方图
        self.generate_histogram(plain, output_dir / "hist_plain.png")
        self.generate_histogram(cipher, output_dir / "hist_cipher.png")
        
        # 计算信息熵
        entropy_cipher = self.calculate_entropy(cipher)
        
        # 计算相邻像素相关性（RGB 转灰度处理）
        plain_gray = self.to_grayscale(plain)
        cipher_gray = self.to_grayscale(cipher)
        
        corr_plain = self.calculate_correlation(plain_gray, corr_sample_k, output_dir, "plain")
        corr_cipher = self.calculate_correlation(cipher_gray, corr_sample_k, output_dir, "cipher")
        
        # 计算 NPCR 和 UACI（明文敏感性）
        npcr_uaci_result = self.calculate_npcr_uaci(plain, cipher, params)
        
        end_time = time.time()
        eval_time_ms = (end_time - start_time) * 1000
        
        metrics = {
            "entropy_cipher": round(entropy_cipher, 6),
            "corr_plain": {
                "H": round(corr_plain["H"], 6),
                "V": round(corr_plain["V"], 6),
                "D": round(corr_plain["D"], 6)
            },
            "corr_cipher": {
                "H": round(corr_cipher["H"], 6),
                "V": round(corr_cipher["V"], 6),
                "D": round(corr_cipher["D"], 6)
            },
            "npcr": round(npcr_uaci_result["npcr"], 4),
            "uaci": round(npcr_uaci_result["uaci"], 4),
            "perturbation": npcr_uaci_result["perturbation"],
            "eval_time_ms": round(eval_time_ms, 2)
        }
        
        return metrics
    
    def to_grayscale(self, image):
        """
        将图像转换为灰度图
        
        Args:
            image: 图像数组 (H,W) 或 (H,W,3)
            
        Returns:
            numpy.ndarray: 灰度图像 (H,W)
        """
        if len(image.shape) == 2:
            # 已经是灰度图
            return image
        elif len(image.shape) == 3 and image.shape[2] == 3:
            # RGB 转灰度：使用标准权重 0.299*R + 0.587*G + 0.114*B
            gray = (0.299 * image[:, :, 0] + 
                   0.587 * image[:, :, 1] + 
                   0.114 * image[:, :, 2])
            return gray.astype(np.uint8)
        else:
            return image
    
    def calculate_correlation(self, image, k, output_dir, prefix):
        """
        计算相邻像素相关性并生成散点图
        
        Args:
            image: 灰度图像 (H,W)
            k: 采样对数
            output_dir: 输出目录
            prefix: 文件名前缀 ("plain" 或 "cipher")
            
        Returns:
            dict: {"H": r_h, "V": r_v, "D": r_d}
        """
        h, w = image.shape
        
        # 采样 K 对相邻像素
        directions = {
            "H": self.sample_pairs(image, k, direction="H"),  # 水平
            "V": self.sample_pairs(image, k, direction="V"),  # 垂直
            "D": self.sample_pairs(image, k, direction="D")   # 对角
        }
        
        results = {}
        
        for direction, (X, Y) in directions.items():
            # 计算皮尔逊相关系数
            r = self.pearson_correlation(X, Y)
            results[direction] = r
            
            # 生成散点图
            output_path = output_dir / f"corr_{prefix}_{direction}.png"
            self.plot_correlation(X, Y, r, direction, output_path)
        
        return results
    
    def sample_pairs(self, image, k, direction):
        """
        采样相邻像素对
        
        Args:
            image: 灰度图像 (H,W)
            k: 采样对数
            direction: "H" (水平), "V" (垂直), "D" (对角)
            
        Returns:
            tuple: (X, Y) 两个长度为 k 的数组
        """
        h, w = image.shape
        X = []
        Y = []
        
        # 根据方向确定有效采样范围
        if direction == "H":
            # 水平：(x,y) 与 (x,y+1)
            valid_positions = [(i, j) for i in range(h) for j in range(w - 1)]
        elif direction == "V":
            # 垂直：(x,y) 与 (x+1,y)
            valid_positions = [(i, j) for i in range(h - 1) for j in range(w)]
        elif direction == "D":
            # 对角：(x,y) 与 (x+1,y+1)
            valid_positions = [(i, j) for i in range(h - 1) for j in range(w - 1)]
        else:
            raise ValueError(f"Unknown direction: {direction}")
        
        # 随机采样 k 对
        if len(valid_positions) < k:
            k = len(valid_positions)
        
        rng = np.random.RandomState(42)  # 固定种子确保可复现
        sampled_indices = rng.choice(len(valid_positions), size=k, replace=False)
        
        for idx in sampled_indices:
            i, j = valid_positions[idx]
            
            if direction == "H":
                X.append(image[i, j])
                Y.append(image[i, j + 1])
            elif direction == "V":
                X.append(image[i, j])
                Y.append(image[i + 1, j])
            elif direction == "D":
                X.append(image[i, j])
                Y.append(image[i + 1, j + 1])
        
        return np.array(X, dtype=np.float64), np.array(Y, dtype=np.float64)
    
    def pearson_correlation(self, X, Y):
        """
        计算皮尔逊相关系数
        
        Args:
            X: 数组
            Y: 数组
            
        Returns:
            float: 相关系数 r
        """
        if len(X) == 0 or len(Y) == 0:
            return 0.0
        
        mean_x = np.mean(X)
        mean_y = np.mean(Y)
        
        numerator = np.sum((X - mean_x) * (Y - mean_y))
        denominator = np.sqrt(np.sum((X - mean_x) ** 2) * np.sum((Y - mean_y) ** 2))
        
        if denominator == 0:
            return 0.0
        
        r = numerator / denominator
        return r
    
    def plot_correlation(self, X, Y, r, direction, output_path):
        """
        绘制相关性散点图
        
        Args:
            X: 横轴数据
            Y: 纵轴数据
            r: 相关系数
            direction: 方向标签
            output_path: 输出路径
        """
        plt.figure(figsize=(6, 6))
        plt.scatter(X, Y, s=1, alpha=0.5, c='blue')
        plt.xlabel('Pixel Value at Position (x,y)')
        plt.ylabel(f'Pixel Value at Adjacent Position ({direction})')
        plt.title(f'Correlation in {direction} Direction (r = {r:.6f})')
        plt.xlim([0, 255])
        plt.ylim([0, 255])
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(output_path, dpi=100, bbox_inches='tight')
        plt.close()
    
    def generate_histogram(self, image, output_path):
        """
        生成图像直方图
        
        Args:
            image: 图像数组 (H,W) 或 (H,W,3)
            output_path: 输出文件路径
        """
        plt.figure(figsize=(10, 6))
        
        if len(image.shape) == 2:
            # 灰度图像
            hist, bins = np.histogram(image.flatten(), bins=256, range=(0, 256))
            plt.bar(range(256), hist, width=1.0, color='gray', edgecolor='gray')
            plt.title('Grayscale Histogram')
            plt.xlabel('Pixel Value')
            plt.ylabel('Frequency')
            plt.xlim([0, 255])
            plt.grid(axis='y', alpha=0.3)
            
        elif len(image.shape) == 3 and image.shape[2] == 3:
            # RGB 图像：三个子图
            colors = ['red', 'green', 'blue']
            channel_names = ['Red', 'Green', 'Blue']
            
            for i in range(3):
                plt.subplot(3, 1, i + 1)
                channel_data = image[:, :, i].flatten()
                hist, bins = np.histogram(channel_data, bins=256, range=(0, 256))
                plt.bar(range(256), hist, width=1.0, color=colors[i], edgecolor=colors[i], alpha=0.7)
                plt.title(f'{channel_names[i]} Channel Histogram')
                plt.xlabel('Pixel Value')
                plt.ylabel('Frequency')
                plt.xlim([0, 255])
                plt.grid(axis='y', alpha=0.3)
            
            plt.tight_layout()
        
        plt.savefig(output_path, dpi=100, bbox_inches='tight')
        plt.close()
    
    def calculate_entropy(self, image):
        """
        计算图像的 Shannon 熵
        
        Args:
            image: 图像数组
            
        Returns:
            float: 信息熵值
        """
        # 将图像展平为一维数组
        flat_image = image.flatten()
        
        # 统计每个像素值的频次
        hist, _ = np.histogram(flat_image, bins=256, range=(0, 256))
        
        # 计算概率分布
        total_pixels = flat_image.size
        probabilities = hist / total_pixels
        
        # 计算熵：H = -sum(p_i * log2(p_i))，跳过 p_i = 0
        entropy = 0.0
        for p in probabilities:
            if p > 0:
                entropy -= p * np.log2(p)
        
        return entropy


    
    def calculate_npcr_uaci(self, plain, cipher, params):
        """
        计算 NPCR 和 UACI（明文敏感性评测）
        
        Args:
            plain: 明文图像
            cipher: 密文图像
            params: 加密参数（包含 seed）
            
        Returns:
            dict: {"npcr": float, "uaci": float, "perturbation": dict}
        """
        from core.encryptor import CipherEngine
        
        # 使用 seed + 999 确保可复现的扰动
        seed = params.get("seed", 42)
        rng = np.random.default_rng(seed + 999)
        
        # 创建扰动后的明文
        plain2 = plain.copy()
        perturbation_info = {}
        
        if len(plain.shape) == 2:
            # 灰度图像：随机选择 (x, y)
            h, w = plain.shape
            x = rng.integers(0, h)
            y = rng.integers(0, w)
            
            original_value = int(plain[x, y])
            new_value = int((int(plain[x, y]) + 1) % 256)
            plain2[x, y] = np.uint8(new_value)
            
            perturbation_info = {
                "type": "grayscale",
                "position": [int(x), int(y)],
                "original_value": original_value,
                "new_value": new_value,
                "rule": "plain2[x,y] = (plain[x,y] + 1) % 256"
            }
            
        elif len(plain.shape) == 3 and plain.shape[2] == 3:
            # RGB 图像：随机选择 (x, y, c)
            h, w, c = plain.shape
            x = rng.integers(0, h)
            y = rng.integers(0, w)
            channel = rng.integers(0, c)
            
            original_value = int(plain[x, y, channel])
            new_value = int((int(plain[x, y, channel]) + 1) % 256)
            plain2[x, y, channel] = np.uint8(new_value)
            
            channel_names = ['R', 'G', 'B']
            perturbation_info = {
                "type": "RGB",
                "position": [int(x), int(y), int(channel)],
                "channel": channel_names[channel],
                "original_value": original_value,
                "new_value": new_value,
                "rule": f"plain2[x,y,{channel_names[channel]}] = (plain[x,y,{channel_names[channel]}] + 1) % 256"
            }
        
        # 使用相同参数加密扰动后的明文
        cipher_engine = CipherEngine()
        cipher2 = cipher_engine.encrypt(plain2, params)
        
        # 计算 NPCR（不同像素占比）
        # 将图像展平为一维数组进行比较
        cipher_flat = cipher.flatten()
        cipher2_flat = cipher2.flatten()
        
        diff_pixels = np.sum(cipher_flat != cipher2_flat)
        total_pixels = cipher_flat.size
        npcr = (diff_pixels / total_pixels) * 100.0  # 百分比
        
        # 计算 UACI（平均强度变化）
        # UACI = (1/T) * Σ|cipher[i] - cipher2[i]| / 255 * 100%
        # 其中 T 是总像素数
        intensity_diff = np.abs(cipher_flat.astype(np.float64) - cipher2_flat.astype(np.float64))
        uaci = (np.sum(intensity_diff) / total_pixels / 255.0) * 100.0  # 百分比
        
        return {
            "npcr": npcr,
            "uaci": uaci,
            "perturbation": perturbation_info
        }


class Evaluator:
    """图像加密测评器（封装 EvaluationEngine）"""
    
    def __init__(self):
        self.eval_engine = EvaluationEngine()
    
    def evaluate(self, plain_image, cipher_image, enc_time_ms, image_path, params):
        """
        生成完整测评结果
        
        Args:
            plain_image: 明文图像
            cipher_image: 密文图像
            enc_time_ms: 加密耗时（毫秒）
            image_path: 原始图像路径
            params: 加密参数
            
        Returns:
            dict: 测评结果
        """
        # 调用 EvaluationEngine 获取测评指标
        metrics = self.eval_engine.run(plain_image, cipher_image, params, settings=None)
        
        # 提取 perturbation 和 eval_time_ms 信息
        perturbation = metrics.pop("perturbation", None)
        eval_time_ms = metrics.pop("eval_time_ms", 0)
        
        # 组装完整结果
        results = {
            "enc_time_ms": round(enc_time_ms, 2),
            "eval_time_ms": round(eval_time_ms, 2),
            **metrics,  # 展开测评指标
            "meta": {
                "image_path": image_path,
                "image_shape": list(plain_image.shape),
                "params": params,
                "perturbation": perturbation
            }
        }
        
        return results
