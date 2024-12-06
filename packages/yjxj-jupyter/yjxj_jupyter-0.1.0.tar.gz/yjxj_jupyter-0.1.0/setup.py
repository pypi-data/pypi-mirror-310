from setuptools import setup, find_packages

setup(
    name="yjxj_jupyter",  # 修改这一行
    version="0.1.0",
    author="鼬君夏纪",
    author_email="youjunxiaji@gmail.com",
    description="Jupyter笔记本的内存监控工具",
    long_description=open("README.md", encoding='utf-8').read(),  # 添加 encoding='utf-8'
    long_description_content_type="text/markdown",
    documentation="https://github.com/youjunxiaji/jupyter-memory-monitor",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "ipython>=7.0.0",
        "psutil>=5.0.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: IPython",
        "Framework :: Jupyter",
    ],
    python_requires=">=3.6",
)