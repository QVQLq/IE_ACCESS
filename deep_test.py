"""
深入测试系统各环节
"""
import json
import numpy as np
import sys
import os
import traceback

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# 测试配置
TEST_IMAGE_SIZE = (256, 256)
TEST_IMAGE_PATH = None  # 如果有测试图像可以设置路径


def convert_bytes_to_serializable(obj):
    if isinstance(obj, bytes):
        return list(obj)
    elif isinstance(obj, dict):
        return {k: convert_bytes_to_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [convert_bytes_to_serializable(item) for item in obj]
    return obj


def convert_lists_to_bytes(obj):
    if isinstance(obj, dict):
        return {k: convert_lists_to_bytes(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        if all(isinstance(x, int) and 0 <= x <= 255 for x in obj):
            return bytes(obj)
        return [convert_lists_to_bytes(item) for item in obj]
    return obj


def test_1_plugin_loading():
    """测试1: 插件加载"""
    print("\n" + "=" * 60)
    print("测试1: 插件加载")
    print("=" * 60)

    from core.plugin_loader import PluginLoader
    loader = PluginLoader()
    algorithms = loader.load_plugins()

    print(f"\n结果: 加载了 {len(algorithms)} 个算法")
    for name in algorithms.keys():
        print(f"  - {name}")

    # 测试每个算法的 get_default_key
    print("\n各算法默认密钥:")
    for name, algo in algorithms.items():
        default_key = algo.get_default_key()
        print(f"\n  [{name}]")
        print(f"    类型: {type(default_key)}")
        if default_key:
            for k, v in default_key.items():
                print(f"    {k}: {type(v).__name__} = {str(v)[:50]}...")
        else:
            print(f"    (无默认密钥)")

    return algorithms


def test_2_key_display_and_parse():
    """测试2: 密钥显示和解析"""
    print("\n" + "=" * 60)
    print("测试2: 密钥显示和解析 (模拟界面 on_algorithm_changed)")
    print("=" * 60)

    from core.plugin_loader import PluginLoader
    loader = PluginLoader()
    algorithms = loader.load_plugins()

    for name, algo in algorithms.items():
        print(f"\n--- 算法: {name} ---")

        # 模拟界面获取默认密钥
        default_key = algo.get_default_key()

        # 模拟界面 JSON 序列化 (on_algorithm_changed 中的逻辑)
        try:
            key_json = json.dumps(convert_bytes_to_serializable(default_key))
            print(f"  JSON 显示: {key_json[:80]}...")
            key_input.setText(key_json)  # 模拟 UI 设置
        except Exception as e:
            print(f"  [错误] JSON序列化失败: {e}")
            continue

        # 模拟界面解析密钥 (start_batch_evaluation 中的逻辑)
        try:
            parsed_key = json.loads(key_input.text())
            parsed_key = convert_lists_to_bytes(parsed_key)
            print(f"  解析后密钥类型: key={type(parsed_key.get('key') if isinstance(parsed_key, dict) else None)}")
        except Exception as e:
            print(f"  [错误] JSON解析失败: {e}")
            continue


# 模拟 UI 组件
class MockQLineEdit:
    def __init__(self):
        self._text = ""

    def setText(self, text):
        self._text = text
        print(f"  [UI] 设置密钥输入框文本: {text[:50]}...")

    def text(self):
        return self._text


key_input = MockQLineEdit()


def test_3_image_reading():
    """测试3: 图像读取"""
    print("\n" + "=" * 60)
    print("测试3: 图像读取")
    print("=" * 60)

    from utils.image_io import imread_chinese

    # 使用随机图像测试
    test_image = np.random.randint(0, 256, (256, 256, 3), dtype=np.uint8)
    print(f"\n创建测试图像: shape={test_image.shape}, dtype={test_image.dtype}")
    print(f"  像素范围: [{test_image.min()}, {test_image.max()}]")
    print(f"  总像素数: {test_image.size}")

    return test_image


def test_4_encryption_decryption(algorithms, test_image):
    """测试4: 加密解密流程"""
    print("\n" + "=" * 60)
    print("测试4: 完整加密解密流程 (模拟 BatchEvaluationThread)")
    print("=" * 60)

    results = []

    for name, algo in algorithms.items():
        print(f"\n--- 算法: {name} ---")

        try:
            # 1. 获取密钥 (模拟界面流程)
            default_key = algo.get_default_key()
            key_json = json.dumps(convert_bytes_to_serializable(default_key))
            key_input.setText(key_json)

            parsed_key = json.loads(key_input.text())
            parsed_key = convert_lists_to_bytes(parsed_key)

            print(f"  [1] 密钥准备完成")

            # 2. 加密 (模拟 controller._evaluate_single_image)
            encrypted = algo.encrypt(test_image.copy(), parsed_key)
            print(f"  [2] 加密完成: shape={encrypted.shape}, dtype={encrypted.dtype}")
            print(f"      像素范围: [{encrypted.min()}, {encrypted.max()}]")

            # 检查加密是否有效 (图像应该有变化)
            diff_count = np.sum(test_image != encrypted)
            change_rate = diff_count / test_image.size * 100
            print(f"      像素变化率: {change_rate:.2f}%")

            # 3. 解密
            decrypted = algo.decrypt(encrypted.copy(), parsed_key)
            print(f"  [3] 解密完成: shape={decrypted.shape}")

            # 4. 验证
            is_equal = np.array_equal(test_image, decrypted)
            print(f"  [4] 验证结果: {'成功 ✓' if is_equal else '失败 ✗'}")

            if not is_equal:
                diff = np.sum(test_image != decrypted)
                print(f"      不同像素数: {diff}")

            results.append({
                'name': name,
                'success': is_equal,
                'change_rate': change_rate
            })

        except Exception as e:
            print(f"  [错误] {str(e)}")
            traceback.print_exc()
            results.append({
                'name': name,
                'success': False,
                'error': str(e)
            })

    # 汇总
    print("\n" + "-" * 40)
    print("测试汇总:")
    for r in results:
        status = "成功" if r['success'] else f"失败: {r.get('error', '未知')}"
        change = f"变化率: {r.get('change_rate', 0):.1f}%" if 'change_rate' in r else ""
        print(f"  {r['name']}: {status} {change}")

    return results


def test_5_ui_flow_simulation():
    """测试5: 完整 UI 流程模拟"""
    print("\n" + "=" * 60)
    print("测试5: 完整 UI 流程模拟")
    print("=" * 60)

    from core.plugin_loader import PluginLoader
    from core.controller import Controller

    # 1. 加载算法
    loader = PluginLoader()
    algorithms = loader.load_plugins()

    # 2. 创建控制器
    controller = Controller()

    # 3. 选择第一个算法
    algo_name = list(algorithms.keys())[0]
    algo = algorithms[algo_name]
    controller.set_algorithm(algo)
    print(f"\n[UI模拟] 选择算法: {algo_name}")

    # 4. 获取并显示密钥
    default_key = algo.get_default_key()
    key_json = json.dumps(convert_bytes_to_serializable(default_key))
    key_input.setText(key_json)
    print(f"[UI模拟] 密钥显示在输入框")

    # 5. 解析密钥
    parsed_key = json.loads(key_input.text())
    parsed_key = convert_lists_to_bytes(parsed_key)
    controller.set_key(parsed_key)
    print(f"[UI模拟] 密钥已设置到控制器")

    # 6. 添加测试图像
    test_image = np.random.randint(0, 256, (128, 128), dtype=np.uint8)
    controller.add_image("test_image.png", test_image)
    print(f"[UI模拟] 添加测试图像: {test_image.shape}")

    # 7. 启动评估
    print(f"\n[UI模拟] 启动批量评估...")
    try:
        eval_thread = controller.start_batch_evaluation()
        print(f"[UI模拟] 评估线程已创建")

        # 直接运行 (不在新线程中)
        eval_thread.run()

        print(f"[UI模拟] 评估完成")
        print(f"[UI模拟] 结果数量: {len(controller.result_list)}")

        # 检查结果
        for i, result in enumerate(controller.result_list):
            print(f"\n  结果 {i+1}:")
            print(f"    图像: {result['image_name']}")
            print(f"    状态: {result['status']}")
            if result['status'] == 'success':
                print(f"    加密时间: {result['encryption_time']*1000:.2f} ms")
                print(f"    解密时间: {result['decryption_time']*1000:.2f} ms")
                print(f"    完美恢复: {result['perfect_recovery']}")
                print(f"    NPCR: {result['npcr']:.2f}%")
                print(f"    UACI: {result['uaci']:.2f}%")
            else:
                print(f"    错误: {result.get('error_message', '未知')}")

    except Exception as e:
        print(f"[错误] {str(e)}")
        traceback.print_exc()


def test_6_color_image():
    """测试6: 彩色图像处理"""
    print("\n" + "=" * 60)
    print("测试6: 彩色图像处理")
    print("=" * 60)

    from core.plugin_loader import PluginLoader

    loader = PluginLoader()
    algorithms = loader.load_plugins()

    # 创建彩色测试图像
    test_image = np.random.randint(0, 256, (128, 128, 3), dtype=np.uint8)
    print(f"\n测试图像: shape={test_image.shape}, dtype={test_image.dtype}")

    for name, algo in algorithms.items():
        try:
            default_key = algo.get_default_key()
            key_json = json.dumps(convert_bytes_to_serializable(default_key))
            parsed_key = json.loads(key_json)
            parsed_key = convert_lists_to_bytes(parsed_key)

            encrypted = algo.encrypt(test_image.copy(), parsed_key)
            decrypted = algo.decrypt(encrypted.copy(), parsed_key)

            is_equal = np.array_equal(test_image, decrypted)
            print(f"  {name}: {'成功 ✓' if is_equal else '失败 ✗'} (加密后shape={encrypted.shape})")

        except Exception as e:
            print(f"  {name}: 错误 - {str(e)[:50]}")


def test_7_entropy_calculation():
    """测试7: 熵计算"""
    print("\n" + "=" * 60)
    print("测试7: 熵计算 (Evaluator)")
    print("=" * 60)

    from core.plugin_loader import PluginLoader
    from core.evaluator import Evaluator

    loader = PluginLoader()
    algorithms = loader.load_plugins()

    # 创建测试图像
    test_image = np.random.randint(0, 256, (256, 256), dtype=np.uint8)

    for name, algo in list(algorithms.items())[:3]:  # 只测试前3个
        try:
            default_key = algo.get_default_key()
            key_json = json.dumps(convert_bytes_to_serializable(default_key))
            parsed_key = json.loads(key_json)
            parsed_key = convert_lists_to_bytes(parsed_key)

            encrypted = algo.encrypt(test_image.copy(), parsed_key)

            # 计算熵
            entropy_original = Evaluator.calculate_entropy(test_image)
            entropy_encrypted = Evaluator.calculate_entropy(encrypted)

            # 计算相关性
            corr_original = Evaluator.calculate_correlation_all_directions(test_image)
            corr_encrypted = Evaluator.calculate_correlation_all_directions(encrypted)

            print(f"\n  [{name}]")
            print(f"    原图熵: {entropy_original:.4f}")
            print(f"    密文熵: {entropy_encrypted:.4f}")
            print(f"    原图相关性(水平): {corr_original['correlation_horizontal']:.4f}")
            print(f"    密文相关性(水平): {corr_encrypted['correlation_horizontal']:.4f}")

        except Exception as e:
            print(f"\n  [{name}]")
            print(f"    错误: {str(e)}")


if __name__ == "__main__":
    print("=" * 60)
    print("ImageCrypto-Bench 系统深度测试")
    print("=" * 60)

    # 执行所有测试
    algorithms = test_1_plugin_loading()
    test_2_key_display_and_parse()
    test_image = test_3_image_reading()
    test_4_encryption_decryption(algorithms, test_image)
    test_5_ui_flow_simulation()
    test_6_color_image()
    test_7_entropy_calculation()

    print("\n" + "=" * 60)
    print("所有测试完成")
    print("=" * 60)
