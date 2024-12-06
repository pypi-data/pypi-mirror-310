# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='lib_mx_colab',
    version='0.2.3',
    author='IA Sistema de Interes',  # Sin tildes
    author_email='system.ai.of.interest@gmail.com',
    description='IA Sistema de Interes',  # Sin tildes
    url='https://www.youtube.com/@IA.Sistema.de.Interes',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests',
        'IPython',
    ],
)



