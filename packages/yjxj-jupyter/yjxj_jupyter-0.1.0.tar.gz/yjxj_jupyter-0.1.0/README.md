# Jupyter Memory Monitor

一个简单的Jupyter笔记本内存监控工具，可以实时显示每个单元格执行后的内存使用情况。

## 功能特点

- 实时监控内存使用情况
- 自动显示每个单元格执行后的内存占用
- 显示系统总内存使用率
- 轻量级，无需额外配置

## 安装

```bash
pip install jupyter-memory-monitor
```

## 快速开始

在Jupyter笔记本中导入并初始化：

```python
import jupyter_memory_monitor
jupyter_memory_monitor.init()
```


初始化后，每次执行单元格都会在输出区域看到类似下面的信息：

内存使用情况: 当前使用: 256.45 MB 使用率: 12.3%


## 依赖要求

- Python >= 3.6
- IPython >= 7.0.0
- psutil >= 5.0.0

## 许可证

本项目采用 MIT 许可证

## 贡献指南

欢迎提交 Issue 和 Pull Request！

## 更新日志

### 0.1.0
- 首次发布
- 实现基本的内存监控功能