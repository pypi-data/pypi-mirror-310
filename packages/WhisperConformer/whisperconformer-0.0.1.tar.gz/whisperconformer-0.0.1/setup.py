from setuptools import setup, find_packages

setup(
    name='WhisperConformer', 
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'torch>=2.4.0',
        'typing_extensions>=4.12.2',
        'transformers>=4.42.4'
    ],
    author='thanakronN',  
    author_email='thanakron.nop@gmail.com',
    description='A library for Whisper Conformer model',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License', 
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',

)