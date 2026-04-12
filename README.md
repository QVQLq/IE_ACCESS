# ImageCrypto-Bench

图像加密算法测评系统 — 基于插件化架构的图像加密算法测试与评估平台

---

## 1. 项目简介

ImageCrypto-Bench 是一个完整的图像加密算法测评平台，采用**插件化架构**设计，支持自动加载、测试和评估多种图像加密算法。系统提供直观的图形界面，可一键对多张图像运行加密/解密流程，并从统计学、安全性、性能等多个维度量化评估算法的质量。

### 适用场景

- 评估和对比不同图像加密算法的效果
- 论文/毕设中图像加密实验的数据生成
- 快速验证新加密算法的性能与安全性

---

## 2. 系统架构

```
main_enhanced.py                  # 主程序入口 (PySide6 GUI)
        │
        ▼
┌───────────────────────────────────────────────┐
│         ui/main_window_enhanced.py            │
│    (增强版主窗口：批量处理 + 图表可视化)          │
└──────────────────┬────────────────────────────┘
                   │
        ┌──────────▼──────────────┐
        │   core/controller.py     │
        │  (控制器：线程调度 + 结果汇总) │
        └──────────┬──────────────┘
                   │
    ┌──────────────┼──────────────┐
    ▼              ▼              ▼
┌─────────┐  ┌───────────┐  ┌──────────┐
│Plugin   │  │ Evaluator  │  │utils/    │
│Loader   │  │(评估指标)   │  │image_io  │
│(插件加载)│  │           │  │(中文路径) │
└────┬────┘  └───────────┘  └──────────┘
     │
     ▼
algorithms/               # 算法插件目录
  ├── logistic_chaos_encryptor.py   # Logistic 混沌加密 (对比算法)
  ├── dppad_encryptor_original.py   # DPPAD-IE 原始版本
  └── dppad_encryptor_ultra.py      # DPPAD-IE 优化版本 (Numba加速)
```

### 核心模块

| 模块 | 文件 | 功能 |
|------|------|------|
| 抽象基类 | `core/base_encryptor.py` | 定义加密器标准接口 |
| 插件加载器 | `core/plugin_loader.py` | 自动扫描并加载 `algorithms/` 下的所有算法 |
| 评估器 | `core/evaluator.py` | 计算熵、NPCR、UACI、相关性等指标 |
| 控制器 | `core/controller.py` | 协调加密流程，后台线程执行批量评估 |
| 图像工具 | `utils/image_io.py` | 支持中文路径的图像读写 |

---

## 3. 内置算法

| 算法 | 文件 | 说明 |
|------|------|------|
| Logistic 混沌加密 | `logistic_chaos_encryptor.py` | 基于 Logistic 映射的简单 XOR 加密，适合作为对比基线 |
| Logistic 置乱扩散加密 | `logistic_chaos_encryptor.py` | 包含置乱和扩散两阶段，比纯 XOR 更安全 |
| **DPPAD-IE 原始版本** | `dppad_encryptor_original.py` | 基于双向 Arnold 扩散的加密算法（Numba JIT 初版） |
| **DPPAD-IE 优化版本** | `dppad_encryptor_ultra.py` | 位运算 + 内存优化 + Numba JIT 加速，性能大幅提升 |

### DPPAD-IE 算法原理

DPPAD-IE (Diffusion-Permutation-Permutation-Arnold-Diffusion Image Encryption) 采用**置乱-扩散**双阶段架构：

```
明文图像
   │
   ▼  置乱阶段 (Permutation)
   │  使用 Logistic 混沌映射生成全局置乱索引，打乱像素位置
   │
   ▼  扩散阶段 1 (Diffusion Forward)
   │  2D-CGHM 生成混沌序列 K1/K2/K3
   │  Arnold 双向反馈扩散（从左到右 + 从右到左）
   │
   ▼  密文图像
```

解密过程严格逆转上述步骤。DPPAD-IE 原始版本使用 Numba `@njit` 装饰器编译 Python 循环；优化版本进一步引入位运算 (`& 255` 替代 `% 256`)、循环不变量提取 (`ab1 = a*b+1`)、原地覆写（减少内存分配），加密速度提升约 **5 倍**。

---

## 4. 测评指标

### 统计学指标

| 指标 | 说明 | 理想值 |
|------|------|--------|
| **信息熵** | 密文信息量，熵越高越接近随机 | 接近 8 bits（灰度图） |
| **直方图均匀性** | 卡方检验 p 值，越接近 1 表示分布越均匀 | → 1.0 |
| **相邻像素相关性** | 水平/垂直/对角方向的相关性 | → 0 |

### 安全指标

