"""
完整测试所有算法 - 找出问题
"""
import numpy as np
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from core.plugin_loader import PluginLoader
from core.evaluator import Evaluator


def test_all_algorithms():
    """测试所有算法在不同图像上的表现"""
    print("=" * 60)
    print("完整测试所有算法")
    print("=" * 60)

    loader = PluginLoader()
    algorithms = loader.load_plugins()

    # 测试用例
    test_images = [
        ("64x64灰度", np.random.randint(0, 256, (64, 64), dtype=np.uint8)),
        ("64x64彩色", np.random.randint(0, 256, (64, 64, 3), dtype=np.uint8)),
        ("100x200灰度", np.random.randint(0, 256, (100, 200), dtype=np.uint8)),
        ("100x200彩色", np.random.randint(0, 256, (100, 200, 3), dtype=np.uint8)),
        ("512x512灰度", np.random.randint(0, 256, (512, 512), dtype=np.uint8)),
        ("512x512彩色", np.random.randint(0, 256, (512, 512, 3), dtype=np.uint8)),
    ]

    results = {}

    for algo_name, algo in algorithms.items():
        results[algo_name] = {}
        key = algo.get_default_key()

        print(f"\n--- {algo_name} ---")

        for img_name, image in test_images:
            try:
                # 加密
                encrypted = algo.encrypt(image.copy(), key)

                # 解密
                decrypted = algo.decrypt(encrypted.copy(), key)

                # 验证
                success = np.array_equal(image, decrypted)

                results[algo_name][img_name] = "成功" if success else "失败"

                # 打印结果
                status = "✓" if success else "✗"
                print(f"  {img_name}: {status}")

                if not success:
                    diff = np.sum(image != decrypted)
                    print(f"    差异像素: {diff}/{image.size}")

            except Exception as e:
                results[algo_name][img_name] = f"错误: {str(e)[:30]}"
                print(f"  {img_name}: 错误 - {str(e)[:40]}")

    # 汇总
    print("\n" + "=" * 60)
    print("汇总")
    print("=" * 60)

    for algo_name, img_results in results.items():
        failures = [(k, v) for k, v in img_results.items() if v != "成功"]
        if failures:
            print(f"\n{algo_name}:")
            for img_name, status in failures:
                print(f"  {img_name}: {status}")


def test_with_ui_flow():
    """模拟 UI 流程测试"""
    print("\n" + "=" * 60)
    print("模拟 UI 流程测试")
    print("=" * 60)

    import json
    from core.plugin_loader import PluginLoader
    from core.controller import BatchEvaluationThread

    loader = PluginLoader()
    algorithms = loader.load_plugins()

    # 模拟 UI
    def convert_bytes(obj):
        if isinstance(obj, bytes):
            return list(obj)
        elif isinstance(obj, dict):
            return {k: convert_bytes(v) for k, v in obj.items()}
        return obj

    def convert_lists_to_bytes(obj):
        if isinstance(obj, dict):
            return {k: convert_lists_to_bytes(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            if all(isinstance(x, int) and 0 <= x <= 255 for x in obj):
                return bytes(obj)
            return [convert_lists_to_bytes(item) for item in obj]
        return obj

    # 选择 Arnold 置乱+简单扩散
    algo = algorithms["Arnold 置乱+简单扩散"]
    default_key = algo.get_default_key()

    # 模拟 UI: 显示密钥 -> 解析密钥
    key_json = json.dumps(convert_bytes(default_key))
    parsed_key = json.loads(key_json)
    parsed_key = convert_lists_to_bytes(parsed_key)

    print(f"解析后密钥类型检查:")
    for k, v in parsed_key.items():
        print(f"  {k}: {type(v).__name__}")

    # 测试非正方形图像
    test_image = np.random.randint(0, 256, (100, 200), dtype=np.uint8)
    print(f"\n测试图像: {test_image.shape}")

    try:
        encrypted = algo.encrypt(test_image.copy(), parsed_key)
        decrypted = algo.decrypt(encrypted.copy(), parsed_key)

        success = np.array_equal(test_image, decrypted)
        print(f"加密/解密: {'成功' if success else '失败'}")

    except Exception as e:
        print(f"错误: {str(e)}")


def test_original_vs_modified_key():
    """测试使用原始密钥 vs 解析后的密钥"""
    print("\n" + "=" * 60)
    print("原始密钥 vs 解析后密钥 测试")
    print("=" * 60)

    import json
    from core.plugin_loader import PluginLoader

    loader = PluginLoader()
    algorithms = loader.load_plugins()

    def convert_bytes(obj):
        if isinstance(obj, bytes):
            return list(obj)
        elif isinstance(obj, dict):
            return {k: convert_bytes(v) for k, v in obj.items()}
        return obj

    def convert_lists_to_bytes(obj):
        if isinstance(obj, dict):
            return {k: convert_lists_to_bytes(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            if all(isinstance(x, int) and 0 <= x <= 255 for x in obj):
                return bytes(obj)
            return [convert_lists_to_bytes(item) for item in obj]
        return obj

    test_image = np.random.randint(0, 256, (64, 64), dtype=np.uint8)

    for algo_name, algo in algorithms.items():
        key = algo.get_default_key()

        # 原始密钥测试
        try:
            enc1 = algo.encrypt(test_image.copy(), key)
            dec1 = algo.decrypt(enc1.copy(), key)
            success1 = np.array_equal(test_image, dec1)
        except Exception as e:
            success1 = f"错误: {str(e)[:30]}"
            enc1 = None

        # JSON 解析后密钥测试
        try:
            key_json = json.dumps(convert_bytes(key))
            parsed_key = json.loads(key_json)
            parsed_key = convert_lists_to_bytes(parsed_key)

            enc2 = algo.encrypt(test_image.copy(), parsed_key)
            dec2 = algo.decrypt(enc2.copy(), parsed_key)
            success2 = np.array_equal(test_image, dec2)
        except Exception as e:
            success2 = f"错误: {str(e)[:30]}"
            enc2 = None

        # 比较结果
        status = "一致" if success1 == success2 else "不一致！"
        enc_same = "相同" if enc1 is not None and enc2 is not None and np.array_equal(enc1, enc2) else "不同"

        print(f"{algo_name}:")
        print(f"  原始密钥: {success1}")
        print(f"  解析后密钥: {success2}")
        print(f"  加密结果: {enc_same}")
        print()


if __name__ == "__main__":
    test_all_algorithms()
    test_with_ui_flow()
    test_original_vs_modified_key()

    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)
