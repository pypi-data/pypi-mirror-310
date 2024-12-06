from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()
    

setup(
    name='AdvanceForCaesar',
    version='2.0.3',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    license='MIT',
    author='Guo Zilu,Gong Yifu,Zhang Zhichen',
    author_email='sm37kx@126.com',
    description="An advanced Caesar cipher encryption tool that supports both encryption and decryption of text using a range of shift values.",

    install_requires=[
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
    ],
)
