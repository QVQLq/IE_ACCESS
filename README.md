# ImageCrypto-Bench

图像加密算法测评系统 - 插件化架构的图像加密算法测试与评估平台

## 项目简介

ImageCrypto-Bench 是一个基于插件化架构的图像加密算法测评系统，支持自动加载和测试多种图像加密算法。系统提供了完整的测评指标，包括加密性能、图像质量、安全性等多个维度。

## 主要特性

- **插件化架构**: 算法通过继承 `BaseEncryptor` 基类自动加载，无需修改主程序
- **自动发现**: `PluginLoader` 自动扫描 `algorithms/` 目录并加载所有算法
- **标准接口**: 统一的 `encrypt()` 和 `decrypt()` 接口，输入输出均为 NumPy 数组
- **自动测评**: 一键运行完整的算法测评流程
- **多维度指标**: 包括加密时间、PSNR、信息熵、NPCR/UACI等
- **图形界面**: 基于PyQt5的直观操作界面（可选）
- **易于扩展**: 只需编写算法类即可添加新算法

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 创建你的第一个算法

在 `algorithms/` 目录创建 `my_algo.py`:

```python
import numpy as np
from core.base_encryptor import BaseEncryptor

class MyEncryptor(BaseEncryptor):
    def encrypt(self, image_np: np.ndarray, key: int) -> np.ndarray:
        return np.bitwise_xor(image_np, key)
    
    def decrypt(self, cryptogram_np: np.ndarray, key: int) -> np.ndarray:
        return np.bitwise_xor(cryptogram_np, key)
```

### 3. 测试算法

```bash
python test_plugin_loader.py
```

### 4. 运行完整系统（可选）

```bash
python main.py
```

## 项目结构

```
ImageCrypto-Bench/
├── main.py                      # 主程序入口
├── test_plugin_loader.py        # 插件测试脚本
├── requirements.txt             # 依赖包列表
├── README.md                    # 项目说明
├── QUICK_START.md              # 快速开始指南
├── PLUGIN_GUIDE.md             # 插件开发指南
├── ARCHITECTURE.md             # 架构文档
├── core/                       # 核心模块
│   ├── __init__.py
│   ├── base_encryptor.py       # ⭐ 加密器抽象基类
│   ├── plugin_loader.py        # ⭐ 插件加载器
│   ├── base_algorithm.py       # (旧版兼容)
│   ├── plugin_manager.py       # (旧版兼容)
│   └── benchmark.py            # 测评引擎
├── algorithms/                 # 算法插件目录
│   ├── __init__.py
│   ├── simple_xor_encryptor.py # ⭐ XOR加密示例
│   └── example_xor.py          # (旧版示例)
├── ui/                         # 界面模块
│   ├── __init__.py
│   └── main_window.py          # 主窗口
└── utils/                      # 辅助工具
    ├── __init__.py
    └── image_utils.py          # 图像处理工具
```

⭐ 标记的是核心组件

## 核心API

### BaseEncryptor - 抽象基类

所有加密算法必须继承此类：

```python
from abc import ABC, abstractmethod
import numpy as np

class BaseEncryptor(ABC):
    @abstractmethod
    def encrypt(self, image_np: np.ndarray, key) -> np.ndarray:
        """加密图像"""
        pass
    
    @abstractmethod
    def decrypt(self, cryptogram_np: np.ndarray, key) -> np.ndarray:
        """解密图像"""
        pass
```

### PluginLoader - 插件加载器

自动扫描并加载算法插件：

```python
from core.plugin_loader import PluginLoader

# 创建加载器
loader = PluginLoader(plugin_dir="algorithms")

# 加载所有插件，返回 Dict[str, BaseEncryptor]
algorithms = loader.load_plugins()

# 使用算法
my_algo = algorithms["Simple XOR"]
encrypted = my_algo.encrypt(image, key=42)
decrypted = my_algo.decrypt(encrypted, key=42)
```

## 如何添加新算法

### 方法1: 最简单的方式

1. 在 `algorithms/` 目录下创建新的 Python 文件
2. 继承 `BaseEncryptor` 类并实现 `encrypt()` 和 `decrypt()` 方法
3. 运行测试或重启程序，系统会自动加载新算法

