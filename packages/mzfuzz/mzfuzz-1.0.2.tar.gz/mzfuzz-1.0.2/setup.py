from setuptools import setup, find_packages


setup(
    name="mzfuzz",
    version="1.0.2",
    description=("you can hacking fast!!!"),
    long_description="日常使用脚本函数合集，快速多线程，快速转excel，快速读excel",
    author="mzfuzz",
    author_email="1094067816@qq.com",
    url="https://github.com/shinyxiaoxia/mzfuzz",
    license="MIT Licence",
    packages=find_packages(),
    install_requires=['requests','phone','openpyxl','pandas','tqdm'],
)
