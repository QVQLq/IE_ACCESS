# DPPAD 加密算法快速使用指南

## 快速开始

### 1. 安装依赖

```bash
pip install numpy numba pillow
```

### 2. 基本使用

```python
from algorithms.dppad_encryptor import DPPAD_Encryptor
import numpy as np

# 创建加密器
encryptor = DPPAD_Encryptor()

# 准备图像（示例：随机生成）
image = np.random.randint(0, 256, (512, 512), dtype=np.uint8)

# 加密
encrypted = encryptor.encrypt(image, encryptor.default_key)

# 解密
decrypted = encryptor.decrypt(encrypted, encryptor.default_key)

# 验证
assert np.array_equal(image, decrypted)
print("✓ 加密解密成功！")
```

### 3. 使用真实图像

```python
from PIL import Image
import numpy as np
from algorithms.dppad_encryptor import DPPAD_Encryptor

# 加载图像
img = Image.open("your_image.jpg")
img_array = np.array(img)

# 创建加密器
encryptor = DPPAD_Encryptor()

# 加密
encrypted = encryptor.encrypt(img_array, encryptor.default_key)

# 保存加密图像
encrypted_img = Image.fromarray(encrypted)
encrypted_img.save("encrypted_image.jpg")

# 解密
decrypted = encryptor.decrypt(encrypted, encryptor.default_key)

# 保存解密图像
decrypted_img = Image.fromarray(decrypted)
decrypted_img.save("decrypted_image.jpg")
```

## 自定义密钥

### 默认密钥参数

```python
default_key = {
    'x1': -0.8,      # 置乱参数 1
    'r1': 0.9,       # 置乱参数 2
    'x3': -0.8,      # 2D-CGHM 初值 x
    'y3': -0.8,      # 2D-CGHM 初值 y
    'a1': 25,        # 2D-CGHM 控制参数 a
    'b1': 20,        # 2D-CGHM 控制参数 b
    'a': 15,         # 阿诺德扩散参数 a
    'b': 85          # 阿诺德扩散参数 b
}
```

### 修改密钥

```python
# 方法 1: 修改部分参数
custom_key = encryptor.default_key.copy()
custom_key['x1'] = -0.7
custom_key['a'] = 16

# 方法 2: 完全自定义
custom_key = {
    'x1': -0.75,
    'r1': 0.95,
    'x3': -0.85,
    'y3': -0.75,
    'a1': 26,
    'b1': 21,
    'a': 16,
    'b': 86
}

# 使用自定义密钥
encrypted = encryptor.encrypt(image, custom_key)
decrypted = encryptor.decrypt(encrypted, custom_key)
```

## 测试脚本

### 运行所有测试

```bash
# 基本功能测试
python test_dppad_optimized.py

# 性能基准测试
python benchmark_dppad.py

# 演示脚本
python demo_dppad.py

# 完整验证
python verify_dppad.py
```

## 性能参考

| 图像尺寸 | 加密时间 | 解密时间 |
|---------|---------|---------|
| 128×128 | ~4 ms | ~4 ms |
| 256×256 | ~18 ms | ~18 ms |
| 512×512 | ~78 ms | ~80 ms |
| 1024×1024 | ~418 ms | ~416 ms |

## 常见问题

### Q1: 首次运行很慢？
A: Numba 首次运行时会进行 JIT 编译，需要几秒钟。编译后的代码会被缓存，后续运行速度极快。

### Q2: 如何处理 RGB 图像？
A: 算法自动支持 RGB 图像，无需特殊处理：

```python
# RGB 图像会自动处理
rgb_image = np.random.randint(0, 256, (512, 512, 3), dtype=np.uint8)
encrypted = encryptor.encrypt(rgb_image, encryptor.default_key)
```

### Q3: 密钥参数范围？
A: 建议范围：
- x1, x3, y3: [-1, 1]
- r1: [0.5, 1.5]
- a1, b1: [15, 30]
- a, b: [10, 100]

### Q4: 如何提高性能？
A: 
1. 确保已安装 Numba
2. 首次运行后性能会自动提升（JIT 缓存）
3. 使用较小的图像尺寸
4. 批量处理时重用加密器实例

### Q5: 解密失败怎么办？
A: 检查：
1. 密钥是否完全一致
2. 图像数据类型是否为 uint8
3. 是否使用了相同的加密器实例

## 代码示例

### 示例 1: 批量加密

```python
from algorithms.dppad_encryptor import DPPAD_Encryptor
import numpy as np
import time

encryptor = DPPAD_Encryptor()
key = encryptor.default_key

# 批量加密多张图像
images = [
    np.random.randint(0, 256, (256, 256), dtype=np.uint8)
    for _ in range(10)
]

start = time.time()
encrypted_images = [
    encryptor.encrypt(img, key)
    for img in images
]
elapsed = time.time() - start

print(f"批量加密 10 张 256×256 图像耗时: {elapsed:.2f} 秒")
```

### 示例 2: 密钥敏感性测试

```python
from algorithms.dppad_encryptor import DPPAD_Encryptor
import numpy as np

encryptor = DPPAD_Encryptor()
image = np.random.randint(0, 256, (256, 256), dtype=np.uint8)

# 原始密钥
key1 = encryptor.default_key.copy()

# 微小改变
key2 = key1.copy()
key2['x1'] = key1['x1'] + 1e-10

# 加密
encrypted1 = encryptor.encrypt(image, key1)
encrypted2 = encryptor.encrypt(image, key2)

# 计算差异
diff_rate = (np.sum(encrypted1 != encrypted2) / image.size) * 100
print(f"密钥微小改变导致 {diff_rate:.2f}% 的密文像素不同")
```

### 示例 3: 性能测试

```python
from algorithms.dppad_encryptor import DPPAD_Encryptor
import numpy as np
import time

encryptor = DPPAD_Encryptor()
key = encryptor.default_key

# 测试不同尺寸
for size in [128, 256, 512]:
    image = np.random.randint(0, 256, (size, size), dtype=np.uint8)
    
    # 预热
    _ = encryptor.encrypt(image, key)
    
    # 测试
    start = time.perf_counter()
    encrypted = encryptor.encrypt(image, key)
    encrypt_time = time.perf_counter() - start
    
    print(f"{size}×{size}: {encrypt_time*1000:.2f} ms")
```

## 集成到系统

### 在测评系统中使用

```python
from core.plugin_loader import PluginLoader

# 加载所有算法
loader = PluginLoader()
algorithms = loader.load_plugins()

# 获取 DPPAD 算法
dppad = algorithms["DPPAD-IE 算法 (Vectorized & Numba)"]

# 使用
encrypted = dppad.encrypt(image, dppad.default_key)
decrypted = dppad.decrypt(encrypted, dppad.default_key)
```

## 技术支持

如有问题，请查看：
- `DPPAD_优化说明.md` - 优化技术详解
- `DPPAD_测试报告.md` - 完整测试报告
- 测试脚本源码

## 许可证

MIT License

---

**最后更新**: 2026-03-13  
**算法版本**: DPPAD-IE v2.0 (Optimized)
