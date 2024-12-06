# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='lib_mx_colab',  # Cambia por el nombre de tu librería
    version='0.1.1',
    author='IA (Sistema de Intres)',
    author_email='system.ai.of.interest@gmail.com',
    description='IA Sistema de Intres',
    long_description=open('README.md').read(),  # Asegúrate de tener este archivo
    long_description_content_type='text/markdown',
    url='https://www.youtube.com/@IA.Sistema.de.Interes',  # Opcional
    packages=find_packages(),  # Encuentra todos los paquetes y módulos
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests',
        'base64',
        'IPython',
    ],
)

