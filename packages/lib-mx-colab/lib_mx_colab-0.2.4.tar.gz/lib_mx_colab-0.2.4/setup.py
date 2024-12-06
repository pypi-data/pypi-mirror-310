# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os

# Leer el contenido del README.md
def read_readme():
    try:
        with open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print("El archivo README.md no se encuentra en el directorio.")
        return ""  # Devuelve una cadena vacía si no se encuentra el archivo
    except Exception as e:
        print(f"Error al leer el archivo README.md: {e}")
        return ""  # Devuelve una cadena vacía en caso de otro error

setup(
    name='lib_mx_colab',
    version='0.2.4',
    author='IA Sistema de Interes',
    author_email='system.ai.of.interest@gmail.com',
    description='IA Sistema de Interes',
    long_description=read_readme(),  # Lee el README.md
    long_description_content_type='text/markdown',  # Especifica el formato
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


