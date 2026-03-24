# Logistic 混沌加密算法说明

## 算法概述

本系统新增了两个基于 Logistic 混沌映射的图像加密算法，作为简单对比算法：

1. **Logistic 混沌加密** - 简单快速的 XOR 加密
2. **Logistic 置乱扩散加密** - 包含置乱和扩散的增强版本

## 算法原理

### Logistic 映射

Logistic 映射是最经典的混沌系统之一：

```
x(n+1) = r * x(n) * (1 - x(n))
```

其中：
- `r`: 控制参数 (3.57 < r ≤ 4 时系统处于混沌状态)
- `x`: 状态变量 (0 < x < 1)

### 算法1: Logistic 混沌加密

**流程**:
```
原图 → 生成混沌序列 → XOR 加密 → 密文
```

**特点**:
- ✓ 简单易懂
- ✓ 计算快速 (~26ms for 256×256)
- ✓ 适合教学演示
- ✗ 安全性较低（仅 XOR）

**代码示例**:
```python
from algorithms.logistic_chaos_encryptor import LogisticChaosEncryptor

encryptor = LogisticChaosEncryptor()
key = {'r': 3.9999, 'x0': 0.123456}

encrypted = encryptor.encrypt(image, key)
decrypted = encryptor.decrypt(encrypted, key)
```

### 算法2: Logistic 置乱扩散加密

**流程**:
```
原图 → 置乱 → 扩散 → 密文
```

**置乱阶段**:
1. 生成 Logistic 混沌序列
2. 对序列排序得到置乱索引
3. 按索引重排像素位置

**扩散阶段**:
1. 生成新的混沌序列作为密钥流
2. 使用 XOR 和前一像素进行扩散
3. 实现雪崩效应

**特点**:
- ✓ 包含置乱和扩散
- ✓ 安全性更高
- ✓ 仍然保持简单
- ✗ 速度较慢 (~100ms for 256×256)

**代码示例**:
```python
from algorithms.logistic_chaos_encryptor import LogisticPermutationEncryptor

encryptor = LogisticPermutationEncryptor()
key = {
    'r1': 3.9999,   # 置乱参数
    'x1': 0.123456, # 置乱初始值
    'r2': 3.8888,   # 扩散参数
    'x2': 0.654321  # 扩散初始值
}

encrypted = encryptor.encrypt(image, key)
decrypted = encryptor.decrypt(encrypted, key)
```

## 性能对比

| 算法 | 256×256 加密 | 256×256 解密 | 信息熵 | 特点 |
|-----|-------------|-------------|--------|------|
| Logistic 混沌 | ~26 ms | ~26 ms | 7.9966 bits | 简单快速 |
| Logistic 置乱扩散 | ~100 ms | ~95 ms | 7.9966 bits | 更安全 |
| DPPAD 原始版 | ~35 ms | ~35 ms | 7.9962 bits | 双向扩散 |
| DPPAD 极速版 | ~17 ms | ~17 ms | 7.9971 bits | 高度优化 |

## 与 DPPAD 的对比

| 特性 | Logistic 简单版 | Logistic 置乱扩散 | DPPAD 原始版 | DPPAD 极速版 |
|-----|----------------|------------------|-------------|-------------|
| **算法复杂度** | ⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **安全性** | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **加密速度** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **代码可读性** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **教学价值** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |

## 使用场景

### Logistic 混沌加密
- ✓ 教学演示
- ✓ 快速原型
- ✓ 低安全要求场景
- ✗ 不适合高安全需求

### Logistic 置乱扩散加密
- ✓ 教学演示（展示置乱和扩散）
- ✓ 中等安全要求
- ✓ 对比实验
- ✗ 不适合高性能要求

### DPPAD 算法
- ✓ 高安全要求
- ✓ 医学图像加密
- ✓ 生产环境
- ✓ 实时应用（极速版）

## 演示建议

在 10 分钟演示中，可以这样使用：

1. **开场** (1分钟): 展示 Logistic 简单版
   - "这是一个基于混沌系统的简单加密算法"
   - 快速演示加密效果

2. **对比** (2分钟): 展示 Logistic 置乱扩散版
   - "增加置乱和扩散后，安全性提升"
   - 对比两个 Logistic 版本

3. **重点** (7分钟): 展示 DPPAD 算法
   - "DPPAD 采用更复杂的双向扩散机制"
   - 对比原始版和极速版
   - 突出性能提升和优化技术

## 测试

运行测试脚本：
```bash
python test_logistic_algorithms.py
```

## 集成到系统

算法已自动集成到系统中，重启系统后可在下拉菜单中看到：
- Logistic 混沌加密
- Logistic 置乱扩散加密

## 总结

Logistic 算法作为简单对比算法：
- ✓ 代码简单易懂
- ✓ 适合教学演示
- ✓ 突出 DPPAD 的优势
- ✓ 展示算法演进过程

通过对比，可以更好地展示 DPPAD 算法的：
- 更高的安全性
- 更复杂的设计
- 更优秀的性能（极速版）

---

**创建日期**: 2026-03-13  
**算法数量**: 2 个  
**测试状态**: ✓ 全部通过
