# -*- coding: utf-8 -*-
"""
测评结果对话框
"""
from pathlib import Path
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget,
    QTableWidgetItem, QHeaderView, QComboBox, QGroupBox, QScrollArea, QWidget
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap


class ResultsDialog(QDialog):
    def __init__(self, results, output_dir, parent=None):
        super().__init__(parent)
        self.results = results
        self.output_dir = Path(output_dir)
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("测评结果")
        self.setGeometry(150, 100, 900, 800)
        
        # 主布局
        main_layout = QVBoxLayout()
        
        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # 创建滚动内容容器
        scroll_content = QWidget()
        content_layout = QVBoxLayout(scroll_content)
        
        # 图片区
        image_group = QGroupBox("可视化图表")
        image_layout = QVBoxLayout()
        
        # 图片选择下拉框
        selector_layout = QHBoxLayout()
        selector_layout.addWidget(QLabel("选择图表："))
        self.image_selector = QComboBox()
        self.image_selector.addItems([
            "明文直方图",
            "密文直方图",
            "明文相关性-H",
            "明文相关性-V",
            "明文相关性-D",
            "密文相关性-H",
            "密文相关性-V",
            "密文相关性-D"
        ])
        self.image_selector.currentIndexChanged.connect(self.update_image)
        selector_layout.addWidget(self.image_selector)
        selector_layout.addStretch()
        image_layout.addLayout(selector_layout)
        
        # 图片显示区域
        self.label_image = QLabel()
        self.label_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_image.setMinimumHeight(450)
        self.label_image.setStyleSheet("border: 1px solid #ccc; background: #fff;")
        image_layout.addWidget(self.label_image)
        
        image_group.setLayout(image_layout)
        content_layout.addWidget(image_group)
        
        # 扰动信息区域
        if "meta" in self.results and "perturbation" in self.results["meta"]:
            pert_info = self.results["meta"]["perturbation"]
            if pert_info:
                pert_group = QGroupBox("明文敏感性测试 - 扰动信息")
                pert_layout = QVBoxLayout()
                
                pert_text = self.format_perturbation_info(pert_info)
                pert_label = QLabel(pert_text)
                pert_label.setStyleSheet("padding: 10px; background: #f9f9f9; border: 1px solid #ddd;")
                pert_label.setWordWrap(True)
                pert_layout.addWidget(pert_label)
                
                pert_group.setLayout(pert_layout)
                content_layout.addWidget(pert_group)
        
        # 结果表格
        table_group = QGroupBox("测评数据")
        table_layout = QVBoxLayout()
        
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["指标", "值"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setMinimumHeight(300)
        
        # 展平并填充数据
        flat_data = self.flatten_dict(self.results)
        self.table.setRowCount(len(flat_data))
        
        for i, (key, value) in enumerate(flat_data.items()):
            self.table.setItem(i, 0, QTableWidgetItem(key))
            self.table.setItem(i, 1, QTableWidgetItem(str(value)))
        
        table_layout.addWidget(self.table)
        table_group.setLayout(table_layout)
        content_layout.addWidget(table_group)
        
        # 设置滚动区域的内容
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)
        
        self.setLayout(main_layout)
        
        # 默认显示明文直方图
        self.update_image(0)
        
    def update_image(self, index):
        """更新显示的图片"""
        image_map = {
            0: "hist_plain.png",
            1: "hist_cipher.png",
            2: "corr_plain_H.png",
            3: "corr_plain_V.png",
            4: "corr_plain_D.png",
            5: "corr_cipher_H.png",
            6: "corr_cipher_V.png",
            7: "corr_cipher_D.png"
        }
        
        image_file = image_map.get(index, "hist_plain.png")
        image_path = self.output_dir / image_file
        
        if image_path.exists():
            pixmap = QPixmap(str(image_path))
            scaled_pixmap = pixmap.scaled(
                self.label_image.width() - 20,
                self.label_image.height() - 20,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.label_image.setPixmap(scaled_pixmap)
        else:
            self.label_image.setText(f"图片文件不存在：{image_path}")
        
    def flatten_dict(self, d, parent_key='', sep='.'):
        """展平嵌套字典"""
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(self.flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)

    
    def format_perturbation_info(self, pert_info):
        """格式化扰动信息"""
        if pert_info["type"] == "grayscale":
            x, y = pert_info["position"]
            text = (f"扰动类型：灰度图像\n"
                   f"扰动位置：({x}, {y})\n"
                   f"扰动规则：{pert_info['rule']}\n"
                   f"原始值：{pert_info['original_value']}\n"
                   f"新值：{pert_info['new_value']}")
        else:  # RGB
            x, y, c = pert_info["position"]
            text = (f"扰动类型：RGB 图像\n"
                   f"扰动位置：({x}, {y}, {pert_info['channel']})\n"
                   f"扰动通道：{pert_info['channel']}\n"
                   f"扰动规则：{pert_info['rule']}\n"
                   f"原始值：{pert_info['original_value']}\n"
                   f"新值：{pert_info['new_value']}")
        return text
