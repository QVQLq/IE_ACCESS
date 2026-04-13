"""
控制器类
负责协调算法、图像和评估器之间的交互
"""
from typing import List, Dict, Any, Optional
import numpy as np
from PySide6.QtCore import QThread, Signal
from core.base_encryptor import BaseEncryptor
from core.evaluator import Evaluator


class BatchEvaluationThread(QThread):
    """批量评估线程"""
    
    # 信号定义
    progress = Signal(int, int, str)  # (当前索引, 总数, 消息)
    image_started = Signal(int, str)  # (索引, 图像名称)
    image_finished = Signal(int, dict)  # (索引, 结果)
    all_finished = Signal(list)  # 所有结果列表
    error = Signal(int, str)  # (索引, 错误消息)
    
    def __init__(self, algorithm: BaseEncryptor, image_list: List[tuple], key: Any):
        """
        初始化批量评估线程
        
        Args:
            algorithm: 加密算法实例
            image_list: 图像列表 [(图像名称, 图像数组), ...]
            key: 加密密钥
        """
        super().__init__()
        self.algorithm = algorithm
        self.image_list = image_list
        self.key = key
        self.result_list = []
        self._is_running = True
        
        # 统计信息
        self.total_pixels = 0
        self.total_encryption_time = 0.0
        self.total_decryption_time = 0.0
    
    def stop(self):
        """停止线程"""
        self._is_running = False
    
    def run(self):
        """运行批量评估"""
        total = len(self.image_list)
        
        for idx, (image_name, image_data) in enumerate(self.image_list):
            if not self._is_running:
                break
            
            try:
                # 发送开始信号
                self.image_started.emit(idx, image_name)
                self.progress.emit(idx, total, f"处理图像 {idx+1}/{total}: {image_name}")
                
                # 执行评估
                result = self._evaluate_single_image(image_name, image_data)
                
                # 累加统计信息
                self.total_pixels += result.get('image_size', 0)
                self.total_encryption_time += result.get('encryption_time', 0)
                self.total_decryption_time += result.get('decryption_time', 0)
                
                # 添加到结果列表
                self.result_list.append(result)
                
                # 发送完成信号
                self.image_finished.emit(idx, result)
                
            except Exception as e:
                # 发送错误信号
                error_msg = f"处理失败: {str(e)}"
                self.error.emit(idx, error_msg)
                
                # 添加错误结果
                error_result = {
                    'image_name': image_name,
                    'status': 'error',
                    'error_message': error_msg
                }
                self.result_list.append(error_result)
        
        # 计算整体统计
        if self.total_encryption_time > 0:
            overall_encryption_speed = self.total_pixels / self.total_encryption_time
        else:
            overall_encryption_speed = 0
        
        if self.total_decryption_time > 0:
            overall_decryption_speed = self.total_pixels / self.total_decryption_time
        else:
            overall_decryption_speed = 0
        
        # 添加整体统计到结果
        overall_stats = {
            'total_images': total,
            'total_pixels': self.total_pixels,
            'total_encryption_time': self.total_encryption_time,
            'total_decryption_time': self.total_decryption_time,
            'overall_encryption_speed': overall_encryption_speed,
            'overall_decryption_speed': overall_decryption_speed
        }
        
        # 将整体统计添加到每个结果中
        for result in self.result_list:
            if result['status'] == 'success':
                result['overall_stats'] = overall_stats
        
        # 发送完成信号
        self.all_finished.emit(self.result_list)
    
    def _evaluate_single_image(self, image_name: str, image_data: np.ndarray) -> Dict[str, Any]:
        """
        评估单个图像
        
        Args:
            image_name: 图像名称
            image_data: 图像数据
            
        Returns:
            评估结果字典
        """
        import time
        
        # 基本信息
        result = {
            'image_name': image_name,
            'status': 'success',
            'image_shape': image_data.shape,
            'image_size': image_data.size,
        }
        
        # 1. 加密（测量时间）
        self.progress.emit(-1, -1, f"加密: {image_name}")
        start_time = time.perf_counter()
        encrypted = self.algorithm.encrypt(image_data.copy(), self.key)
        encryption_time = time.perf_counter() - start_time
        result['encryption_time'] = encryption_time
        
        # 2. 解密（测量时间）
        self.progress.emit(-1, -1, f"解密: {image_name}")
        start_time = time.perf_counter()
        decrypted = self.algorithm.decrypt(encrypted.copy(), self.key)
        decryption_time = time.perf_counter() - start_time
        result['decryption_time'] = decryption_time
        
        # 3. 计算评估指标
        self.progress.emit(-1, -1, f"计算指标: {image_name}")
        
        # 统计学指标
        result['entropy_original'] = Evaluator.calculate_entropy(image_data)
        result['entropy_encrypted'] = Evaluator.calculate_entropy(encrypted)
        
        # 相关性
        result['correlation_original'] = Evaluator.calculate_correlation_all_directions(image_data)
        result['correlation_encrypted'] = Evaluator.calculate_correlation_all_directions(encrypted)
        
        # 安全指标
        # 修改一个像素来计算 NPCR/UACI
        modified_image = image_data.copy()
        if len(modified_image.shape) == 2:
            modified_image[0, 0] = np.uint8((int(modified_image[0, 0]) + 1) % 256)
        else:
            modified_image[0, 0, 0] = np.uint8((int(modified_image[0, 0, 0]) + 1) % 256)

        encrypted_modified = self.algorithm.encrypt(modified_image, self.key)
        result['npcr'] = Evaluator.calculate_npcr(encrypted, encrypted_modified)
        result['uaci'] = Evaluator.calculate_uaci(encrypted, encrypted_modified)

        # 差分攻击测试（明文敏感性 + 密钥敏感性）
        result['differential_attack_test'] = Evaluator.test_differential_attack(
            self.algorithm.encrypt, image_data, self.key
        )
        
        # 解密质量
        result['perfect_recovery'] = np.array_equal(image_data, decrypted)
        result['mse'] = float(np.mean((image_data.astype(float) - decrypted.astype(float)) ** 2))
        
        # 单个图像的加密速度
        result['encryption_speed'] = image_data.size / encryption_time if encryption_time > 0 else 0
        result['decryption_speed'] = image_data.size / decryption_time if decryption_time > 0 else 0
        
        # 存储图像
        result['original_image'] = image_data
        result['encrypted_image'] = encrypted
        result['decrypted_image'] = decrypted
        
        return result


