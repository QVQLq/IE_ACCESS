"""
PySide6 主窗口
图像加密算法测评系统
"""
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QPushButton, QLabel, QComboBox, QLineEdit, QListWidget,
    QGroupBox, QTableWidget, QTableWidgetItem, QSplitter,
    QFileDialog, QMessageBox, QProgressBar, QTextEdit, QScrollArea,
    QDialog
)
from PySide6.QtCore import Qt, QThread, Signal, QMimeData
from PySide6.QtGui import QPixmap, QImage, QDragEnterEvent, QDropEvent
import numpy as np
import cv2
import os
from typing import List, Dict, Any
from core.plugin_loader import PluginLoader
from core.evaluator import Evaluator


class EvaluationThread(QThread):
    """评估线程"""
    finished = Signal(dict)
    progress = Signal(str)
    error = Signal(str)
    
    def __init__(self, algorithm, image, key):
        super().__init__()
        self.algorithm = algorithm
        self.image = image
        self.key = key
    
    def run(self):
        try:
            self.progress.emit("正在加密图像...")
            encrypted = self.algorithm.encrypt(self.image.copy(), self.key)
            
            self.progress.emit("正在解密图像...")
            decrypted = self.algorithm.decrypt(encrypted.copy(), self.key)
            
            self.progress.emit("正在计算评估指标...")
            results = Evaluator.comprehensive_evaluation(
                self.algorithm.encrypt,
                self.algorithm.decrypt,
                self.image,
                self.key,
                include_performance=True,
                include_sensitivity=True
            )
            
            results['encrypted_image'] = encrypted
            results['decrypted_image'] = decrypted
            
            self.finished.emit(results)
        except Exception as e:
            self.error.emit(str(e))


