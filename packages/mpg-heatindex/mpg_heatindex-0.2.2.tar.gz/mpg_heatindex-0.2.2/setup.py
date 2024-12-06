from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='mpg_heatindex',
    version='0.2.2',
    author='Disty Aparicio D\'Sousa',
    author_email='disty.sousa1996@gmail.com',
    description='This package use calculate heat index',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',  # Format README
    url='https://github.com/disty-apariciosousa/heatindex',
    packages=find_packages(),  # Mendeteksi semua sub-package
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
    install_requires=[
        'requests',
    ],
)
