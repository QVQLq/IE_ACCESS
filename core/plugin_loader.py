"""
插件加载器
自动扫描并加载算法插件
"""
import os
import sys
import importlib.util
import inspect
from typing import Dict, Type
from core.base_encryptor import BaseEncryptor


class PluginLoader:
    """插件加载器"""
    
    def __init__(self, plugin_dir: str = "algorithms"):
        """
        初始化插件加载器
        
        Args:
            plugin_dir: 插件目录路径
        """
        self.plugin_dir = plugin_dir
    
    def load_plugins(self) -> Dict[str, BaseEncryptor]:
        """
        自动扫描并加载所有插件
        
        Returns:
            算法名称到算法对象实例的字典
        """
        plugins = {}
        
        if not os.path.exists(self.plugin_dir):
            print(f"警告: 插件目录 '{self.plugin_dir}' 不存在")
            return plugins
        
        # 遍历插件目录
        for filename in os.listdir(self.plugin_dir):
            if filename.endswith('.py') and not filename.startswith('__'):
                filepath = os.path.join(self.plugin_dir, filename)
                loaded_plugins = self._load_plugin_from_file(filepath, filename)
                plugins.update(loaded_plugins)
        
        print(f"成功加载 {len(plugins)} 个加密算法插件")
        return plugins
    
    def _load_plugin_from_file(self, filepath: str, filename: str) -> Dict[str, BaseEncryptor]:
        """
        从单个文件加载插件
        
        Args:
            filepath: 插件文件完整路径
            filename: 插件文件名
            
        Returns:
            从该文件加载的插件字典
        """
        plugins = {}
        
        try:
            # 动态导入模块
            module_name = filename[:-3]  # 去掉 .py 后缀
            spec = importlib.util.spec_from_file_location(module_name, filepath)
            if spec is None or spec.loader is None:
                print(f"警告: 无法加载模块 {filename}")
                return plugins
            
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)
            
            # 查找所有继承 BaseEncryptor 的类
            for name, obj in inspect.getmembers(module, inspect.isclass):
                # 检查是否是 BaseEncryptor 的子类（但不是 BaseEncryptor 本身）
                if (issubclass(obj, BaseEncryptor) and 
                    obj is not BaseEncryptor and
                    obj.__module__ == module_name):
                    
                    try:
                        # 实例化算法对象
                        instance = obj()
                        
                        # 使用类名作为算法名称
                        algorithm_name = name
                        
                        # 如果实例有 name 属性，优先使用
                        if hasattr(instance, 'name'):
                            algorithm_name = instance.name
                        
                        plugins[algorithm_name] = instance
                        print(f"  ✓ 加载插件: {algorithm_name} (来自 {filename})")
                        
                    except Exception as e:
                        print(f"  ✗ 实例化 {name} 失败: {str(e)}")
        
        except Exception as e:
            print(f"  ✗ 加载文件 {filename} 失败: {str(e)}")
        
        return plugins
    
    def get_plugin_classes(self) -> Dict[str, Type[BaseEncryptor]]:
        """
        获取所有插件类（不实例化）
        
        Returns:
            算法名称到算法类的字典
        """
        plugin_classes = {}
        
        if not os.path.exists(self.plugin_dir):
            return plugin_classes
        
        for filename in os.listdir(self.plugin_dir):
            if filename.endswith('.py') and not filename.startswith('__'):
                filepath = os.path.join(self.plugin_dir, filename)
                
                try:
                    module_name = filename[:-3]
                    spec = importlib.util.spec_from_file_location(module_name, filepath)
                    if spec is None or spec.loader is None:
                        continue
                    
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    for name, obj in inspect.getmembers(module, inspect.isclass):
                        if (issubclass(obj, BaseEncryptor) and 
                            obj is not BaseEncryptor and
                            obj.__module__ == module_name):
                            plugin_classes[name] = obj
                
                except Exception:
                    continue
        
        return plugin_classes
