"""
图像加密评估器
提供全面的量化分析指标
"""
import numpy as np
import time
import tracemalloc
from typing import Dict, Any, Tuple, Optional, Callable
from scipy.stats import chi2_contingency


class Evaluator:
    """
    图像加密评估器
    提供统计学指标、安全指标、敏感性测试和性能指标
    """
    
    # ==================== 统计学指标 ====================
    
    @staticmethod
    def calculate_entropy(image: np.ndarray, channel: Optional[int] = None) -> float:
        """
        计算信息熵
        
        Args:
            image: 输入图像 (H, W) 或 (H, W, C)
            channel: 指定通道，None表示计算整体熵
            
        Returns:
            信息熵值 (bits)
        """
        if image is None or image.size == 0:
            raise ValueError("图像不能为空")
        
        # 处理多通道图像
        if len(image.shape) == 3 and channel is not None:
            if channel >= image.shape[2]:
                raise ValueError(f"通道索引 {channel} 超出范围")
            image = image[:, :, channel]
        
        # 展平图像
        flat_image = image.flatten()
        
        # 计算直方图
        hist, _ = np.histogram(flat_image, bins=256, range=(0, 256))
        
        # 归一化为概率分布
        prob = hist / hist.sum()
        
        # 移除零概率
        prob = prob[prob > 0]
        
        # 计算熵
        entropy = -np.sum(prob * np.log2(prob))
        
        return float(entropy)

    
    @staticmethod
    def calculate_entropy_all_channels(image: np.ndarray) -> Dict[str, float]:
        """
        计算所有通道的信息熵
        
        Args:
            image: 输入图像
            
        Returns:
            包含各通道熵值的字典
        """
        result = {}
        
        if len(image.shape) == 2:
            # 灰度图像
            result['entropy'] = Evaluator.calculate_entropy(image)
        else:
            # 彩色图像
            for i in range(image.shape[2]):
                result[f'entropy_channel_{i}'] = Evaluator.calculate_entropy(image, channel=i)
            # 整体熵
            result['entropy_overall'] = Evaluator.calculate_entropy(image)
        
        return result
    
    @staticmethod
    def generate_histogram(image: np.ndarray, channel: Optional[int] = None) -> np.ndarray:
        """
        生成直方图数据
        
        Args:
            image: 输入图像
            channel: 指定通道，None表示使用所有像素
            
        Returns:
            直方图数组 (256,)
        """
        if image is None or image.size == 0:
            raise ValueError("图像不能为空")
        
        # 处理多通道图像
        if len(image.shape) == 3 and channel is not None:
            if channel >= image.shape[2]:
                raise ValueError(f"通道索引 {channel} 超出范围")
            image = image[:, :, channel]
        
        # 计算直方图
        hist, _ = np.histogram(image.flatten(), bins=256, range=(0, 256))
        
        return hist

    
    @staticmethod
    def calculate_histogram_uniformity(image: np.ndarray, channel: Optional[int] = None) -> float:
        """
        计算直方图均匀性 (使用卡方检验)
        
        Args:
            image: 输入图像
            channel: 指定通道
            
        Returns:
            p值 (越接近1表示越均匀)
        """
        hist = Evaluator.generate_histogram(image, channel)
        
        # 期望的均匀分布
        expected = np.full(256, image.size / 256)
        
        # 卡方检验
        try:
            chi2, p_value = chi2_contingency([hist, expected])[:2]
            return float(p_value)
        except:
            return 0.0
    
    @staticmethod
    def calculate_pixel_correlation(image: np.ndarray, 
                                    direction: str = 'horizontal',
                                    channel: Optional[int] = None,
                                    sample_size: int = 5000) -> float:
        """
        计算相邻像素相关性
        
        Args:
            image: 输入图像
            direction: 方向 ('horizontal', 'vertical', 'diagonal')
            channel: 指定通道，None表示使用第一个通道或灰度
            sample_size: 采样数量（用于大图像加速）
            
        Returns:
            相关系数 [-1, 1]
        """
        if image is None or image.size == 0:
            raise ValueError("图像不能为空")
        
        # 处理多通道图像
        if len(image.shape) == 3:
            if channel is not None and channel < image.shape[2]:
                img = image[:, :, channel]
            else:
                img = image[:, :, 0]  # 默认使用第一个通道
        else:
            img = image
        
        h, w = img.shape
        
        # 根据方向选择相邻像素对
        if direction == 'horizontal':
            if w < 2:
                return 0.0
            x = img[:, :-1].flatten()
            y = img[:, 1:].flatten()
        elif direction == 'vertical':
            if h < 2:
                return 0.0
            x = img[:-1, :].flatten()
            y = img[1:, :].flatten()
        elif direction == 'diagonal':
            if h < 2 or w < 2:
                return 0.0
            x = img[:-1, :-1].flatten()
            y = img[1:, 1:].flatten()
        else:
            raise ValueError(f"不支持的方向: {direction}")
        
        # 采样（如果数据量太大）
        if len(x) > sample_size:
            indices = np.random.choice(len(x), sample_size, replace=False)
            x = x[indices]
            y = y[indices]
        
        # 计算相关系数
        if len(x) == 0:
            return 0.0
        
        try:
            correlation = np.corrcoef(x, y)[0, 1]
            return float(correlation) if not np.isnan(correlation) else 0.0
        except:
            return 0.0

    
    @staticmethod
    def calculate_correlation_all_directions(image: np.ndarray, 
                                            channel: Optional[int] = None) -> Dict[str, float]:
        """
        计算所有方向的相邻像素相关性
        
        Args:
            image: 输入图像
            channel: 指定通道
            
        Returns:
            包含各方向相关性的字典
        """
        return {
            'correlation_horizontal': Evaluator.calculate_pixel_correlation(
                image, 'horizontal', channel
            ),
            'correlation_vertical': Evaluator.calculate_pixel_correlation(
                image, 'vertical', channel
            ),
            'correlation_diagonal': Evaluator.calculate_pixel_correlation(
                image, 'diagonal', channel
            )
        }
    
    # ==================== 安全指标 ====================
    
    @staticmethod
    def calculate_npcr(image1: np.ndarray, image2: np.ndarray) -> float:
        """
        计算 NPCR (Number of Pixels Change Rate)
        像素改变率
        
        Args:
            image1: 第一张图像
            image2: 第二张图像
            
        Returns:
            NPCR值 (百分比)
        """
        if image1.shape != image2.shape:
            raise ValueError("两张图像的形状必须相同")
        
        if image1.size == 0:
            raise ValueError("图像不能为空")
        
        # 计算不同像素的数量
        diff = (image1 != image2).astype(np.float64)
        npcr = (diff.sum() / diff.size) * 100.0
        
        return float(npcr)
    
    @staticmethod
    def calculate_uaci(image1: np.ndarray, image2: np.ndarray) -> float:
        """
        计算 UACI (Unified Average Changing Intensity)
        统一平均改变强度
        
        Args:
            image1: 第一张图像
            image2: 第二张图像
            
        Returns:
            UACI值 (百分比)
        """
        if image1.shape != image2.shape:
            raise ValueError("两张图像的形状必须相同")
        
        if image1.size == 0:
            raise ValueError("图像不能为空")
        
        # 计算像素差异的绝对值
        diff = np.abs(image1.astype(np.float64) - image2.astype(np.float64))
        uaci = (diff.sum() / (diff.size * 255.0)) * 100.0
        
        return float(uaci)

    
    @staticmethod
    def calculate_npcr_uaci(image1: np.ndarray, image2: np.ndarray) -> Dict[str, float]:
        """
        同时计算 NPCR 和 UACI
        
        Args:
            image1: 第一张图像
            image2: 第二张图像
            
        Returns:
            包含 NPCR 和 UACI 的字典
        """
        return {
            'npcr': Evaluator.calculate_npcr(image1, image2),
            'uaci': Evaluator.calculate_uaci(image1, image2)
        }
    
    # ==================== 敏感性测试 ====================
    
    @staticmethod
    def test_key_sensitivity(encrypt_func: Callable,
                           image: np.ndarray,
                           key: Any,
                           bit_position: int = 0) -> Dict[str, Any]:
        """
        测试密钥敏感性（改变密钥的1个bit）
        
        Args:
            encrypt_func: 加密函数 func(image, key) -> encrypted
            image: 原始图像
            key: 原始密钥
            bit_position: 要改变的bit位置
            
        Returns:
            包含敏感性指标的字典
        """
        if image is None or image.size == 0:
            raise ValueError("图像不能为空")
        
        # 使用原始密钥加密
        encrypted1 = encrypt_func(image, key)
        
        # 修改密钥的1个bit
        if isinstance(key, int):
            # 整数密钥：翻转指定bit
            modified_key = key ^ (1 << bit_position)
        elif isinstance(key, float):
            # 浮点密钥：转换为整数，翻转bit，再转回
            key_bits = int(key * 1e10)
            modified_bits = key_bits ^ (1 << bit_position)
            modified_key = modified_bits / 1e10
        elif isinstance(key, str):
            # 字符串密钥：修改一个字符
            key_list = list(key)
            if len(key_list) > 0:
                idx = bit_position % len(key_list)
                key_list[idx] = chr((ord(key_list[idx]) + 1) % 256)
                modified_key = ''.join(key_list)
            else:
                modified_key = key
        elif isinstance(key, dict):
            # 字典密钥：修改第一个数值字段的 bit
            modified_key = key.copy()
            for k in modified_key:
                if isinstance(modified_key[k], (int, float)):
                    if isinstance(modified_key[k], int):
                        modified_key[k] = modified_key[k] ^ (1 << bit_position)
                    else:
                        key_bits = int(modified_key[k] * 1e10)
                        modified_bits = key_bits ^ (1 << bit_position)
                        modified_key[k] = modified_bits / 1e10
                    break
        else:
            # 其他类型：尝试转换为整数处理
            try:
                key_int = int(key)
                modified_key = key_int ^ (1 << bit_position)
            except:
                raise TypeError(f"不支持的密钥类型: {type(key)}")
        
        # 使用修改后的密钥加密
        encrypted2 = encrypt_func(image, modified_key)
        
        # 计算差异
        npcr = Evaluator.calculate_npcr(encrypted1, encrypted2)
        uaci = Evaluator.calculate_uaci(encrypted1, encrypted2)
        
        return {
            'original_key': key,
            'modified_key': modified_key,
            'bit_position': bit_position,
            'npcr': npcr,
            'uaci': uaci,
            'is_sensitive': npcr > 99.0  # NPCR > 99% 表示高敏感性
        }

    
    @staticmethod
    def test_plaintext_sensitivity(encrypt_func: Callable,
                                   image: np.ndarray,
                                   key: Any,
                                   pixel_position: Optional[Tuple[int, int]] = None) -> Dict[str, Any]:
        """
        测试明文敏感性（改变图像的1个像素）
        
        Args:
            encrypt_func: 加密函数 func(image, key) -> encrypted
            image: 原始图像
            key: 密钥
            pixel_position: 要修改的像素位置 (row, col)，None表示随机选择
            
        Returns:
            包含敏感性指标的字典
        """
        if image is None or image.size == 0:
            raise ValueError("图像不能为空")
        
        # 使用原始图像加密
        encrypted1 = encrypt_func(image.copy(), key)
        
        # 修改图像的1个像素
        modified_image = image.copy()
        
        if pixel_position is None:
            # 随机选择一个像素
            if len(image.shape) == 2:
                row = np.random.randint(0, image.shape[0])
                col = np.random.randint(0, image.shape[1])
            else:
                row = np.random.randint(0, image.shape[0])
                col = np.random.randint(0, image.shape[1])
        else:
            row, col = pixel_position
        
        # 修改像素值（加1并取模）
        if len(modified_image.shape) == 2:
            original_value = modified_image[row, col]
            modified_image[row, col] = np.uint8((int(modified_image[row, col]) + 1) % 256)
            modified_value = modified_image[row, col]
        else:
            original_value = modified_image[row, col, 0]
            modified_image[row, col, 0] = np.uint8((int(modified_image[row, col, 0]) + 1) % 256)
            modified_value = modified_image[row, col, 0]
        
        # 使用修改后的图像加密
        encrypted2 = encrypt_func(modified_image, key)
        
        # 计算差异
        npcr = Evaluator.calculate_npcr(encrypted1, encrypted2)
        uaci = Evaluator.calculate_uaci(encrypted1, encrypted2)
        
        return {
            'pixel_position': (row, col),
            'original_value': int(original_value),
            'modified_value': int(modified_value),
            'npcr': npcr,
            'uaci': uaci,
            'is_sensitive': npcr > 99.0  # NPCR > 99% 表示高敏感性
        }

    
    @staticmethod
    def test_differential_attack(encrypt_func: Callable,
                                 image: np.ndarray,
                                 key: Any) -> Dict[str, Any]:
        """
        综合差分攻击测试，同时执行明文敏感性测试和密钥敏感性测试。

        Args:
            encrypt_func: 加密函数 func(image, key) -> encrypted
            image: 原始图像
            key: 原始密钥

        Returns:
            包含两类敏感性测试结果的字典
        """
        plaintext_result = Evaluator.test_plaintext_sensitivity(
            encrypt_func, image, key, pixel_position=(0, 0)
        )

        key_result = Evaluator.test_key_sensitivity(
            encrypt_func, image, key, bit_position=0
        )

        return {
            'plaintext_sensitivity': {
                'pixel_position': plaintext_result['pixel_position'],
                'original_value': plaintext_result['original_value'],
                'modified_value': plaintext_result['modified_value'],
                'npcr': plaintext_result['npcr'],
                'uaci': plaintext_result['uaci'],
                'is_sensitive': plaintext_result['is_sensitive']
            },
            'key_sensitivity': {
                'original_key': key_result['original_key'],
                'modified_key': key_result['modified_key'],
                'modification_description': Evaluator._build_key_mod_description(
                    key, key_result['modified_key']
                ),
                'npcr': key_result['npcr'],
                'uaci': key_result['uaci'],
                'is_sensitive': key_result['is_sensitive']
            }
        }

    @staticmethod
    def _build_key_mod_description(original_key: Any, modified_key: Any) -> str:
        """
        根据密钥类型生成易读的变化描述。

        Args:
            original_key: 原始密钥
            modified_key: 修改后的密钥

        Returns:
            描述密钥如何变化的字符串
        """
        if isinstance(original_key, int):
            diff = modified_key - original_key
            return f"整数密钥 ±{diff}"
        elif isinstance(original_key, float):
            diff = modified_key - original_key
            return f"浮点密钥 ±{diff:.10g}"
        elif isinstance(original_key, str):
            return f"字符串密钥第1个字符 +1"
        elif isinstance(original_key, dict):
            changed_keys = []
            for k in original_key:
                if k in modified_key and original_key[k] != modified_key[k]:
                    changed_keys.append(k)
            return f"字典密钥 {changed_keys[0] if changed_keys else '?'} 发生变化"
        else:
            return f"{type(original_key).__name__} 密钥发生变化"

    # ==================== 性能指标 ====================
    
    @staticmethod
    def measure_encryption_time(encrypt_func: Callable,
                               image: np.ndarray,
                               key: Any,
                               iterations: int = 10) -> Dict[str, float]:
        """
        测量加密耗时
        
        Args:
            encrypt_func: 加密函数
            image: 输入图像
            key: 密钥
            iterations: 迭代次数
            
        Returns:
            包含时间统计的字典
        """
        if iterations < 1:
            raise ValueError("迭代次数必须大于0")
        
        times = []
        
        for _ in range(iterations):
            start_time = time.perf_counter()
            _ = encrypt_func(image.copy(), key)
            end_time = time.perf_counter()
            times.append(end_time - start_time)
        
        times = np.array(times)
        
        return {
            'mean_time': float(np.mean(times)),
            'std_time': float(np.std(times)),
            'min_time': float(np.min(times)),
            'max_time': float(np.max(times)),
            'median_time': float(np.median(times)),
            'total_time': float(np.sum(times)),
            'iterations': iterations
        }
    
    @staticmethod
    def measure_memory_usage(encrypt_func: Callable,
                            image: np.ndarray,
                            key: Any) -> Dict[str, float]:
        """
        测量内存占用情况
        
        Args:
            encrypt_func: 加密函数
            image: 输入图像
            key: 密钥
            
        Returns:
            包含内存统计的字典 (单位: MB)
        """
        # 开始内存追踪
        tracemalloc.start()
        
        # 获取初始内存
        snapshot_before = tracemalloc.take_snapshot()
        
        # 执行加密
        encrypted = encrypt_func(image.copy(), key)
        
        # 获取加密后内存
        snapshot_after = tracemalloc.take_snapshot()
        
        # 停止追踪
        tracemalloc.stop()
        
        # 计算内存差异
        top_stats = snapshot_after.compare_to(snapshot_before, 'lineno')
        
        total_memory = sum(stat.size_diff for stat in top_stats)
        peak_memory = sum(stat.size for stat in top_stats if stat.size > 0)
        
        # 计算图像内存占用
        image_memory = image.nbytes
        encrypted_memory = encrypted.nbytes
        
        return {
            'image_size_mb': image_memory / (1024 * 1024),
            'encrypted_size_mb': encrypted_memory / (1024 * 1024),
            'memory_increase_mb': total_memory / (1024 * 1024),
            'peak_memory_mb': peak_memory / (1024 * 1024),
            'image_shape': image.shape,
            'encrypted_shape': encrypted.shape
        }

    
    @staticmethod
    def measure_throughput(encrypt_func: Callable,
                          image: np.ndarray,
                          key: Any,
                          duration: float = 1.0) -> Dict[str, float]:
        """
        测量加密吞吐量
        
        Args:
            encrypt_func: 加密函数
            image: 输入图像
            key: 密钥
            duration: 测试持续时间（秒）
            
        Returns:
            包含吞吐量统计的字典
        """
        start_time = time.perf_counter()
        iterations = 0
        
        while time.perf_counter() - start_time < duration:
            _ = encrypt_func(image.copy(), key)
            iterations += 1
        
        elapsed_time = time.perf_counter() - start_time
        
        # 计算吞吐量
        pixels_per_second = (image.size * iterations) / elapsed_time
        mb_per_second = (image.nbytes * iterations) / (elapsed_time * 1024 * 1024)
        images_per_second = iterations / elapsed_time
        
        return {
            'iterations': iterations,
            'elapsed_time': elapsed_time,
            'images_per_second': images_per_second,
            'pixels_per_second': pixels_per_second,
            'mb_per_second': mb_per_second
        }
    
    # ==================== 综合评估 ====================
    
    @staticmethod
    def comprehensive_evaluation(encrypt_func: Callable,
                                decrypt_func: Callable,
                                original_image: np.ndarray,
                                key: Any,
                                include_performance: bool = True,
                                include_sensitivity: bool = True) -> Dict[str, Any]:
        """
        综合评估加密算法
        
        Args:
            encrypt_func: 加密函数
            decrypt_func: 解密函数
            original_image: 原始图像
            key: 密钥
            include_performance: 是否包含性能测试
            include_sensitivity: 是否包含敏感性测试
            
        Returns:
            包含所有评估指标的字典
        """
        results = {
            'image_info': {
                'shape': original_image.shape,
                'dtype': str(original_image.dtype),
                'size': original_image.size,
                'size_mb': original_image.nbytes / (1024 * 1024)
            }
        }
        
        # 加密图像
        encrypted_image = encrypt_func(original_image.copy(), key)
        
        # 解密图像
        decrypted_image = decrypt_func(encrypted_image.copy(), key)
        
        # 1. 统计学指标
        results['statistics'] = {
            'original': Evaluator.calculate_entropy_all_channels(original_image),
            'encrypted': Evaluator.calculate_entropy_all_channels(encrypted_image),
            'histogram_uniformity': Evaluator.calculate_histogram_uniformity(encrypted_image)
        }
        
        # 2. 相关性分析
        results['correlation'] = {
            'original': Evaluator.calculate_correlation_all_directions(original_image),
            'encrypted': Evaluator.calculate_correlation_all_directions(encrypted_image)
        }
        
        # 3. 安全指标
        results['security'] = Evaluator.calculate_npcr_uaci(original_image, encrypted_image)
        
        # 4. 解密质量
        results['decryption_quality'] = {
            'perfect_recovery': np.array_equal(original_image, decrypted_image),
            'mse': float(np.mean((original_image.astype(float) - decrypted_image.astype(float)) ** 2)),
            'different_pixels': int(np.sum(original_image != decrypted_image))
        }
        
        # 5. 敏感性测试（可选）
        if include_sensitivity:
            try:
                results['sensitivity'] = {
                    'key_sensitivity': Evaluator.test_key_sensitivity(
                        encrypt_func, original_image, key
                    ),
                    'plaintext_sensitivity': Evaluator.test_plaintext_sensitivity(
                        encrypt_func, original_image, key
                    )
                }
            except Exception as e:
                results['sensitivity'] = {'error': str(e)}
        
        # 6. 性能指标（可选）
        if include_performance:
            try:
                results['performance'] = {
                    'encryption_time': Evaluator.measure_encryption_time(
                        encrypt_func, original_image, key, iterations=5
                    ),
                    'memory_usage': Evaluator.measure_memory_usage(
                        encrypt_func, original_image, key
                    )
                }
            except Exception as e:
                results['performance'] = {'error': str(e)}
        
        return results
