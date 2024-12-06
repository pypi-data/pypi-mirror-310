from IPython import get_ipython
import psutil
import os


def log_memory_usage_after_execution(result=None):
    try:
        process = psutil.Process(os.getpid())
        current_memory = process.memory_info().rss / 1024 ** 2
        total_memory = psutil.virtual_memory().total / 1024 ** 2
        memory_percent = (current_memory / total_memory) * 100

        print(
            f"\r内存使用情况: 当前使用: {current_memory:.2f} MB 使用率: {memory_percent:.1f}%",
            end='', flush=True)
    except Exception as e:
        print(f"\r监控内存时出错: {e}", end='', flush=True)


def init():
    """初始化内存监控"""
    ipython = get_ipython()
    if ipython is None:
        print("警告: 未在IPython/Jupyter环境中运行")
        return

    if hasattr(ipython.events, 'callbacks'):
        ipython.events.callbacks['post_run_cell'] = []
    ipython.events.register('post_run_cell', log_memory_usage_after_execution)