### 示例代码

```python
# algorithms/my_algorithm.py
import numpy as np
from core.base_encryptor import BaseEncryptor

class MyEncryptor(BaseEncryptor):
    def __init__(self):
        self.name = "My Algorithm"  # 可选：自定义算法名称
        self.description = "我的加密算法"
        self.version = "1.0.0"
    
    def encrypt(self, image_np: np.ndarray, key: int) -> np.ndarray:
        """
        加密图像
        
        Args:
            image_np: 输入图像的NumPy数组
            key: 加密密钥
            
        Returns:
            加密后的图像NumPy数组
        """
        # 实现你的加密逻辑
        encrypted = np.bitwise_xor(image_np, key)
        return encrypted
    
    def decrypt(self, cryptogram_np: np.ndarray, key: int) -> np.ndarray:
        """
        解密图像
        
        Args:
            cryptogram_np: 加密图像的NumPy数组
            key: 解密密钥
            
        Returns:
            解密后的图像NumPy数组
        """
        # 实现你的解密逻辑
        decrypted = np.bitwise_xor(cryptogram_np, key)
        return decrypted
```

### 方法2: 使用旧版API（兼容）

也可以继承 `BaseAlgorithm` 类（旧版接口，仍然支持）：

```python
from core.base_algorithm import BaseAlgorithm

class MyAlgorithm(BaseAlgorithm):
    def encrypt(self, image: np.ndarray, **kwargs) -> np.ndarray:
        # 实现加密
        pass
    
    def decrypt(self, encrypted_image: np.ndarray, **kwargs) -> np.ndarray:
        # 实现解密
        pass
```

## 测评指标

系统提供以下测评指标：

1. **性能指标**
   - 加密时间
   - 解密时间

2. **质量指标**
   - PSNR (峰值信噪比)

3. **安全性指标**
   - 信息熵 (原始图像 vs 加密图像)
   - 直方图均匀性 (卡方检验)
   - 相邻像素相关性 (水平、垂直、对角)
   - NPCR (像素变化率)
   - UACI (平均变化强度)

## 使用说明

### 命令行测试

```bash
# 测试插件加载和基本功能
python test_plugin_loader.py
```

### 图形界面（可选）

1. 启动程序后，从左侧面板选择算法
2. 点击"加载图像"选择要加密的图像
3. 点击"加密"按钮进行加密
4. 点击"解密"按钮进行解密
5. 点击"运行完整测评"查看详细测评结果

### 编程方式使用

```python
import numpy as np
from core.plugin_loader import PluginLoader

# 加载所有算法
loader = PluginLoader()
algorithms = loader.load_plugins()

# 选择算法
xor_algo = algorithms["Simple XOR"]

# 准备图像（示例）
image = np.random.randint(0, 256, (512, 512), dtype=np.uint8)

# 加密
key = 42
encrypted = xor_algo.encrypt(image, key)

# 解密
decrypted = xor_algo.decrypt(encrypted, key)

# 验证
assert np.array_equal(image, decrypted)
print("加密解密成功！")
```

## 文档

- [QUICK_START.md](QUICK_START.md) - 5分钟快速上手指南
- [PLUGIN_GUIDE.md](PLUGIN_GUIDE.md) - 详细的插件开发指南
- [ARCHITECTURE.md](ARCHITECTURE.md) - 系统架构文档

## 示例算法

系统包含以下示例算法：

1. **Simple XOR** - 简单XOR加密
   - 文件: `algorithms/simple_xor_encryptor.py`
   - 使用固定密钥进行XOR运算

2. **Advanced XOR** - 增强型XOR加密
   - 文件: `algorithms/simple_xor_encryptor.py`
   - 使用伪随机密钥序列进行XOR运算

你可以参考这些示例来开发自己的算法。

## 注意事项

- 确保图像格式为常见格式 (PNG, JPG, BMP, TIFF)
- 算法插件文件名不要以下划线开头
- 每个插件文件应包含一个继承 BaseAlgorithm 的类

## 许可证

MIT License
