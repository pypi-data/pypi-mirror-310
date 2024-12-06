from setuptools import setup, find_packages

setup(
    name= 'gpu-active',
    version='0.1.1',
    description='Utilities for GPU activation and data transfer in PyTorch.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Eman Gope',
    author_email='gopeeman87@gmail.com',
    url='https://github.com/dimeneman/get-gpu',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
    install_requires=[
        'torch>=1.7.0',
    ],
)
