import sys
import importlib.util
from typing import Set

def is_stdlib_module(module_name: str) -> bool:
    """
    判断一个模块是否为Python标准库模块
    
    Args:
        module_name: 模块名称
    
    Returns:
        bool: 是否为标准库模块
    """
    if module_name in sys.stdlib_module_names:
        return True
        
    # 处理一些特殊情况
    spec = importlib.util.find_spec(module_name)
    if spec is None:
        return False
        
    location = spec.origin
    if location is None:
        return True  # 内建模块
        
    return ('site-packages' not in location and 
            'dist-packages' not in location and 
            'Python.framework' in location) 