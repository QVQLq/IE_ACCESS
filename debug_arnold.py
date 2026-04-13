"""
调试 Arnold 置乱算法 - 非正方形图像问题
"""
import numpy as np
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')


def arnold_transform(image, a, b, c, d):
    """单轮 Arnold Cat Map 变换"""
    H, W = image.shape[:2]
    result = np.empty_like(image)

    for y in range(H):
        for x in range(W):
            new_x = (a * x + b * y) % W
            new_y = (c * x + d * y) % H
            result[new_y, new_x] = image[y, x]

    return result


def arnold_inverse_transform(image, a, b, c, d):
    """Arnold Cat Map 逆变换"""
    H, W = image.shape[:2]
    result = np.empty_like(image)

    for y in range(H):
        for x in range(W):
            new_x = (d * x - b * y) % W
            new_y = (-c * x + a * y) % H
            result[new_y, new_x] = image[y, x]

    return result


def test_arnold_non_square():
    """测试 Arnold 变换对非正方形图像的处理"""
    print("=" * 60)
    print("测试 Arnold 变换 - 非正方形图像")
    print("=" * 60)

    test_cases = [
        ("正方形 64x64", (64, 64)),
        ("非正方形 100x200", (100, 200)),
        ("非正方形 200x100", (200, 100)),
        ("非正方形 50x150", (50, 150)),
    ]

    a, b, c, d = 1, 1, 1, 2

    for name, (H, W) in test_cases:
        print(f"\n--- {name} ---")

        # 创建测试图像
        original = np.arange(H * W, dtype=np.uint8).reshape(H, W)
        print(f"原始: shape={original.shape}, 首元素={original[0,0]}, 末元素={original[-1,-1]}")

        # Arnold 变换
        transformed = arnold_transform(original, a, b, c, d)
        print(f"变换后: shape={transformed.shape}")

        # Arnold 逆变换
        restored = arnold_inverse_transform(transformed, a, b, c, d)
        print(f"恢复: shape={restored.shape}")

        # 验证
        equal = np.array_equal(original, restored)
        print(f"验证: {'成功' if equal else '失败'}")

        if not equal:
            diff_count = np.sum(original != restored)
            print(f"差异像素: {diff_count} / {H*W}")


def test_gray_100x200():
    """详细测试 100x200 灰度图像"""
    print("\n" + "=" * 60)
    print("详细测试 100x200 灰度图像加解密")
    print("=" * 60)

    from algorithms.arnold_permutation_simple_diffusion import (
        Arnold_Permutation_Simple_Encryptor,
        arnold_n_rounds,
        arnold_n_rounds_inverse,
        simple_chain_diffusion_forward,
        simple_chain_diffusion_inverse
    )
    from algorithms.dppad_encryptor_ultra import generate_2d_cghm

    key = {'a': 1, 'b': 1, 'c': 1, 'd': 2, 'n': 3, 'x3': -0.8, 'y3': -0.8, 'a1': 25, 'b1': 20}

    # 创建测试图像
    original = np.random.randint(0, 256, (100, 200), dtype=np.uint8)
    print(f"原始图像: shape={original.shape}")

    # ========== 手动加解密流程 ==========
    print("\n--- 手动加密 ---")
    H, W = original.shape[:2]
    shape = original.shape

    # 1. Arnold 置乱
    permuted = arnold_n_rounds(original, key['a'], key['b'], key['c'], key['d'], key['n'])
    print(f"1. Arnold置乱: shape={permuted.shape}")

    # 2. 链式扩散
    L = original.size
    K1, _, _ = generate_2d_cghm(key['x3'], key['y3'], key['a1'], key['b1'], L)
    diffused = simple_chain_diffusion_forward(permuted.flatten().astype(np.int64), K1)
    encrypted = diffused.reshape(shape).astype(np.uint8)
    print(f"2. 链式扩散: shape={encrypted.shape}")

    print("\n--- 手动解密 ---")
    # 1. 链式逆向扩散
    restored = simple_chain_diffusion_inverse(encrypted.flatten().astype(np.int64), K1)
    restored = restored.reshape(shape).astype(np.uint8)
    print(f"1. 链式逆扩散: shape={restored.shape}, 是否等于permuted? {np.array_equal(restored, permuted)}")

    # 2. Arnold 逆置乱
    decrypted = arnold_n_rounds_inverse(restored, key['a'], key['b'], key['c'], key['d'], key['n'])
    print(f"2. Arnold逆置乱: shape={decrypted.shape}")

    # 验证
    equal = np.array_equal(original, decrypted)
    print(f"\n验证: {'成功' if equal else '失败'}")

    if not equal:
        diff_count = np.sum(original != decrypted)
        print(f"差异像素: {diff_count} / {original.size}")


