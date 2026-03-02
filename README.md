# 图像加密与测评系统

基于 Python 3.10+ 和 PyQt6 的图像加密与测评桌面应用。

## 环境要求

- Python 3.10+
- PyQt6
- Pillow
- NumPy

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行方式

```bash
python main.py
```

## 功能说明

### 左侧输入区
- 选择图像：支持 png/jpg/bmp/tif 格式
- 图像预览缩略图
- 显示图像信息（尺寸、通道数、数据类型）

### 中间核心区
- 加密按钮：执行加密操作
- 日志框：显示操作日志（包括加密耗时、测评耗时、密文 MD5）
- 密文预览：显示加密后的图像
- 保存密文：将密文另存为文件
- 导出本次结果：将所有结果文件复制到时间戳目录
- 显示测评：查看测评结果

### 右侧参数区
- 加密参数配置
  - seed：随机种子（控制加密可复现性）
  - rounds：加密轮数（占位参数）
  - corr_sample_k：相关性采样数（占位参数）
  - npcr_mode：NPCR 模式（占位参数）
  - show_cipher_md5：是否在日志中显示密文 MD5
- 输出目录设置
- 默认参数：恢复到预设值
- 保存/加载配置：支持 JSON 格式

## 加密算法

本系统使用可复现的 XOR 加密算法：

1. 使用 `numpy.random.default_rng(seed)` 生成与输入图像同 shape 的 uint8 随机密钥流
2. 密文 = 明文 XOR 密钥流（逐元素按位异或）
3. 支持灰度图像 (H,W) 和 RGB 图像 (H,W,3)

## 测评指标

### 1. 信息熵 (Shannon Entropy)
- 计算密文的信息熵：H = -Σ(p_i × log₂(p_i))
- 理想密文熵值接近 8.0（对于 8-bit 图像）

### 2. 直方图分析
- 灰度图像：统计 0-255 像素值频次
- RGB 图像：分别统计 R/G/B 三通道的像素值分布

### 3. 相邻像素相关性
- 采样 K 对相邻像素（K = corr_sample_k，默认 5000）
- 三个方向：
  - H (水平)：(x,y) 与 (x,y+1)
  - V (垂直)：(x,y) 与 (x+1,y)
  - D (对角)：(x,y) 与 (x+1,y+1)
- 计算皮尔逊相关系数 r
- 生成散点图（X 轴为原位置像素值，Y 轴为相邻位置像素值）

**注意**：对于 RGB 图像，相关性分析会先转换为灰度图（使用标准权重：0.299×R + 0.587×G + 0.114×B），以简化计算并保证稳定性。

### 4. 明文敏感性（NPCR & UACI）
- 测试加密算法对明文微小变化的敏感性
- 扰动规则（可复现）：
  - 使用 `numpy.random.default_rng(seed + 999)` 决定扰动位置
  - 灰度图像：随机选择 (x,y)，令 `plain2[x,y] = (plain[x,y] + 1) % 256`
  - RGB 图像：随机选择 (x,y,c)，令 `plain2[x,y,c] = (plain[x,y,c] + 1) % 256`
- 使用相同参数分别加密 plain 和 plain2，得到 cipher 和 cipher2
- 计算指标：
  - NPCR (Number of Pixels Change Rate)：不同像素占比（%）
  - UACI (Unified Average Changing Intensity)：平均强度变化（%）
- 对于 RGB 图像，将所有通道的像素作为整体计算（H×W×C 个元素）
- 理想值：NPCR ≈ 99.6%，UACI ≈ 33.4%

## 复现性验证方法

### 验证步骤

1. 选择一张测试图像
2. 设置固定的 seed 值（例如 42）
3. 点击"加密"按钮，记录日志中的密文 MD5 值
4. 再次点击"加密"按钮（使用相同的图像和 seed）
5. 对比两次加密的密文 MD5 值

### 预期结果

- 相同的图像 + 相同的 seed → 密文 MD5 完全一致
- `enc_time_ms` 已写入 `outputs/results.json`
- 加密后 `results.json` 自动更新
- "显示测评"弹窗能正确读取并展示结果

### 示例

```bash
# 第一次加密
使用 seed=42
加密耗时：1.23 ms
密文 MD5：a1b2c3d4e5f6...

# 第二次加密（相同参数）
使用 seed=42
加密耗时：1.25 ms
密文 MD5：a1b2c3d4e5f6...  # 与第一次完全相同
```

## 输出文件

- `outputs/cipher.png`：加密后的密文图像
- `outputs/results.json`：测评结果数据（包含 enc_time_ms 和其他指标）
- `outputs/hist_plain.png`：明文直方图
- `outputs/hist_cipher.png`：密文直方图
- `outputs/corr_plain_H.png`：明文水平相关性散点图
- `outputs/corr_plain_V.png`：明文垂直相关性散点图
- `outputs/corr_plain_D.png`：明文对角相关性散点图
- `outputs/corr_cipher_H.png`：密文水平相关性散点图
- `outputs/corr_cipher_V.png`：密文垂直相关性散点图
- `outputs/corr_cipher_D.png`：密文对角相关性散点图

## 测评流程

1. 点击"加密"按钮后，系统自动执行以下步骤：
   - 执行加密并计时（enc_time_ms）
   - 保存密文图像
   - 调用 `EvaluationEngine.run()` 生成测评指标并计时（eval_time_ms）：
     - 信息熵
     - 直方图
     - 相邻像素相关性（H/V/D）
     - 明文敏感性（NPCR/UACI）
   - 将结果写入 `results.json`（包含 enc_time_ms 和 eval_time_ms）
   
2. 点击"显示测评"按钮查看详细结果：
   - 可视化图表（直方图、相关性散点图）
   - 扰动信息（位置、规则、原值/新值）
   - 所有测评指标数值（包括计时信息）

3. 点击"导出本次结果"按钮：
   - 将 outputs 目录下的所有结果文件复制到 `outputs/run_YYYYmmdd_HHMMSS/` 目录
   - 包含：cipher.png、results.json、所有直方图和相关性散点图
   - 便于论文插图和复现实验

## 复现性说明

- 相同的 seed 值确保：
  - 加密结果完全一致（密文 MD5 相同）
  - 扰动位置固定（seed + 999 决定）
  - NPCR/UACI 结果可重复