class Controller:
    """
    控制器类
    协调算法、图像和评估器
    """
    
    def __init__(self):
        self.algorithm = None
        self.key = None
        self.image_list = []
        self.result_list = []
        self.evaluation_thread = None
    
    def set_algorithm(self, algorithm: BaseEncryptor):
        """设置算法"""
        self.algorithm = algorithm
    
    def set_key(self, key: Any):
        """设置密钥"""
        self.key = key
    
    def add_image(self, image_name: str, image_data: np.ndarray):
        """添加图像"""
        self.image_list.append((image_name, image_data))
    
    def clear_images(self):
        """清空图像列表"""
        self.image_list.clear()
    
    def clear_results(self):
        """清空结果列表"""
        self.result_list.clear()
    
    def start_batch_evaluation(self) -> BatchEvaluationThread:
        """
        开始批量评估
        
        Returns:
            评估线程对象
        """
        if self.algorithm is None:
            raise ValueError("未设置算法")
        
        if len(self.image_list) == 0:
            raise ValueError("图像列表为空")
        
        if self.key is None:
            raise ValueError("未设置密钥")
        
        # 清空之前的结果
        self.result_list.clear()
        
        # 创建评估线程
        self.evaluation_thread = BatchEvaluationThread(
            self.algorithm,
            self.image_list,
            self.key
        )
        
        return self.evaluation_thread
    
    def stop_evaluation(self):
        """停止评估"""
        if self.evaluation_thread and self.evaluation_thread.isRunning():
            self.evaluation_thread.stop()
            self.evaluation_thread.wait()
    
    def get_results(self) -> List[Dict[str, Any]]:
        """获取所有结果"""
        return self.result_list
    
    def export_results_summary(self) -> str:
        """
        导出结果摘要
        
        Returns:
            格式化的摘要文本
        """
        if len(self.result_list) == 0:
            return "无评估结果"
        
        summary = []
        summary.append("=" * 60)
        summary.append("批量评估结果摘要")
        summary.append("=" * 60)
        summary.append(f"总图像数: {len(self.result_list)}")
        summary.append(f"算法: {self.algorithm.name if hasattr(self.algorithm, 'name') else '未知'}")
        summary.append(f"密钥: {self.key}")
        summary.append("")
        
        for idx, result in enumerate(self.result_list):
            summary.append(f"图像 {idx+1}: {result['image_name']}")
            summary.append("-" * 40)
            
            if result['status'] == 'error':
                summary.append(f"  状态: 失败")
                summary.append(f"  错误: {result['error_message']}")
            else:
                summary.append(f"  状态: 成功")
                summary.append(f"  形状: {result['image_shape']}")
                summary.append(f"  原图熵: {result['entropy_original']:.4f}")
                summary.append(f"  密文熵: {result['entropy_encrypted']:.4f}")
                summary.append(f"  NPCR: {result['npcr']:.4f}%")
                summary.append(f"  UACI: {result['uaci']:.4f}%")
                summary.append(f"  加密时间: {result['encryption_time']*1000:.2f} ms")
                summary.append(f"  完美恢复: {'是' if result['perfect_recovery'] else '否'}")
            
            summary.append("")
        
        return "\n".join(summary)
