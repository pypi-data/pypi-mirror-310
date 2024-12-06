# setup.py

from setuptools import setup, find_packages

setup(
    name='mpmg',  
    version='0.2.2',  
    description='A Minimum Price Markov Game modular environment', 
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Igor Sadoune',
    author_email='igor.sadoune@polymtl.ca',
    url='https://github.com/IgorSadoune/mpmg-python-package',
    license='MIT', 
    packages=find_packages(),
    install_requires=[
        'numpy',
        ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.10.12',
)