class ImageListWidget(QListWidget):
    """支持拖拽的图像列表"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.image_paths = []
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
    
    def dropEvent(self, event: QDropEvent):
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif')):
                if file_path not in self.image_paths:
                    self.image_paths.append(file_path)
                    self.addItem(os.path.basename(file_path))
    
    def get_selected_image_path(self):
        """获取选中的图像路径"""
        current_row = self.currentRow()
        if current_row >= 0 and current_row < len(self.image_paths):
            return self.image_paths[current_row]
        return None
    
    def clear_all(self):
        """清空列表"""
        self.clear()
        self.image_paths.clear()



class ImagePreviewLabel(QLabel):
    """图像预览标签"""
    
    def __init__(self, title="", parent=None):
        super().__init__(parent)
        self.title = title
        self.setAlignment(Qt.AlignCenter)
        self.setMinimumSize(300, 300)
        self.setStyleSheet("""
            QLabel {
                background-color: #f0f0f0;
                border: 2px solid #cccccc;
                border-radius: 5px;
            }
        """)
        self.setText(f"{title}\n(无图像)")
    
    def set_image(self, image: np.ndarray):
        """设置显示的图像"""
        if image is None or image.size == 0:
            self.setText(f"{self.title}\n(无图像)")
            return
        
        # 转换为 QImage
        if len(image.shape) == 3:
            height, width, channel = image.shape
            bytes_per_line = 3 * width
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            # 确保数组是连续的
            if not rgb_image.flags['C_CONTIGUOUS']:
                rgb_image = np.ascontiguousarray(rgb_image)
            q_image = QImage(rgb_image.data, width, height, bytes_per_line, QImage.Format_RGB888)
        else:
            height, width = image.shape
            bytes_per_line = width
            # 确保数组是连续的
            if not image.flags['C_CONTIGUOUS']:
                image = np.ascontiguousarray(image)
            q_image = QImage(image.data, width, height, bytes_per_line, QImage.Format_Grayscale8)
        
        # 转换为 QPixmap 并缩放
        pixmap = QPixmap.fromImage(q_image)
        scaled_pixmap = pixmap.scaled(
            self.size(), 
            Qt.KeepAspectRatio, 
            Qt.SmoothTransformation
        )
        self.setPixmap(scaled_pixmap)
    
    def clear_image(self):
        """清空图像"""
        self.clear()
        self.setText(f"{self.title}\n(无图像)")


class DifferentialAttackDialog(QDialog):
    """差分攻击测试结果弹窗"""

    def __init__(self, plaintext_data, key_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("差分攻击测试结果")
        self.setMinimumSize(620, 340)
        self._build_ui(plaintext_data, key_data)

    def _build_ui(self, plaintext_data, key_data):
        main_layout = QHBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(15, 15, 15, 15)

        # 左侧：明文敏感性
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)

        left_title = QLabel("一、明文敏感性")
        left_title.setStyleSheet("font-weight: bold; font-size: 14px;")
        left_layout.addWidget(left_title)

        plaintext_table = QTableWidget()
        plaintext_table.setColumnCount(2)
        plaintext_table.setHorizontalHeaderLabels(["指标", "值"])
        plaintext_table.horizontalHeader().setStretchLastSection(True)
        plaintext_table.setEditTriggers(QTableWidget.NoEditTriggers)
        plaintext_table.setRowCount(5)
        rows = [
            ("修改像素位置", str(plaintext_data.get('pixel_position', ''))),
            ("原像素值", str(plaintext_data.get('original_value', ''))),
            ("修改后像素值", str(plaintext_data.get('modified_value', ''))),
            ("NPCR", f"{plaintext_data.get('npcr', 0):.4f}%"),
            ("UACI", f"{plaintext_data.get('uaci', 0):.4f}%"),
        ]
        for i, (label, value) in enumerate(rows):
            plaintext_table.setItem(i, 0, QTableWidgetItem(label))
            plaintext_table.setItem(i, 1, QTableWidgetItem(value))
        left_layout.addWidget(plaintext_table)

        # 右侧：密钥敏感性
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)

        right_title = QLabel("二、密钥敏感性")
        right_title.setStyleSheet("font-weight: bold; font-size: 14px;")
        right_layout.addWidget(right_title)

        key_table = QTableWidget()
        key_table.setColumnCount(2)
        key_table.setHorizontalHeaderLabels(["指标", "值"])
        key_table.horizontalHeader().setStretchLastSection(True)
        key_table.setEditTriggers(QTableWidget.NoEditTriggers)
        key_table.setRowCount(5)
        rows = [
            ("原密钥", str(key_data.get('original_key', ''))),
            ("修改后密钥", str(key_data.get('modified_key', ''))),
            ("修改说明", key_data.get('modification_description', '')),
            ("NPCR", f"{key_data.get('npcr', 0):.4f}%"),
            ("UACI", f"{key_data.get('uaci', 0):.4f}%"),
        ]
        for i, (label, value) in enumerate(rows):
            key_table.setItem(i, 0, QTableWidgetItem(label))
            key_table.setItem(i, 1, QTableWidgetItem(value))
        right_layout.addWidget(key_table)

        main_layout.addWidget(left_widget, 1)
        main_layout.addWidget(right_widget, 1)

        # 关闭按钮
        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()
        close_btn = QPushButton("关闭")
        close_btn.clicked.connect(self.accept)
        bottom_layout.addWidget(close_btn)
        main_layout.addLayout(bottom_layout)


class MainWindow(QMainWindow):
    """主窗口"""
    
    def __init__(self):
        super().__init__()
        self.plugin_loader = PluginLoader()
        self.algorithms = {}
        self.current_algorithm = None
        self.current_image = None
        self.encrypted_image = None
        self.decrypted_image = None
        self.evaluation_results = None
        
        self.init_ui()
        self.load_algorithms()
    
    def init_ui(self):
        """初始化界面"""
        self.setWindowTitle("ImageCrypto-Bench - 图像加密算法测评系统")
        self.setGeometry(100, 100, 1600, 900)
        
        # 中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # 左侧面板
        left_panel = self.create_left_panel()
        main_layout.addWidget(left_panel, 1)
        
        # 中间面板（图像预览）
        middle_panel = self.create_middle_panel()
        main_layout.addWidget(middle_panel, 3)
        
        # 右侧面板（测评数据）
        right_panel = self.create_right_panel()
        main_layout.addWidget(right_panel, 2)
    
    def create_left_panel(self) -> QWidget:
        """创建左侧控制面板"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setSpacing(10)
        
        # 算法选择区
        algo_group = QGroupBox("算法选择")
        algo_layout = QVBoxLayout()
        
        algo_layout.addWidget(QLabel("选择加密算法:"))
        self.algo_combo = QComboBox()
        self.algo_combo.currentTextChanged.connect(self.on_algorithm_changed)
        algo_layout.addWidget(self.algo_combo)
        
        # 算法信息
        self.algo_info_label = QLabel("算法信息将显示在这里")
        self.algo_info_label.setWordWrap(True)
        self.algo_info_label.setStyleSheet("padding: 5px; background-color: #f9f9f9;")
        algo_layout.addWidget(self.algo_info_label)
        
        algo_group.setLayout(algo_layout)
        layout.addWidget(algo_group)
        
        # 图像导入区
        image_group = QGroupBox("图像导入")
        image_layout = QVBoxLayout()
        
        image_layout.addWidget(QLabel("拖拽图像到列表或点击按钮添加:"))
        
        self.image_list = ImageListWidget()
        self.image_list.setMaximumHeight(200)
        self.image_list.currentRowChanged.connect(self.on_image_selected)
        image_layout.addWidget(self.image_list)
        
        # 图像操作按钮
        btn_layout = QHBoxLayout()
        
        self.add_image_btn = QPushButton("添加图像")
        self.add_image_btn.clicked.connect(self.add_images)
        btn_layout.addWidget(self.add_image_btn)
        
        self.clear_images_btn = QPushButton("清空列表")
        self.clear_images_btn.clicked.connect(self.clear_images)
        btn_layout.addWidget(self.clear_images_btn)
        
        image_layout.addLayout(btn_layout)
        
        image_group.setLayout(image_layout)
        layout.addWidget(image_group)
        
        # 密钥输入区
        key_group = QGroupBox("密钥设置")
        key_layout = QVBoxLayout()
        
        key_layout.addWidget(QLabel("输入密钥:"))
        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("例如: 12345 或 mykey123")
        self.key_input.setText("42")
        key_layout.addWidget(self.key_input)
        
        key_group.setLayout(key_layout)
        layout.addWidget(key_group)
        
        # 运行按钮
        self.run_btn = QPushButton("运行评估")
        self.run_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        self.run_btn.clicked.connect(self.run_evaluation)
        self.run_btn.setEnabled(False)
        layout.addWidget(self.run_btn)

        # 差分攻击测试按钮
        self.diff_attack_btn = QPushButton("差分攻击测试")
        self.diff_attack_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 8px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #FB8C00;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        self.diff_attack_btn.clicked.connect(self.run_differential_attack_test)
        self.diff_attack_btn.setEnabled(False)
        layout.addWidget(self.diff_attack_btn)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # 状态信息
        self.status_label = QLabel("就绪")
        self.status_label.setStyleSheet("padding: 5px; background-color: #e3f2fd;")
        layout.addWidget(self.status_label)
        
        layout.addStretch()
        
        return panel

    
    def create_middle_panel(self) -> QWidget:
        """创建中间图像预览面板"""
        panel = QWidget()
        layout = QHBoxLayout(panel)
        layout.setSpacing(10)
        
        # 原始图像
        original_group = QGroupBox("原始图像")
        original_layout = QVBoxLayout()
        self.original_preview = ImagePreviewLabel("原图")
        original_layout.addWidget(self.original_preview)
        original_group.setLayout(original_layout)
        layout.addWidget(original_group)
        
        # 加密图像
        encrypted_group = QGroupBox("加密图像")
        encrypted_layout = QVBoxLayout()
        self.encrypted_preview = ImagePreviewLabel("密文")
        encrypted_layout.addWidget(self.encrypted_preview)
        encrypted_group.setLayout(encrypted_layout)
        layout.addWidget(encrypted_group)
        
        # 解密图像
        decrypted_group = QGroupBox("解密图像")
        decrypted_layout = QVBoxLayout()
        self.decrypted_preview = ImagePreviewLabel("解密")
        decrypted_layout.addWidget(self.decrypted_preview)
        decrypted_group.setLayout(decrypted_layout)
        layout.addWidget(decrypted_group)
        
        return panel
    
    def create_right_panel(self) -> QWidget:
        """创建右侧测评数据面板"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setSpacing(10)
        
        # 性能指标区
        perf_group = QGroupBox("性能指标")
        perf_layout = QVBoxLayout()
        
        self.perf_text = QTextEdit()
        self.perf_text.setReadOnly(True)
        self.perf_text.setMaximumHeight(150)
        self.perf_text.setPlaceholderText("运行评估后显示性能指标...")
        perf_layout.addWidget(self.perf_text)
        
        perf_group.setLayout(perf_layout)
        layout.addWidget(perf_group)
        
        # NPCR/UACI 表格
        security_group = QGroupBox("安全指标")
        security_layout = QVBoxLayout()
        
        self.security_table = QTableWidget()
        self.security_table.setColumnCount(2)
        self.security_table.setHorizontalHeaderLabels(["指标", "值"])
        self.security_table.setMaximumHeight(150)
        self.security_table.horizontalHeader().setStretchLastSection(True)
        security_layout.addWidget(self.security_table)
        
        security_group.setLayout(security_layout)
        layout.addWidget(security_group)
        
        # 统计指标区
        stats_group = QGroupBox("统计指标")
        stats_layout = QVBoxLayout()
        
        self.stats_text = QTextEdit()
        self.stats_text.setReadOnly(True)
        self.stats_text.setMaximumHeight(150)
        self.stats_text.setPlaceholderText("运行评估后显示统计指标...")
        stats_layout.addWidget(self.stats_text)
        
        stats_group.setLayout(stats_layout)
        layout.addWidget(stats_group)
        
        # 直方图按钮
        histogram_group = QGroupBox("直方图")
        histogram_layout = QVBoxLayout()
        
        self.show_histogram_btn = QPushButton("显示直方图")
        self.show_histogram_btn.clicked.connect(self.show_histogram)
        self.show_histogram_btn.setEnabled(False)
        histogram_layout.addWidget(self.show_histogram_btn)
        
        histogram_group.setLayout(histogram_layout)
        layout.addWidget(histogram_group)
        
        # 详细报告
        report_group = QGroupBox("详细报告")
        report_layout = QVBoxLayout()
        
        self.report_text = QTextEdit()
        self.report_text.setReadOnly(True)
        self.report_text.setPlaceholderText("运行评估后显示详细报告...")
        report_layout.addWidget(self.report_text)
        
        report_group.setLayout(report_layout)
        layout.addWidget(report_group)
        
        return panel

    
    # ==================== 功能实现 ====================
    
    def load_algorithms(self):
        """加载算法插件"""
        try:
            self.algorithms = self.plugin_loader.load_plugins()
            
            if len(self.algorithms) == 0:
                QMessageBox.warning(
                    self, 
                    "警告", 
                    "未找到任何算法插件！\n请在 algorithms/ 目录下添加算法文件。"
                )
                return
            
            # 填充下拉菜单
            self.algo_combo.clear()
            self.algo_combo.addItems(list(self.algorithms.keys()))
            
            self.status_label.setText(f"成功加载 {len(self.algorithms)} 个算法")
        
        except Exception as e:
            QMessageBox.critical(self, "错误", f"加载算法失败: {str(e)}")
    
    def on_algorithm_changed(self, algo_name: str):
        """算法选择改变"""
        if algo_name in self.algorithms:
            self.current_algorithm = self.algorithms[algo_name]
            
            # 显示算法信息
            info_text = f"<b>算法:</b> {algo_name}<br>"
            if hasattr(self.current_algorithm, 'description'):
                info_text += f"<b>描述:</b> {self.current_algorithm.description}<br>"
            if hasattr(self.current_algorithm, 'version'):
                info_text += f"<b>版本:</b> {self.current_algorithm.version}<br>"
            if hasattr(self.current_algorithm, 'author'):
                info_text += f"<b>作者:</b> {self.current_algorithm.author}"
            
            self.algo_info_label.setText(info_text)
            self.update_run_button_state()
    
    def add_images(self):
        """添加图像"""
        file_paths, _ = QFileDialog.getOpenFileNames(
            self,
            "选择图像文件",
            "",
            "图像文件 (*.png *.jpg *.jpeg *.bmp *.tiff *.tif)"
        )
        
        for file_path in file_paths:
            if file_path not in self.image_list.image_paths:
                self.image_list.image_paths.append(file_path)
                self.image_list.addItem(os.path.basename(file_path))
        
        if len(file_paths) > 0:
            self.status_label.setText(f"已添加 {len(file_paths)} 个图像")
    
    def clear_images(self):
        """清空图像列表"""
        self.image_list.clear_all()
        self.current_image = None
        self.original_preview.clear_image()
        self.encrypted_preview.clear_image()
        self.decrypted_preview.clear_image()
        self.update_run_button_state()
        self.status_label.setText("已清空图像列表")
    
    def on_image_selected(self, row: int):
        """图像选择改变"""
        image_path = self.image_list.get_selected_image_path()
        if image_path:
            try:
                self.current_image = cv2.imread(image_path)
                if self.current_image is not None:
                    self.original_preview.set_image(self.current_image)
                    self.encrypted_preview.clear_image()
                    self.decrypted_preview.clear_image()
                    self.update_run_button_state()
                    self.status_label.setText(f"已加载: {os.path.basename(image_path)}")
                else:
                    QMessageBox.warning(self, "警告", f"无法加载图像: {image_path}")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"加载图像失败: {str(e)}")
    
    def update_run_button_state(self):
        """更新运行按钮状态"""
        can_run = (
            self.current_algorithm is not None and
            self.current_image is not None and
            len(self.key_input.text()) > 0
        )
        self.run_btn.setEnabled(can_run)
        self.diff_attack_btn.setEnabled(can_run)

    
    def run_evaluation(self):
        """运行评估"""
        if self.current_algorithm is None or self.current_image is None:
            return
        
        # 获取密钥
        key_text = self.key_input.text()
        try:
            # 尝试转换为整数
            key = int(key_text)
        except ValueError:
            # 如果不是整数，使用字符串
            key = key_text
        
        # 禁用按钮
        self.run_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # 不确定进度
        
        # 创建评估线程
        self.eval_thread = EvaluationThread(
            self.current_algorithm,
            self.current_image,
            key
        )
        self.eval_thread.finished.connect(self.on_evaluation_finished)
        self.eval_thread.progress.connect(self.on_evaluation_progress)
        self.eval_thread.error.connect(self.on_evaluation_error)
        self.eval_thread.start()
    
    def on_evaluation_progress(self, message: str):
        """评估进度更新"""
        self.status_label.setText(message)
    
    def on_evaluation_error(self, error_message: str):
        """评估错误"""
        self.progress_bar.setVisible(False)
        self.run_btn.setEnabled(True)
        self.status_label.setText("评估失败")
        QMessageBox.critical(self, "错误", f"评估失败: {error_message}")
    
    def on_evaluation_finished(self, results: Dict[str, Any]):
        """评估完成"""
        self.progress_bar.setVisible(False)
        self.run_btn.setEnabled(True)
        self.status_label.setText("评估完成")
        
        self.evaluation_results = results
        
        # 显示图像
        self.encrypted_image = results.get('encrypted_image')
        self.decrypted_image = results.get('decrypted_image')
        
        if self.encrypted_image is not None:
            self.encrypted_preview.set_image(self.encrypted_image)
        
        if self.decrypted_image is not None:
            self.decrypted_preview.set_image(self.decrypted_image)
        
        # 显示评估结果
        self.display_results(results)
        
        # 启用直方图按钮
        self.show_histogram_btn.setEnabled(True)
    
    def display_results(self, results: Dict[str, Any]):
        """显示评估结果"""
        # 1. 性能指标
        perf_text = "<b>性能指标</b><br>"
        if 'performance' in results:
            perf = results['performance']
            if 'encryption_time' in perf:
                time_stats = perf['encryption_time']
                perf_text += f"<b>加密时间:</b> {time_stats['mean_time']*1000:.2f} ms<br>"
                perf_text += f"<b>速度:</b> {results['image_info']['size'] / time_stats['mean_time']:.0f} 像素/秒<br>"
            
            if 'memory_usage' in perf:
                mem = perf['memory_usage']
                perf_text += f"<b>图像大小:</b> {mem['image_size_mb']:.2f} MB<br>"
        
        self.perf_text.setHtml(perf_text)
        
        # 2. 安全指标表格
        self.security_table.setRowCount(0)
        
        if 'security' in results:
            security = results['security']
            
            row = self.security_table.rowCount()
            self.security_table.insertRow(row)
            self.security_table.setItem(row, 0, QTableWidgetItem("NPCR"))
            self.security_table.setItem(row, 1, QTableWidgetItem(f"{security['npcr']:.4f}%"))
            
            row = self.security_table.rowCount()
            self.security_table.insertRow(row)
            self.security_table.setItem(row, 0, QTableWidgetItem("UACI"))
            self.security_table.setItem(row, 1, QTableWidgetItem(f"{security['uaci']:.4f}%"))
        
        if 'sensitivity' in results and 'key_sensitivity' in results['sensitivity']:
            key_sens = results['sensitivity']['key_sensitivity']
            
            row = self.security_table.rowCount()
            self.security_table.insertRow(row)
            self.security_table.setItem(row, 0, QTableWidgetItem("密钥敏感性"))
            self.security_table.setItem(row, 1, QTableWidgetItem(
                "是" if key_sens['is_sensitive'] else "否"
            ))
        
        # 3. 统计指标
        stats_text = "<b>统计指标</b><br>"
        
        if 'statistics' in results:
            stats = results['statistics']
            
            if 'original' in stats:
                orig_entropy = stats['original'].get('entropy', 0)
                stats_text += f"<b>原图熵:</b> {orig_entropy:.4f} bits<br>"
            
            if 'encrypted' in stats:
                enc_entropy = stats['encrypted'].get('entropy', 0)
                stats_text += f"<b>密文熵:</b> {enc_entropy:.4f} bits<br>"
            
            if 'histogram_uniformity' in stats:
                stats_text += f"<b>直方图均匀性:</b> {stats['histogram_uniformity']:.6f}<br>"
        
        if 'correlation' in results and 'encrypted' in results['correlation']:
            corr = results['correlation']['encrypted']
            stats_text += f"<b>相关性 (水平):</b> {corr['correlation_horizontal']:.6f}<br>"
            stats_text += f"<b>相关性 (垂直):</b> {corr['correlation_vertical']:.6f}<br>"
            stats_text += f"<b>相关性 (对角):</b> {corr['correlation_diagonal']:.6f}<br>"
        
        self.stats_text.setHtml(stats_text)
        
        # 4. 详细报告
        self.report_text.clear()
        self.report_text.append("=" * 60)
        self.report_text.append("详细评估报告")
        self.report_text.append("=" * 60)
        self.report_text.append("")
        
        self.append_dict_to_report(results, indent=0)
    
    def append_dict_to_report(self, data: Dict, indent: int = 0):
        """递归添加字典到报告"""
        for key, value in data.items():
            if key in ['encrypted_image', 'decrypted_image']:
                continue  # 跳过图像数据
            
            if isinstance(value, dict):
                self.report_text.append("  " * indent + f"{key}:")
                self.append_dict_to_report(value, indent + 1)
            elif isinstance(value, (list, tuple)):
                self.report_text.append("  " * indent + f"{key}: {value}")
            elif isinstance(value, float):
                self.report_text.append("  " * indent + f"{key}: {value:.6f}")
            else:
                self.report_text.append("  " * indent + f"{key}: {value}")
    
    def run_differential_attack_test(self):
        """执行差分攻击测试"""
        if self.current_algorithm is None or self.current_image is None:
            QMessageBox.warning(self, "警告", "请先选择算法和图像")
            return

        # 获取密钥
        key_text = self.key_input.text()
        try:
            key = int(key_text)
        except ValueError:
            key = key_text

        try:
            diff_result = Evaluator.test_differential_attack(
                self.current_algorithm.encrypt,
                self.current_image,
                key
            )
        except Exception as e:
            QMessageBox.critical(self, "错误", f"差分攻击测试失败: {str(e)}")
            return

        dlg = DifferentialAttackDialog(
            diff_result['plaintext_sensitivity'],
            diff_result['key_sensitivity'],
            self
        )
        dlg.exec()

    def show_histogram(self):
        """显示直方图"""
        if self.encrypted_image is None:
            return
        
        try:
            import matplotlib.pyplot as plt
            
            # 计算直方图
            hist = Evaluator.generate_histogram(self.encrypted_image)
            
            # 绘制直方图
            plt.figure(figsize=(10, 6))
            plt.bar(range(256), hist, color='blue', alpha=0.7)
            plt.title('加密图像直方图')
            plt.xlabel('像素值')
            plt.ylabel('频率')
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.show()
        
        except ImportError:
            QMessageBox.warning(
                self, 
                "警告", 
                "需要安装 matplotlib 才能显示直方图\n运行: pip install matplotlib"
            )
        except Exception as e:
            QMessageBox.critical(self, "错误", f"显示直方图失败: {str(e)}")