| 指标 | 说明 | 理想值 |
|------|------|--------|
| **NPCR** (像素改变率) | 改变一个像素后密文的变化比例 | > 99.6% |
| **UACI** (平均变化强度) | 变化的平均幅度 | > 33.3% |
| **密钥敏感性** | 密钥改变 1 bit 后密文的 NPCR/UACI | 高敏感性 |
| **明文敏感性** | 明文改变 1 pixel 后密文的 NPCR/UACI | 高敏感性 |

### 性能指标

| 指标 | 说明 |
|------|------|
| **加密/解密时间** | 多次运行取平均值、最小最大值 |
| **内存占用** | 使用 `tracemalloc` 追踪峰值内存 |
| **吞吐量** | 像素/秒、MB/秒 |

---

## 5. 安装与运行

### 环境要求

- Python 3.10+
- 依赖包（参见 `requirements.txt`）:
  - `numpy`, `opencv-python`, `scipy`
  - `PySide6`（图形界面）
  - `numba`（DPPAD 算法 JIT 加速）
  - `matplotlib`（图表可视化）

### 安装

```bash
pip install -r requirements.txt
```

### 运行

```bash
python main_enhanced.py
```

图形界面将自动启动。首次运行会扫描 `algorithms/` 目录并加载所有加密算法插件。

---

## 6. 使用方法

### 图形界面操作流程

```
1. 启动程序
   └─> 自动加载所有算法插件

2. 选择算法
   └─> 从下拉框选择（Logistic / DPPAD-IE 原始 / DPPAD-IE 优化）

3. 添加图像
   └─> 点击"添加图像"按钮，支持 PNG/JPG/BMP/TIFF 等格式
   └─> 支持中文路径

4. 开始运行
   └─> 点击"开始运行"，后台线程执行加密/解密
   └─> 实时显示进度和状态

5. 查看结果
   └─> 右侧表格显示每张图像的 NPCR、UACI、熵、加密时间等
   └─> 点击"直方图"按钮查看原图/密文/解密图直方图对比
   └─> 点击"相关性"按钮查看相邻像素散点图

6. 导出结果
   └─> 点击"导出结果"，保存加密图、解密图和评估报告
```

---

## 7. 添加新算法

在 `algorithms/` 目录下新建 Python 文件，继承 `BaseEncryptor` 即可：

```python
import numpy as np
from core.base_encryptor import BaseEncryptor

class MyEncryptor(BaseEncryptor):
    def __init__(self):
        super().__init__()
        self.name = "我的加密算法"
        self.default_key = {"seed": 42}

    def encrypt(self, image_np: np.ndarray, key) -> np.ndarray:
        # 实现加密逻辑
        return encrypted

    def decrypt(self, cryptogram_np: np.ndarray, key) -> np.ndarray:
        # 实现解密逻辑
        return decrypted
```

重启程序后，新算法将自动出现在界面下拉框中。

---

## 8. 项目文件结构

```
ImageCrypto-Bench/
├── main_enhanced.py                  # 主程序入口
├── requirements.txt                   # 依赖包
├── README.md                         # 本文件
├── core/                             # 核心模块
│   ├── __init__.py
│   ├── base_encryptor.py             # 抽象基类
│   ├── plugin_loader.py              # 插件加载器
│   ├── evaluator.py                  # 评估指标计算
│   └── controller.py                 # 控制器（线程调度）
├── algorithms/                       # 加密算法插件
│   ├── __init__.py
│   ├── logistic_chaos_encryptor.py   # Logistic 混沌系列
│   ├── dppad_encryptor_original.py    # DPPAD-IE 原始版本
│   └── dppad_encryptor_ultra.py       # DPPAD-IE 优化版本
├── ui/                               # 界面模块
│   ├── main_window_pyside6.py        # 基础窗口
│   └── main_window_enhanced.py       # 增强版（批量+图表）
└── utils/                            # 工具模块
    ├── __init__.py
    └── image_io.py                   # 中文路径图像读写
```

---

## 9. 相关文档

| 文档 | 内容 |
|------|------|
| `DPPAD_快速使用指南.md` | DPPAD-IE 快速上手操作步骤 |
| `DPPAD_版本说明.md` | DPPAD 原始版与优化版的技术差异 |
| `DPPAD_优化说明.md` | Numba 优化的详细技术细节 |
| `DPPAD_测试报告.md` | DPPAD-IE 算法测试结果 |
| `Logistic算法说明.md` | Logistic 混沌加密算法原理 |
| `答辩指南_10分钟.md` | 答辩参考 |
| `答辩PPT大纲.md` | PPT 制作参考 |

---

## 许可证

MIT License
