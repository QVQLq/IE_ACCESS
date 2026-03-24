"""
ImageCrypto-Bench 主程序 (增强版)
集成 Controller 逻辑的批量评估系统
"""
import sys
from PySide6.QtWidgets import QApplication
from ui.main_window_enhanced import EnhancedMainWindow


def main():
    """主函数"""
    print("=" * 70)
    print("ImageCrypto-Bench - 图像加密算法批量评估系统")
    print("=" * 70)
    print()
    print("功能特性:")
    print("  ✓ 批量处理多个图像")
    print("  ✓ 实时更新评估结果")
    print("  ✓ 子线程运行防止界面卡死")
    print("  ✓ 详细的评估指标")
    print("  ✓ 结果导出功能")
    print()
    print("=" * 70)
    print()
    
    # 创建应用
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    # 创建主窗口
    window = EnhancedMainWindow()
    window.show()
    
    print("界面已启动")
    print("=" * 70)
    
    # 运行应用
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
