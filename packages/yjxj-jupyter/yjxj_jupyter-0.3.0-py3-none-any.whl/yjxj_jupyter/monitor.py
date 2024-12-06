from IPython import get_ipython
import psutil
import os
import time

_cell_start_time = None

def _pre_run_cell(*args, **kwargs):
    """记录单元格开始执行的时间"""
    global _cell_start_time
    _cell_start_time = time.time()

def log_memory_usage_after_execution(*args, **kwargs):
    """记录内存使用情况和单元格运行时间"""
    global _cell_start_time
    try:
        # 检查开始时间是否存在
        if _cell_start_time is None:
            execution_time = 0
        else:
            execution_time = time.time() - _cell_start_time
        
        process = psutil.Process(os.getpid())
        current_memory = process.memory_info().rss / 1024 ** 2
        total_memory = psutil.virtual_memory().total / 1024 ** 2
        memory_percent = (current_memory / total_memory) * 100

        print(
            f"\r内存使用情况: 当前使用: {current_memory:.2f} MB 使用率: {memory_percent:.1f}% "
            f"单元格运行时间: {execution_time:.2f}秒",
            end='', flush=True)
    except Exception as e:
        print(f"\r监控内存时出错: {e}", end='', flush=True)
    finally:
        # 重置开始时间
        _cell_start_time = None

def init():
    """初始化内存监控"""
    ipython = get_ipython()
    if ipython is None:
        print("警告: 未在IPython/Jupyter环境中运行")
        return

    # 清理现有的回调
    if hasattr(ipython.events, 'callbacks'):
        for event in ['pre_run_cell', 'post_run_cell']:
            ipython.events.callbacks.setdefault(event, [])
            if event == 'pre_run_cell':
                ipython.events.callbacks[event] = [cb for cb in ipython.events.callbacks[event] 
                                                if cb.__name__ != '_pre_run_cell']
            else:
                ipython.events.callbacks[event] = [cb for cb in ipython.events.callbacks[event] 
                                                if cb.__name__ != 'log_memory_usage_after_execution']
    
    # 注册新的回调
    ipython.events.register('pre_run_cell', _pre_run_cell)
    ipython.events.register('post_run_cell', log_memory_usage_after_execution)
