
from setuptools import setup, find_packages

setup(
    name='multi_bars',  # パッケージ名
    version='0.1.0',  # バージョン
    packages=find_packages(),
    description='MultiBars is a simple package for progress bar',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='DiamondGotCat',
    author_email='chii@kamu.jp',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)