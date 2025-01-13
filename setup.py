from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="burphttp",
    version="0.1.2",
    author="kasusa",
    author_email="kasusaland@gmail.com",  # 请填写您的邮箱
    description="一个用于解析和发送HTTP请求的Python库，支持代理和保存响应",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cornradio/burphttprequest",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.25.0",
    ],
) 