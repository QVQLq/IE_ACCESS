# -*- coding: utf-8 -*-
"""
主窗口界面
"""
import os
import json
from pathlib import Path
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QLabel, QTextEdit, QLineEdit, QComboBox,
    QFileDialog, QMessageBox, QFormLayout, QGroupBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from core.image_processor import ImageProcessor
from core.encryptor import Encryptor
from core.evaluator import Evaluator
from ui.results_dialog import ResultsDialog
from utils.config import DEFAULT_PARAMS, save_config, load_config, compute_md5


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.image_processor = ImageProcessor()
        self.encryptor = Encryptor()
        self.evaluator = Evaluator()
        
        self.plain_image = None
        self.cipher_image = None
        self.image_path = None
        
        self.init_ui()
        self.load_default_params()
        
    def init_ui(self):
        self.setWindowTitle("图像加密与测评系统")
        self.setGeometry(100, 100, 1200, 700)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        
        # 左侧输入区
        left_panel = self.create_left_panel()
        main_layout.addWidget(left_panel, 1)
        
        # 中间核心区
        center_panel = self.create_center_panel()
        main_layout.addWidget(center_panel, 2)
        
        # 右侧参数区
        right_panel = self.create_right_panel()
        main_layout.addWidget(right_panel, 1)
        
    def create_left_panel(self):
        """创建左侧输入区"""
        group = QGroupBox("输入区")
        layout = QVBoxLayout()
        
        # 选择图像按钮
        self.btn_select_image = QPushButton("选择图像")
        self.btn_select_image.clicked.connect(self.select_image)
        layout.addWidget(self.btn_select_image)
        
        # 图像预览
        self.label_preview = QLabel("未选择图像")
        self.label_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_preview.setFixedSize(300, 300)
        self.label_preview.setStyleSheet("border: 1px solid #ccc; background: #f5f5f5;")
        layout.addWidget(self.label_preview)
        
        # 图像信息
        self.label_info = QLabel("图像信息：\n尺寸：-\n通道数：-\ndtype：-")
        self.label_info.setStyleSheet("padding: 10px; background: #fff; border: 1px solid #ddd;")
        layout.addWidget(self.label_info)
        
        layout.addStretch()
        group.setLayout(layout)
        return group
        
    def create_center_panel(self):
        """创建中间核心区"""
        group = QGroupBox("核心区")
        layout = QVBoxLayout()
        
        # 加密和显示测评按钮
        btn_layout = QHBoxLayout()
        self.btn_encrypt = QPushButton("加密")
        self.btn_encrypt.clicked.connect(self.encrypt_image)
        btn_layout.addWidget(self.btn_encrypt)
        
        self.btn_show_results = QPushButton("显示测评")
        self.btn_show_results.clicked.connect(self.show_results)
        btn_layout.addWidget(self.btn_show_results)
        layout.addLayout(btn_layout)
        
        # 日志框
        log_label = QLabel("日志：")
        layout.addWidget(log_label)
        self.text_log = QTextEdit()
        self.text_log.setReadOnly(True)
        self.text_log.setMaximumHeight(150)
        layout.addWidget(self.text_log)
        
        # 密文预览
        cipher_label = QLabel("密文预览：")
        layout.addWidget(cipher_label)
        self.label_cipher = QLabel("未生成密文")
        self.label_cipher.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_cipher.setFixedSize(400, 300)
        self.label_cipher.setStyleSheet("border: 1px solid #ccc; background: #f5f5f5;")
        layout.addWidget(self.label_cipher)
        
        # 保存密文按钮
        self.btn_save_cipher = QPushButton("保存密文")
        self.btn_save_cipher.clicked.connect(self.save_cipher)
        self.btn_save_cipher.setEnabled(False)
        layout.addWidget(self.btn_save_cipher)
        
        # 导出结果按钮
        self.btn_export_results = QPushButton("导出本次结果")
        self.btn_export_results.clicked.connect(self.export_results)
        self.btn_export_results.setEnabled(False)
        layout.addWidget(self.btn_export_results)
        
        layout.addStretch()
        group.setLayout(layout)
        return group
        
    def create_right_panel(self):
        """创建右侧参数区"""
        group = QGroupBox("参数区")
        layout = QVBoxLayout()
        
        # 参数表单
        form_layout = QFormLayout()
        
        self.input_seed = QLineEdit()
        form_layout.addRow("seed:", self.input_seed)
        
        self.input_rounds = QLineEdit()
        form_layout.addRow("rounds:", self.input_rounds)
        
        self.input_corr_sample_k = QLineEdit()
        form_layout.addRow("corr_sample_k:", self.input_corr_sample_k)
        
        self.combo_npcr_mode = QComboBox()
        self.combo_npcr_mode.addItems(["single_pixel_plus1", "flip_lsb"])
        form_layout.addRow("npcr_mode:", self.combo_npcr_mode)
        
        self.input_output_dir = QLineEdit()
        form_layout.addRow("output_dir:", self.input_output_dir)
        
        self.combo_show_md5 = QComboBox()
        self.combo_show_md5.addItems(["True", "False"])
        form_layout.addRow("show_cipher_md5:", self.combo_show_md5)
        
        layout.addLayout(form_layout)
        
        # 默认参数按钮
        self.btn_default_params = QPushButton("默认参数")
        self.btn_default_params.clicked.connect(self.load_default_params)
        layout.addWidget(self.btn_default_params)
        
        # 保存配置按钮
        self.btn_save_config = QPushButton("保存配置")
        self.btn_save_config.clicked.connect(self.save_config_file)
        layout.addWidget(self.btn_save_config)
        
        # 加载配置按钮
        self.btn_load_config = QPushButton("加载配置")
        self.btn_load_config.clicked.connect(self.load_config_file)
        layout.addWidget(self.btn_load_config)
        
        layout.addStretch()
        group.setLayout(layout)
        return group
        
    def log(self, message):
        """添加日志"""
        self.text_log.append(message)
        
    def select_image(self):
        """选择图像"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择图像",
            "",
            "图像文件 (*.png *.jpg *.jpeg *.bmp *.tif *.tiff)"
        )
        
        if file_path:
            try:
                self.plain_image = self.image_processor.load_image(file_path)
                self.image_path = file_path
                
                # 显示缩略图
                pixmap = QPixmap(file_path)
                scaled_pixmap = pixmap.scaled(
                    self.label_preview.size(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.label_preview.setPixmap(scaled_pixmap)
                
                # 显示图像信息
                shape = self.plain_image.shape
                if len(shape) == 2:
                    h, w = shape
                    channels = 1
                else:
                    h, w, channels = shape
                    
                info_text = f"图像信息：\n尺寸：{h}×{w}\n通道数：{channels}\ndtype：{self.plain_image.dtype}"
                self.label_info.setText(info_text)
                
                self.log(f"已加载图像：{file_path}")
                self.log(f"尺寸：{h}×{w}，通道数：{channels}")
                
            except Exception as e:
                QMessageBox.critical(self, "错误", f"加载图像失败：{str(e)}")
                
    def get_params(self):
        """获取当前参数"""
        return {
            "seed": int(self.input_seed.text()),
            "rounds": int(self.input_rounds.text()),
            "corr_sample_k": int(self.input_corr_sample_k.text()),
            "npcr_mode": self.combo_npcr_mode.currentText(),
            "output_dir": self.input_output_dir.text(),
            "show_cipher_md5": self.combo_show_md5.currentText() == "True"
        }
        
    def encrypt_image(self):
        """加密图像"""
        if self.plain_image is None:
            QMessageBox.warning(self, "警告", "请先选择图像")
            return
            
        try:
            params = self.get_params()
            output_dir = Path(params["output_dir"])
            output_dir.mkdir(parents=True, exist_ok=True)
            
            self.log("开始加密...")
            self.log(f"使用 seed={params['seed']}")
            
            # 执行加密（只计时 encrypt 本体）
            result = self.encryptor.encrypt(self.plain_image, params)
            self.cipher_image = result["cipher"]
            enc_time_ms = result["enc_time_ms"]
            
            self.log(f"加密耗时：{enc_time_ms:.2f} ms")
            
            # 计算并显示密文 MD5（可选）
            if params.get("show_cipher_md5", True):
                cipher_md5 = compute_md5(self.cipher_image)
                self.log(f"密文 MD5：{cipher_md5}")
            
            # 保存密文
            cipher_path = output_dir / "cipher.png"
            self.image_processor.save_image(self.cipher_image, str(cipher_path))
            self.log(f"密文已保存：{cipher_path}")
            
            # 显示密文预览
            pixmap = QPixmap(str(cipher_path))
            scaled_pixmap = pixmap.scaled(
                self.label_cipher.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.label_cipher.setPixmap(scaled_pixmap)
            self.btn_save_cipher.setEnabled(True)
            self.btn_export_results.setEnabled(True)
            
            # 自动生成测评结果
            self.log("自动生成测评结果...")
            results = self.evaluator.evaluate(
                self.plain_image,
                self.cipher_image,
                enc_time_ms,
                self.image_path,
                params
            )
            
            # 保存结果到 results.json
            results_path = output_dir / "results.json"
            with open(results_path, "w", encoding="utf-8") as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            self.log(f"测评结果已保存：{results_path}")
            self.log(f"测评耗时：{results['eval_time_ms']:.2f} ms")
            
            QMessageBox.information(self, "成功", "加密完成！测评结果已自动生成。")
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"加密失败：{str(e)}")
            self.log(f"错误：{str(e)}")
            
    def save_cipher(self):
        """保存密文"""
        if self.cipher_image is None:
            QMessageBox.warning(self, "警告", "没有可保存的密文")
            return
            
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "保存密文",
            "cipher.png",
            "PNG 图像 (*.png)"
        )
        
        if file_path:
            try:
                self.image_processor.save_image(self.cipher_image, file_path)
                self.log(f"密文已另存为：{file_path}")
                QMessageBox.information(self, "成功", "密文保存成功！")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"保存失败：{str(e)}")
                
    def show_results(self):
        """显示测评结果"""
        params = self.get_params()
        output_dir = params["output_dir"]
        results_path = Path(output_dir) / "results.json"
        
        if not results_path.exists():
            QMessageBox.warning(self, "警告", "请先加密生成测评结果")
            return
            
        try:
            with open(results_path, "r", encoding="utf-8") as f:
                results = json.load(f)
            
            dialog = ResultsDialog(results, output_dir, self)
            dialog.exec()
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"加载结果失败：{str(e)}")
            
    def load_default_params(self):
        """加载默认参数"""
        self.input_seed.setText(str(DEFAULT_PARAMS["seed"]))
        self.input_rounds.setText(str(DEFAULT_PARAMS["rounds"]))
        self.input_corr_sample_k.setText(str(DEFAULT_PARAMS["corr_sample_k"]))
        self.combo_npcr_mode.setCurrentText(DEFAULT_PARAMS["npcr_mode"])
        self.input_output_dir.setText(DEFAULT_PARAMS["output_dir"])
        self.combo_show_md5.setCurrentText(str(DEFAULT_PARAMS["show_cipher_md5"]))
        self.log("已恢复默认参数")
        
    def save_config_file(self):
        """保存配置到文件"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "保存配置",
            "config.json",
            "JSON 文件 (*.json)"
        )
        
        if file_path:
            try:
                params = self.get_params()
                save_config(params, file_path)
                self.log(f"配置已保存：{file_path}")
                QMessageBox.information(self, "成功", "配置保存成功！")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"保存配置失败：{str(e)}")
                
    def load_config_file(self):
        """从文件加载配置"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "加载配置",
            "",
            "JSON 文件 (*.json)"
        )
        
        if file_path:
            try:
                params = load_config(file_path)
                self.input_seed.setText(str(params["seed"]))
                self.input_rounds.setText(str(params["rounds"]))
                self.input_corr_sample_k.setText(str(params["corr_sample_k"]))
                self.combo_npcr_mode.setCurrentText(params["npcr_mode"])
                self.input_output_dir.setText(params["output_dir"])
                if "show_cipher_md5" in params:
                    self.combo_show_md5.setCurrentText(str(params["show_cipher_md5"]))
                self.log(f"配置已加载：{file_path}")
                QMessageBox.information(self, "成功", "配置加载成功！")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"加载配置失败：{str(e)}")

    
    def export_results(self):
        """导出本次结果到时间戳目录"""
        import shutil
        from datetime import datetime
        
        params = self.get_params()
        output_dir = Path(params["output_dir"])
        
        # 检查必要文件是否存在
        required_files = [
            "cipher.png",
            "results.json",
            "hist_plain.png",
            "hist_cipher.png",
            "corr_plain_H.png",
            "corr_plain_V.png",
            "corr_plain_D.png",
            "corr_cipher_H.png",
            "corr_cipher_V.png",
            "corr_cipher_D.png"
        ]
        
        missing_files = []
        for filename in required_files:
            if not (output_dir / filename).exists():
                missing_files.append(filename)
        
        if missing_files:
            QMessageBox.warning(
                self, 
                "警告", 
                f"以下文件不存在，请先完成加密和测评：\n" + "\n".join(missing_files)
            )
            return
        
        try:
            # 生成时间戳目录名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            export_dir = output_dir / f"run_{timestamp}"
            export_dir.mkdir(parents=True, exist_ok=True)
            
            # 复制所有结果文件
            copied_files = []
            for filename in required_files:
                src = output_dir / filename
                dst = export_dir / filename
                shutil.copy2(src, dst)
                copied_files.append(filename)
            
            self.log(f"结果已导出到：{export_dir}")
            self.log(f"导出文件数：{len(copied_files)}")
            
            QMessageBox.information(
                self, 
                "成功", 
                f"结果已导出到：\n{export_dir}\n\n共导出 {len(copied_files)} 个文件"
            )
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"导出失败：{str(e)}")
            self.log(f"导出错误：{str(e)}")
