# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='lib_mx_colab',  # Cambia por el nombre de tu librería
    version='0.2.2',
    author='IA (Sistema de Interes)',
    author_email='system.ai.of.interest@gmail.com',
    description='IA Sistema de Interes',
    url='https://www.youtube.com/@IA.Sistema.de.Interes',  # Opcional
    packages=find_packages(),  # Encuentra todos los paquetes y módulos
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests',  # Paquete externo válido
        'IPython',   # Paquete externo válido
    ],
)


