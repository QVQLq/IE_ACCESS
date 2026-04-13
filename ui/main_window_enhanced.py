"""
增强版 PySide6 主窗口
集成 Controller 逻辑，支持批量处理
"""
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QComboBox, QLineEdit, QListWidget,
    QGroupBox, QTableWidget, QTableWidgetItem, QTextEdit,
    QFileDialog, QMessageBox, QProgressBar, QHeaderView,
    QDialog, QSplitter, QScrollArea, QFrame
)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QPixmap, QImage
import numpy as np
import cv2
import os
import io
from typing import Dict, Any, Tuple, Optional, List
from core.plugin_loader import PluginLoader
from core.controller import Controller
from core.evaluator import Evaluator
from ui.main_window_pyside6 import ImageListWidget, ImagePreviewLabel
from utils.image_io import imread_chinese

# Matplotlib导入
import matplotlib
matplotlib.use('Qt5Agg')  # 使用Qt后端
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题


class PlotDialog(QDialog):
    """图表显示对话框 - 用于显示直方图和相关性散点图"""

    def __init__(self, parent=None, title="图表", wide=False):
        super().__init__(parent)
        self.setWindowTitle(title)
        if wide:
            self.setGeometry(100, 100, 1400, 600)
        else:
            self.setGeometry(100, 100, 1100, 900)
        self.init_ui()

    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)

        # matplotlib图形会根据plot方法中的设置来调整
        self.figure = Figure(dpi=100)
        self.canvas = FigureCanvas(self.figure)
        
        # 添加工具栏
        self.toolbar = NavigationToolbar(self.canvas, self)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        
        # 关闭按钮
        close_btn = QPushButton("关闭")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)
    
    def plot_histograms(self, original_image: np.ndarray, encrypted_image: np.ndarray, 
                        decrypted_image: np.ndarray, image_name: str = ""):
        """
        绘制三幅图像的直方图对比
        
        Args:
            original_image: 原始图像
            encrypted_image: 加密图像
            decrypted_image: 解密图像
            image_name: 图像名称
        """
        self.figure.clear()

        # 判断图像类型（灰度或彩色）
        is_gray = len(original_image.shape) == 2 or original_image.shape[2] == 1

        if is_gray:
            # 灰度图像 - 横向3列
            self.figure.set_size_inches(9, 4)
            self._plot_gray_histograms(original_image, encrypted_image, decrypted_image, image_name)
        else:
            # 彩色图像 - 3x3 正方形
            self.figure.set_size_inches(8, 8)
            self._plot_color_histograms(original_image, encrypted_image, decrypted_image, image_name)
        
        self.canvas.draw()
    
    def _plot_gray_histograms(self, original, encrypted, decrypted, image_name):
        """绘制灰度图像的直方图"""
        ax1 = self.figure.add_subplot(1, 3, 1)
        ax2 = self.figure.add_subplot(1, 3, 2)
        ax3 = self.figure.add_subplot(1, 3, 3)

        # 原始图像直方图
        ax1.hist(original.flatten(), bins=256, range=(0, 256),
                 color='blue', alpha=0.7, edgecolor='none')
        ax1.set_title(f'原始图像 - {image_name}' if image_name else '原始图像', fontsize=12)
        ax1.set_xlabel('像素值')
        ax1.set_ylabel('频数', fontsize=10)
        ax1.set_xlim(0, 255)
        ax1.grid(True, alpha=0.3)

        # 加密图像直方图
        ax2.hist(encrypted.flatten(), bins=256, range=(0, 256),
                 color='red', alpha=0.7, edgecolor='none')
        ax2.set_title('加密图像', fontsize=12)
        ax2.set_xlabel('加密图像-像素值')
        ax2.set_ylabel('频数', fontsize=10)
        ax2.set_xlim(0, 255)
        ax2.grid(True, alpha=0.3)

        # 解密图像直方图
        ax3.hist(decrypted.flatten(), bins=256, range=(0, 256),
                 color='green', alpha=0.7, edgecolor='none')
        ax3.set_title('解密图像', fontsize=12)
        ax3.set_xlabel('解密图像-像素值')
        ax3.set_ylabel('频数', fontsize=10)
        ax3.set_xlim(0, 255)
        ax3.grid(True, alpha=0.3)

        self.figure.subplots_adjust(left=0.08, right=0.97, top=0.90, bottom=0.13, wspace=0.28)
    
    def _plot_color_histograms(self, original, encrypted, decrypted, image_name):
        """绘制彩色图像的直方图"""
        colors = ('red', 'green', 'blue')
        color_names = ('R', 'G', 'B')

        # 3行(原图、密文、解密)，3列(RGB通道)
        axes = []
        for i in range(3):  # 行
            for j in range(3):  # 列
                axes.append(self.figure.add_subplot(3, 3, i * 3 + j + 1))

        images = [original, encrypted, decrypted]
        titles = [
            f'原始图像 - {image_name}' if image_name else '原始图像',
            '加密图像', '解密图像'
        ]

        for row, (img, title) in enumerate(zip(images, titles)):
            for col, (color, name) in enumerate(zip(colors, color_names)):
                idx = row * 3 + col
                ax = axes[idx]

                # 计算直方图
                hist, _ = np.histogram(img[:, :, col].flatten(), bins=256, range=(0, 256))
                ax.plot(hist, color=color, linewidth=1.5)
                ax.fill_between(range(256), hist, color=color, alpha=0.3)

                if row == 0:
                    ax.set_title(f'{title} - {name}通道', fontsize=11)
                else:
                    ax.set_title(f'{name}通道', fontsize=11)
                ax.set_xlabel('像素值', fontsize=10)
                ax.set_ylabel('频数', fontsize=10)
                ax.set_xlim(0, 255)
                ax.grid(True, alpha=0.3)

        self.figure.subplots_adjust(left=0.06, right=0.97, top=0.95, bottom=0.07, hspace=0.40, wspace=0.28)
    
    def plot_correlation_scatter(self, image: np.ndarray, image_name: str = "",
                                  direction: str = "encrypted"):
        """
        绘制相邻像素相关性散点图

        Args:
            image: 输入图像
            image_name: 图像名称
            direction: 用于标题显示（"original"或"encrypted"）
        """
        self.figure.clear()

        if len(image.shape) == 3:
            img = image[:, :, 0]
        else:
            img = image

        h, w = img.shape
        sample_size = min(5000, h * w // 2)

        self.figure.set_size_inches(16, 6)

        fig_text = f'{image_name}  |  {"原始图像" if direction == "original" else "加密图像"} - 相邻像素相关性分析'
        self.figure.text(0.5, 0.97, fig_text, ha='center', va='top', fontsize=14, fontweight='bold')

        ax1 = self.figure.add_subplot(1, 3, 1)
        x_h = img[:, :-1].flatten()
        y_h = img[:, 1:].flatten()
        if len(x_h) > sample_size:
            indices = np.random.choice(len(x_h), sample_size, replace=False)
            x_h, y_h = x_h[indices], y_h[indices]
        ax1.scatter(x_h, y_h, s=1, alpha=0.5, c='blue')
        corr_h = np.corrcoef(x_h, y_h)[0, 1] if len(x_h) > 0 else 0
        ax1.set_title(f'水平方向  r={corr_h:.4f}', fontsize=12, pad=10)
        ax1.set_xlabel('像素值', fontsize=10)
        ax1.set_ylabel('像素值', fontsize=10)
        ax1.tick_params(axis='both', labelsize=9)
        ax1.grid(True, alpha=0.3)
        ax1.set_xlim(-5, 260)
        ax1.set_ylim(-5, 260)

        ax2 = self.figure.add_subplot(1, 3, 2)
        x_v = img[:-1, :].flatten()
        y_v = img[1:, :].flatten()
        if len(x_v) > sample_size:
            indices = np.random.choice(len(x_v), sample_size, replace=False)
            x_v, y_v = x_v[indices], y_v[indices]
        ax2.scatter(x_v, y_v, s=1, alpha=0.5, c='green')
        corr_v = np.corrcoef(x_v, y_v)[0, 1] if len(x_v) > 0 else 0
        ax2.set_title(f'垂直方向  r={corr_v:.4f}', fontsize=12, pad=10)
        ax2.set_xlabel('像素值', fontsize=10)
        ax2.set_ylabel('像素值', fontsize=10)
        ax2.tick_params(axis='both', labelsize=9)
        ax2.grid(True, alpha=0.3)
        ax2.set_xlim(-5, 260)
        ax2.set_ylim(-5, 260)

        ax3 = self.figure.add_subplot(1, 3, 3)
        x_d = img[:-1, :-1].flatten()
        y_d = img[1:, 1:].flatten()
        if len(x_d) > sample_size:
            indices = np.random.choice(len(x_d), sample_size, replace=False)
            x_d, y_d = x_d[indices], y_d[indices]
        ax3.scatter(x_d, y_d, s=1, alpha=0.5, c='red')
        corr_d = np.corrcoef(x_d, y_d)[0, 1] if len(x_d) > 0 else 0
        ax3.set_title(f'对角方向  r={corr_d:.4f}', fontsize=12, pad=10)
        ax3.set_xlabel('像素值', fontsize=10)
        ax3.set_ylabel('像素值', fontsize=10)
        ax3.tick_params(axis='both', labelsize=9)
        ax3.grid(True, alpha=0.3)
        ax3.set_xlim(-5, 260)
        ax3.set_ylim(-5, 260)

        self.figure.subplots_adjust(top=0.82, wspace=0.25, bottom=0.14, left=0.06, right=0.98)
        self.canvas.draw()


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


class EnhancedMainWindow(QMainWindow):
    """增强版主窗口 - 集成 Controller"""
    
    def __init__(self):
        super().__init__()
        
        # 核心组件
        self.plugin_loader = PluginLoader()
        self.controller = Controller()
        self.algorithms = {}
        
        # 当前状态
        self.current_image_index = -1
        
        self.init_ui()
        self.load_algorithms()
    
    def init_ui(self):
        """初始化界面"""
        self.setWindowTitle("ImageCrypto-Bench - 批量评估系统")
        self.setGeometry(100, 100, 1800, 1000)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        
        # 顶部控制区
        top_panel = self.create_top_panel()
        main_layout.addWidget(top_panel)
        
        # 中间内容区
        content_layout = QHBoxLayout()
        
        # 左侧图像列表
        left_panel = self.create_left_panel()
        content_layout.addWidget(left_panel, 1)
        
        # 中间预览区
        middle_panel = self.create_middle_panel()
        content_layout.addWidget(middle_panel, 2)
        
        # 右侧结果表格
        right_panel = self.create_right_panel()
        content_layout.addWidget(right_panel, 2)
        
        main_layout.addLayout(content_layout, 1)
        
        # 底部状态栏
        bottom_panel = self.create_bottom_panel()
        main_layout.addWidget(bottom_panel)
    
    def create_top_panel(self) -> QWidget:
        """创建顶部控制面板"""
        panel = QWidget()
        layout = QHBoxLayout(panel)
        
        # 算法选择
        layout.addWidget(QLabel("算法:"))
        self.algo_combo = QComboBox()
        self.algo_combo.setMinimumWidth(200)
        self.algo_combo.currentTextChanged.connect(self.on_algorithm_changed)
        layout.addWidget(self.algo_combo)
        
        layout.addSpacing(20)
        
        # 密钥输入
        layout.addWidget(QLabel("密钥:"))
        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("输入密钥...")
        self.key_input.setMinimumWidth(120)
        self.key_input.setStyleSheet("""
            QLineEdit {
                padding: 5px 10px;
                border: 1px solid #cccccc;
                border-radius: 3px;
            }
        """)
        layout.addWidget(self.key_input)
        
        layout.addSpacing(20)
        
        # 添加图像按钮
        self.add_images_btn = QPushButton("添加图像")
        self.add_images_btn.clicked.connect(self.add_images)
        layout.addWidget(self.add_images_btn)
        
        # 清空按钮
        self.clear_btn = QPushButton("清空列表")
        self.clear_btn.clicked.connect(self.clear_all)
        layout.addWidget(self.clear_btn)
        
        layout.addSpacing(20)
        
        # 开始运行按钮
        self.run_btn = QPushButton("开始运行")
        self.run_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 8px 20px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        self.run_btn.clicked.connect(self.start_batch_evaluation)
        self.run_btn.setEnabled(False)
        layout.addWidget(self.run_btn)
        
        # 停止按钮
        self.stop_btn = QPushButton("停止")
        self.stop_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 8px 20px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)
        self.stop_btn.clicked.connect(self.stop_evaluation)
        self.stop_btn.setEnabled(False)
        layout.addWidget(self.stop_btn)
        
        layout.addSpacing(20)
        
        # 直方图按钮
        self.histogram_btn = QPushButton("📊 直方图")
        self.histogram_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                font-size: 12px;
                padding: 8px 15px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        self.histogram_btn.clicked.connect(self.show_histograms)
        self.histogram_btn.setEnabled(False)
        layout.addWidget(self.histogram_btn)
        
        # 相关性散点图按钮
        self.correlation_btn = QPushButton("📈 相关性")
        self.correlation_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                font-size: 12px;
                padding: 8px 15px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #F57C00;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        self.correlation_btn.clicked.connect(self.show_correlation)
        self.correlation_btn.setEnabled(False)
        layout.addWidget(self.correlation_btn)

        # 差分攻击测试按钮
        self.diff_attack_btn = QPushButton("差分攻击测试")
        self.diff_attack_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                font-size: 12px;
                padding: 8px 15px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #F57C00;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        self.diff_attack_btn.clicked.connect(self.run_differential_attack_test)
        self.diff_attack_btn.setEnabled(False)
        layout.addWidget(self.diff_attack_btn)

        layout.addStretch()
        
        # 导出按钮
        self.export_btn = QPushButton("导出结果")
        self.export_btn.clicked.connect(self.export_results)
        self.export_btn.setEnabled(False)
        layout.addWidget(self.export_btn)
        
        return panel

    
    def create_left_panel(self) -> QWidget:
        """创建左侧图像列表面板"""
        panel = QGroupBox("图像列表")
        layout = QVBoxLayout(panel)
        
        # 图像列表
        self.image_list = ImageListWidget()
        self.image_list.currentRowChanged.connect(self.on_image_selected)
        layout.addWidget(self.image_list)
        
        # 统计信息
        self.image_count_label = QLabel("图像数量: 0")
        layout.addWidget(self.image_count_label)
        
        return panel
    
    def create_middle_panel(self) -> QWidget:
        """创建中间预览面板"""
        panel = QGroupBox("图像预览")
        layout = QHBoxLayout(panel)
        
        # 原图
        original_layout = QVBoxLayout()
        original_layout.addWidget(QLabel("原始图像", alignment=Qt.AlignCenter))
        self.original_preview = ImagePreviewLabel()
        original_layout.addWidget(self.original_preview)
        layout.addLayout(original_layout)
        
        # 密文
        encrypted_layout = QVBoxLayout()
        encrypted_layout.addWidget(QLabel("加密图像", alignment=Qt.AlignCenter))
        self.encrypted_preview = ImagePreviewLabel()
        encrypted_layout.addWidget(self.encrypted_preview)
        layout.addLayout(encrypted_layout)
        
        # 解密
        decrypted_layout = QVBoxLayout()
        decrypted_layout.addWidget(QLabel("解密图像", alignment=Qt.AlignCenter))
        self.decrypted_preview = ImagePreviewLabel()
        decrypted_layout.addWidget(self.decrypted_preview)
        layout.addLayout(decrypted_layout)
        
        return panel
    
    def create_right_panel(self) -> QWidget:
        """创建右侧结果表格面板"""
        panel = QGroupBox("评估结果")
        layout = QVBoxLayout(panel)
        
        # 结果表格
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(8)
        self.results_table.setHorizontalHeaderLabels([
            "图像名称", "状态", "原图熵", "密文熵", 
            "NPCR(%)", "UACI(%)", "加密时间(ms)", "完美恢复"
        ])
        
        # 设置表格属性
        header = self.results_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        for i in range(1, 8):
            header.setSectionResizeMode(i, QHeaderView.ResizeToContents)
        
        self.results_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.results_table.setSelectionMode(QTableWidget.SingleSelection)
        self.results_table.itemSelectionChanged.connect(self.on_result_selection_changed)
        
        layout.addWidget(self.results_table)
        
        # 详细信息
        detail_label = QLabel("详细信息:")
        layout.addWidget(detail_label)
        
        self.detail_text = QTextEdit()
        self.detail_text.setReadOnly(True)
        self.detail_text.setMaximumHeight(150)
        layout.addWidget(self.detail_text)
        
        return panel
    
    def create_bottom_panel(self) -> QWidget:
        """创建底部状态面板"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 5, 0, 0)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # 状态标签
        self.status_label = QLabel("就绪")
        self.status_label.setStyleSheet("padding: 5px; background-color: #e3f2fd;")
        layout.addWidget(self.status_label)
        
        return panel

    
    # ==================== 功能实现 ====================
    
    def load_algorithms(self):
        """加载算法插件"""
        try:
            self.algorithms = self.plugin_loader.load_plugins()
            
            if len(self.algorithms) == 0:
                QMessageBox.warning(self, "警告", "未找到任何算法插件！")
                return
            
            self.algo_combo.clear()
            self.algo_combo.addItems(list(self.algorithms.keys()))
            
            self.status_label.setText(f"成功加载 {len(self.algorithms)} 个算法")
        
        except Exception as e:
            QMessageBox.critical(self, "错误", f"加载算法失败: {str(e)}")
    
    def on_algorithm_changed(self, algo_name: str):
        """算法选择改变"""
        if algo_name in self.algorithms:
            algorithm = self.algorithms[algo_name]
            self.controller.set_algorithm(algorithm)

            # 显示默认密钥（以 JSON 格式）
            default_key = algorithm.get_default_key()
            import json
            if default_key is not None:
                # 处理 bytes 对象（JSON 不支持 bytes，需要转换为列表）
                def convert_bytes(obj):
                    if isinstance(obj, bytes):
                        return list(obj)
                    elif isinstance(obj, dict):
                        return {k: convert_bytes(v) for k, v in obj.items()}
                    elif isinstance(obj, (list, tuple)):
                        return [convert_bytes(item) for item in obj]
                    return obj
                key_json = json.dumps(convert_bytes(default_key))
                self.key_input.setText(key_json)
            else:
                self.key_input.clear()

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
                # 使用支持中文路径的读取函数
                image_data = imread_chinese(file_path)
                
                if image_data is not None:
                    # 添加到列表
                    self.image_list.image_paths.append(file_path)
                    self.image_list.addItem(os.path.basename(file_path))
                    
                    # 添加到控制器
                    self.controller.add_image(os.path.basename(file_path), image_data)
                else:
                    QMessageBox.warning(self, "警告", f"无法读取图像: {os.path.basename(file_path)}")
        
        self.update_image_count()
        self.update_run_button_state()
        
        if len(file_paths) > 0:
            self.status_label.setText(f"已添加 {len(file_paths)} 个图像")
    
    def clear_all(self):
        """清空所有"""
        self.image_list.clear_all()
        self.controller.clear_images()
        self.controller.clear_results()
        self.results_table.setRowCount(0)
        self.original_preview.clear_image()
        self.encrypted_preview.clear_image()
        self.decrypted_preview.clear_image()
        self.detail_text.clear()
        self.update_image_count()
        self.update_run_button_state()
        self.export_btn.setEnabled(False)
        self.status_label.setText("已清空")
    
    def on_image_selected(self, row: int):
        """图像选择改变"""
        self.current_image_index = row
        
        # 如果有评估结果，显示对应的图像
        results = self.controller.get_results()
        if 0 <= row < len(results):
            result = results[row]
            if result['status'] == 'success':
                self.original_preview.set_image(result['original_image'])
                self.encrypted_preview.set_image(result['encrypted_image'])
                self.decrypted_preview.set_image(result['decrypted_image'])
            else:
                # 只显示原图 - 使用支持中文路径的方法
                image_path = self.image_list.image_paths[row]
                image_data = imread_chinese(image_path)
                
                if image_data is not None:
                    self.original_preview.set_image(image_data)
                    self.encrypted_preview.clear_image()
                    self.decrypted_preview.clear_image()
    
    def update_image_count(self):
        """更新图像数量显示"""
        count = len(self.image_list.image_paths)
        self.image_count_label.setText(f"图像数量: {count}")
    
    def update_run_button_state(self):
        """更新运行按钮状态"""
        can_run = (
            self.controller.algorithm is not None and
            len(self.controller.image_list) > 0
        )
        self.run_btn.setEnabled(can_run)

    
    def start_batch_evaluation(self):
        """开始批量评估"""
        # 使用密钥输入框的密钥
        key_text = self.key_input.text()
        if not key_text:
            QMessageBox.warning(self, "警告", "请输入密钥！")
            return
        # 尝试解析为 JSON 字典，失败则传原始字符串
        try:
            import json
            key = json.loads(key_text)
            # 处理 bytes 转换回来的列表（JSON 不支持 bytes，解析后变成 list）
            def convert_lists_to_bytes(obj):
                # 检查是否是像是 bytes 的列表（全是 0-255 的整数）
                if isinstance(obj, dict):
                    return {k: convert_lists_to_bytes(v) for k, v in obj.items()}
                elif isinstance(obj, list):
                    # 检查是否应该转换为 bytes
                    if all(isinstance(x, int) and 0 <= x <= 255 for x in obj):
                        return bytes(obj)
                    return [convert_lists_to_bytes(item) for item in obj]
                return obj
            key = convert_lists_to_bytes(key)
        except Exception:
            key = key_text

        self.controller.set_key(key)
        
        # 清空之前的结果
        self.results_table.setRowCount(0)
        self.controller.clear_results()
        
        # 禁用控制按钮
        self.run_btn.setEnabled(False)
        self.add_images_btn.setEnabled(False)
        self.clear_btn.setEnabled(False)
        self.algo_combo.setEnabled(False)
        self.stop_btn.setEnabled(True)
        
        # 显示进度条
        self.progress_bar.setVisible(True)
        self.progress_bar.setMaximum(len(self.controller.image_list))
        self.progress_bar.setValue(0)
        
        try:
            # 启动评估线程
            self.eval_thread = self.controller.start_batch_evaluation()
            
            # 连接信号
            self.eval_thread.progress.connect(self.on_progress_update)
            self.eval_thread.image_started.connect(self.on_image_started)
            self.eval_thread.image_finished.connect(self.on_image_finished)
            self.eval_thread.all_finished.connect(self.on_all_finished)
            self.eval_thread.error.connect(self.on_evaluation_error)
            
            # 启动线程
            self.eval_thread.start()
            
            self.status_label.setText(f"开始批量评估... (使用密钥: {key})")
        
        except Exception as e:
            self.on_evaluation_error(-1, str(e))
            self.reset_ui_state()
    
    def stop_evaluation(self):
        """停止评估"""
        if self.eval_thread and self.eval_thread.isRunning():
            self.controller.stop_evaluation()
            self.status_label.setText("正在停止...")
            self.stop_btn.setEnabled(False)
    
    def on_progress_update(self, current: int, total: int, message: str):
        """进度更新"""
        if current >= 0 and total > 0:
            self.progress_bar.setValue(current + 1)
        self.status_label.setText(message)
    
    def on_image_started(self, index: int, image_name: str):
        """图像开始处理"""
        self.status_label.setText(f"处理: {image_name}")
    
    def on_image_finished(self, index: int, result: Dict[str, Any]):
        """图像处理完成 - 实时更新表格"""
        # 添加到结果列表
        self.controller.result_list.append(result)
        
        # 更新表格
        row = self.results_table.rowCount()
        self.results_table.insertRow(row)
        
        # 填充数据
        self.results_table.setItem(row, 0, QTableWidgetItem(result['image_name']))
        
        if result['status'] == 'error':
            self.results_table.setItem(row, 1, QTableWidgetItem("失败"))
            for col in range(2, 8):
                self.results_table.setItem(row, col, QTableWidgetItem("-"))
        else:
            self.results_table.setItem(row, 1, QTableWidgetItem("成功"))
            self.results_table.setItem(row, 2, QTableWidgetItem(f"{result['entropy_original']:.4f}"))
            self.results_table.setItem(row, 3, QTableWidgetItem(f"{result['entropy_encrypted']:.4f}"))
            self.results_table.setItem(row, 4, QTableWidgetItem(f"{result['npcr']:.2f}"))
            self.results_table.setItem(row, 5, QTableWidgetItem(f"{result['uaci']:.2f}"))
            self.results_table.setItem(row, 6, QTableWidgetItem(f"{result['encryption_time']*1000:.2f}"))
            self.results_table.setItem(row, 7, QTableWidgetItem("是" if result['perfect_recovery'] else "否"))
        
        # 自动滚动到最新行
        self.results_table.scrollToBottom()
    
    def on_all_finished(self, results: list):
        """所有评估完成"""
        self.progress_bar.setVisible(False)
        self.reset_ui_state()
        
        success_count = sum(1 for r in results if r['status'] == 'success')
        total_count = len(results)
        
        # 获取整体统计信息
        overall_stats = None
        for result in results:
            if result['status'] == 'success' and 'overall_stats' in result:
                overall_stats = result['overall_stats']
                break
        
        # 显示状态
        if overall_stats:
            status_msg = (
                f"评估完成: {success_count}/{total_count} 成功 | "
                f"整体加密速度: {overall_stats['overall_encryption_speed']:.0f} 像素/秒"
            )
        else:
            status_msg = f"评估完成: {success_count}/{total_count} 成功"
        
        self.status_label.setText(status_msg)
        self.export_btn.setEnabled(True)
        
        # 启用直方图和相关性按钮
        success_count = sum(1 for r in results if r['status'] == 'success')
        if success_count > 0:
            self.histogram_btn.setEnabled(True)
            self.correlation_btn.setEnabled(True)
            self.diff_attack_btn.setEnabled(True)
        
        # 显示摘要对话框
        summary_msg = f"批量评估已完成！\n\n总图像数: {total_count}\n成功: {success_count}\n失败: {total_count - success_count}"
        
        if overall_stats:
            summary_msg += f"\n\n整体统计:"
            summary_msg += f"\n总像素数: {overall_stats['total_pixels']:,}"
            summary_msg += f"\n总加密时间: {overall_stats['total_encryption_time']:.3f} 秒"
            summary_msg += f"\n总解密时间: {overall_stats['total_decryption_time']:.3f} 秒"
            summary_msg += f"\n\n整体加密速度: {overall_stats['overall_encryption_speed']:.0f} 像素/秒"
            summary_msg += f"\n整体解密速度: {overall_stats['overall_decryption_speed']:.0f} 像素/秒"
        
        QMessageBox.information(self, "评估完成", summary_msg)
    
    def on_evaluation_error(self, index: int, error_message: str):
        """评估错误"""
        self.status_label.setText(f"错误: {error_message}")
        
        if index < 0:
            # 全局错误
            QMessageBox.critical(self, "错误", error_message)
            self.reset_ui_state()
    
    def on_result_selection_changed(self):
        """结果表格选择改变"""
        current_row = self.results_table.currentRow()
        if current_row < 0:
            return
        
        results = self.controller.get_results()
        if current_row >= len(results):
            return
        
        result = results[current_row]
        
        # 显示详细信息
        self.display_result_detail(result)
        
        # 显示图像
        if result['status'] == 'success':
            self.original_preview.set_image(result['original_image'])
            self.encrypted_preview.set_image(result['encrypted_image'])
            self.decrypted_preview.set_image(result['decrypted_image'])
    
    def display_result_detail(self, result: Dict[str, Any]):
        """显示结果详细信息"""
        self.detail_text.clear()
        
        if result['status'] == 'error':
            self.detail_text.append(f"图像: {result['image_name']}")
            self.detail_text.append(f"状态: 失败")
            self.detail_text.append(f"错误: {result['error_message']}")
            return
        
        # 格式化显示
        text = f"<b>图像:</b> {result['image_name']}<br>"
        text += f"<b>形状:</b> {result['image_shape']}<br>"
        text += f"<b>大小:</b> {result['image_size']:,} 像素<br>"
        text += "<br>"
        
        text += "<b>统计指标:</b><br>"
        text += f"  原图熵: {result['entropy_original']:.4f} bits<br>"
        text += f"  密文熵: {result['entropy_encrypted']:.4f} bits<br>"
        text += "<br>"
        
        text += "<b>安全指标:</b><br>"
        text += f"  NPCR: {result['npcr']:.4f}%<br>"
        text += f"  UACI: {result['uaci']:.4f}%<br>"
        text += "<br>"
        
        text += "<b>相关性 (密文):</b><br>"
        corr = result['correlation_encrypted']
        text += f"  水平: {corr['correlation_horizontal']:.6f}<br>"
        text += f"  垂直: {corr['correlation_vertical']:.6f}<br>"
        text += f"  对角: {corr['correlation_diagonal']:.6f}<br>"
        text += "<br>"
        
        text += "<b>性能 (单图):</b><br>"
        text += f"  加密时间: {result['encryption_time']*1000:.2f} ms<br>"
        text += f"  解密时间: {result['decryption_time']*1000:.2f} ms<br>"
        text += f"  加密速度: {result['encryption_speed']:.0f} 像素/秒<br>"
        text += f"  解密速度: {result['decryption_speed']:.0f} 像素/秒<br>"
        
        # 显示整体统计
        if 'overall_stats' in result:
            stats = result['overall_stats']
            text += "<br>"
            text += "<b>整体统计 (所有图像):</b><br>"
            text += f"  总图像数: {stats['total_images']}<br>"
            text += f"  总像素数: {stats['total_pixels']:,}<br>"
            text += f"  总加密时间: {stats['total_encryption_time']:.3f} 秒<br>"
            text += f"  总解密时间: {stats['total_decryption_time']:.3f} 秒<br>"
            text += f"  <b>整体加密速度: {stats['overall_encryption_speed']:.0f} 像素/秒</b><br>"
            text += f"  <b>整体解密速度: {stats['overall_decryption_speed']:.0f} 像素/秒</b><br>"
        
        text += "<br>"
        text += "<b>解密质量:</b><br>"
        text += f"  完美恢复: {'是' if result['perfect_recovery'] else '否'}<br>"
        text += f"  MSE: {result['mse']:.6f}<br>"
        
        self.detail_text.setHtml(text)
    
    def reset_ui_state(self):
        """重置UI状态"""
        self.run_btn.setEnabled(True)
        self.add_images_btn.setEnabled(True)
        self.clear_btn.setEnabled(True)
        self.algo_combo.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.progress_bar.setVisible(False)
        # 禁用图表按钮（只有在有结果时才能使用）
        self.histogram_btn.setEnabled(False)
        self.correlation_btn.setEnabled(False)
        self.diff_attack_btn.setEnabled(False)
    
    def show_histograms(self):
        """显示直方图"""
        # 获取当前选中的结果
        current_row = self.results_table.currentRow()
        if current_row < 0:
            current_row = 0  # 默认显示第一个
        
        results = self.controller.get_results()
        if not results or current_row >= len(results):
            QMessageBox.warning(self, "警告", "没有可用的评估结果")
            return
        
        result = results[current_row]
        if result['status'] != 'success':
            QMessageBox.warning(self, "警告", "选中的图像评估失败，无法显示直方图")
            return
        
        # 创建对话框并显示直方图
        dialog = PlotDialog(self, title="图像直方图分析", wide=False)
        dialog.plot_histograms(
            result['original_image'],
            result['encrypted_image'],
            result['decrypted_image'],
            result['image_name']
        )
        dialog.exec()
    
    def show_correlation(self):
        """显示相关性散点图"""
        # 获取当前选中的结果
        current_row = self.results_table.currentRow()
        if current_row < 0:
            current_row = 0  # 默认显示第一个
        
        results = self.controller.get_results()
        if not results or current_row >= len(results):
            QMessageBox.warning(self, "警告", "没有可用的评估结果")
            return
        
        result = results[current_row]
        if result['status'] != 'success':
            QMessageBox.warning(self, "警告", "选中的图像评估失败，无法显示相关性散点图")
            return
        
        # 创建对话框并显示相关性散点图
        dialog = PlotDialog(self, title="相邻像素相关性分析", wide=True)
        dialog.plot_correlation_scatter(
            result['encrypted_image'],
            result['image_name'],
            direction="encrypted"
        )
        dialog.exec()

    def run_differential_attack_test(self):
        """执行差分攻击测试"""
        results = self.controller.get_results()
        row = self.results_table.currentRow()

        # 取当前选中图；无选中则取第一张成功图
        target = None
        if 0 <= row < len(results):
            target = results[row]
        else:
            target = next((r for r in results if r['status'] == 'success'), None)

        if target is None:
            QMessageBox.warning(self, "警告", "请先运行评估")
            return

        # 获取密钥
        key_text = self.key_input.text()
        try:
            import json
            key = json.loads(key_text)
            # 处理 bytes 转换回来的列表
            def convert_lists_to_bytes(obj):
                if isinstance(obj, dict):
                    return {k: convert_lists_to_bytes(v) for k, v in obj.items()}
                elif isinstance(obj, list):
                    if all(isinstance(x, int) and 0 <= x <= 255 for x in obj):
                        return bytes(obj)
                    return [convert_lists_to_bytes(item) for item in obj]
                return obj
            key = convert_lists_to_bytes(key)
        except Exception:
            key = key_text

        # 优先复用评估结果中的差分攻击数据
        diff = target.get('differential_attack_test')
        if diff is None:
            try:
                diff = Evaluator.test_differential_attack(
                    self.controller.algorithm.encrypt,
                    target['original_image'],
                    key
                )
            except Exception as e:
                QMessageBox.critical(self, "错误", f"差分攻击测试失败: {str(e)}")
                return

        dlg = DifferentialAttackDialog(
            diff['plaintext_sensitivity'],
            diff['key_sensitivity'],
            self
        )
        dlg.exec()

    def export_results(self):
        """导出结果"""
        if len(self.controller.result_list) == 0:
            QMessageBox.warning(self, "警告", "没有可导出的结果")
            return
        
        try:
            # 创建 results 主目录
            base_dir = "results"
            if not os.path.exists(base_dir):
                os.makedirs(base_dir)
            
            # 获取算法名称（清理特殊字符）
            algo_name = self.controller.algorithm.name if hasattr(self.controller.algorithm, 'name') else "Unknown"
            # 移除文件名中不允许的字符
            algo_name_clean = "".join(c for c in algo_name if c.isalnum() or c in (' ', '-', '_')).strip()
            algo_name_clean = algo_name_clean.replace(' ', '_')
            
            # 查找下一个可用的编号
            result_num = 1
            while True:
                result_dir = os.path.join(base_dir, f"result_{algo_name_clean}_{result_num}")
                if not os.path.exists(result_dir):
                    break
                result_num += 1
            
            # 创建结果目录
            os.makedirs(result_dir)
            
            # 导出文本报告
            summary = self.controller.export_results_summary()
            report_path = os.path.join(result_dir, "evaluation_report.txt")
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(summary)
            
            # 导出每个图像的结果（保存加密和解密图像）
            from utils.image_io import imwrite_chinese
            
            for idx, result in enumerate(self.controller.result_list):
                if result['status'] == 'success':
                    image_name = result['image_name']
                    base_name = os.path.splitext(image_name)[0]
                    
                    # 保存原始图像
                    original_path = os.path.join(result_dir, f"{base_name}_original.png")
                    imwrite_chinese(original_path, result['original_image'])
                    
                    # 保存加密图像
                    encrypted_path = os.path.join(result_dir, f"{base_name}_encrypted.png")
                    imwrite_chinese(encrypted_path, result['encrypted_image'])
                    
                    # 保存解密图像
                    decrypted_path = os.path.join(result_dir, f"{base_name}_decrypted.png")
                    imwrite_chinese(decrypted_path, result['decrypted_image'])
            
            # 显示成功消息
            self.status_label.setText(f"结果已导出到: {result_dir}")
            
            # 询问是否打开文件夹
            reply = QMessageBox.question(
                self,
                "导出成功",
                f"结果已成功导出到:\n{os.path.abspath(result_dir)}\n\n"
                f"包含内容:\n"
                f"- 评估报告 (evaluation_report.txt)\n"
                f"- 原始图像\n"
                f"- 加密图像\n"
                f"- 解密图像\n\n"
                f"是否打开文件夹？",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.Yes
            )
            
            if reply == QMessageBox.Yes:
                # 打开文件夹
                import subprocess
                import platform
                
                abs_path = os.path.abspath(result_dir)
                if platform.system() == 'Windows':
                    os.startfile(abs_path)
                elif platform.system() == 'Darwin':  # macOS
                    subprocess.Popen(['open', abs_path])
                else:  # Linux
                    subprocess.Popen(['xdg-open', abs_path])
        
        except Exception as e:
            QMessageBox.critical(self, "错误", f"导出失败: {str(e)}")