def test_color_100x200():
    """详细测试 100x200 彩色图像"""
    print("\n" + "=" * 60)
    print("详细测试 100x200x3 彩色图像加解密")
    print("=" * 60)

    from algorithms.arnold_permutation_simple_diffusion import (
        Arnold_Permutation_Simple_Encryptor,
        arnold_n_rounds,
        arnold_n_rounds_inverse,
        simple_chain_diffusion_forward,
        simple_chain_diffusion_inverse
    )
    from algorithms.dppad_encryptor_ultra import generate_2d_cghm

    key = {'a': 1, 'b': 1, 'c': 1, 'd': 2, 'n': 3, 'x3': -0.8, 'y3': -0.8, 'a1': 25, 'b1': 20}

    # 创建测试图像
    original = np.random.randint(0, 256, (100, 200, 3), dtype=np.uint8)
    print(f"原始图像: shape={original.shape}")
    H, W = original.shape[:2]

    # ========== 逐通道手动加解密 ==========
    print("\n--- 逐通道手动加密 ---")
    channels = []
    for ch in range(3):
        channel = original[:, :, ch]

        # Arnold 置乱
        permuted = arnold_n_rounds(channel, key['a'], key['b'], key['c'], key['d'], key['n'])

        # 链式扩散
        L = channel.size
        K1, _, _ = generate_2d_cghm(key['x3'], key['y3'], key['a1'], key['b1'], L)
        diffused = simple_chain_diffusion_forward(permuted.flatten().astype(np.int64), K1)
        channels.append(diffused.reshape(H, W).astype(np.uint8))

    encrypted = np.stack(channels, axis=2)
    print(f"加密后: shape={encrypted.shape}")

    print("\n--- 逐通道手动解密 ---")
    channels_decrypted = []
    for ch in range(3):
        channel = encrypted[:, :, ch]

        # 链式逆向扩散
        L = channel.size
        K1, _, _ = generate_2d_cghm(key['x3'], key['y3'], key['a1'], key['b1'], L)
        restored = simple_chain_diffusion_inverse(channel.flatten().astype(np.int64), K1)
        restored = restored.reshape(H, W).astype(np.uint8)

        # Arnold 逆置乱
        restored = arnold_n_rounds_inverse(restored, key['a'], key['b'], key['c'], key['d'], key['n'])
        channels_decrypted.append(restored)

    decrypted = np.stack(channels_decrypted, axis=2)
    print(f"解密后: shape={decrypted.shape}")

    # 验证
    equal = np.array_equal(original, decrypted)
    print(f"\n验证: {'成功' if equal else '失败'}")

    if not equal:
        diff_count = np.sum(original != decrypted)
        print(f"差异像素: {diff_count} / {original.size}")


def test_using_algorithm_class():
    """使用算法类测试"""
    print("\n" + "=" * 60)
    print("使用 Arnold_Permutation_Simple_Encryptor 类测试")
    print("=" * 60)

    from algorithms.arnold_permutation_simple_diffusion import Arnold_Permutation_Simple_Encryptor

    algo = Arnold_Permutation_Simple_Encryptor()
    key = algo.default_key

    test_cases = [
        ("64x64 灰度", np.random.randint(0, 256, (64, 64), dtype=np.uint8)),
        ("64x64x3 彩色", np.random.randint(0, 256, (64, 64, 3), dtype=np.uint8)),
        ("100x200 灰度", np.random.randint(0, 256, (100, 200), dtype=np.uint8)),
        ("100x200x3 彩色", np.random.randint(0, 256, (100, 200, 3), dtype=np.uint8)),
    ]

    for name, image in test_cases:
        print(f"\n--- {name} ---")
        print(f"输入: shape={image.shape}")

        try:
            encrypted = algo.encrypt(image.copy(), key)
            decrypted = algo.decrypt(encrypted.copy(), key)

            equal = np.array_equal(image, decrypted)
            print(f"结果: {'成功' if equal else '失败'} (加密shape={encrypted.shape}, 解密shape={decrypted.shape})")

            if not equal:
                diff_count = np.sum(image != decrypted)
                print(f"差异像素: {diff_count} / {image.size}")

        except Exception as e:
            print(f"错误: {str(e)}")


if __name__ == "__main__":
    test_arnold_non_square()
    test_gray_100x200()
    test_color_100x200()
    test_using_algorithm_class()

    print("\n" + "=" * 60)
    print("调试完成")
    print("=" * 60)
