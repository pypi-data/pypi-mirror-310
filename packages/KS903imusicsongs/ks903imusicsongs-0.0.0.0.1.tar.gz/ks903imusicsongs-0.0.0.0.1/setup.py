

## **setup.py**
from setuptools import setup, find_packages
import pathlib

# 現在のファイルの場所を取得
here = pathlib.Path(__file__).parent.resolve()

# README.mdから説明を取得
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='KS903imusicsongs',
    version='0.0.0.0.1',
    description='Prototype sample of iSongs Music Media Player',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/NPO_KS903/KS903imusicsongs',
    author='NPO_KS_903.lnc',
    author_email='info@npo-ks903.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Topic :: Multimedia :: Sound/Audio :: Players',
    ],
    keywords='music player audio KS903',
    packages=find_packages(),
    install_requires=[
        'pygame',  # 音楽再生用ライブラリ
    ],
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'ks903imusicsongs=ks903imusicsongs.cli:main',  # コマンドライン実行用エントリーポイント
        ],
    },
)
