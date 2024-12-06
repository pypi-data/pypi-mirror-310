from setuptools import setup, find_packages

setup(
    name='jsnDB',
    version='1.0.2',
    packages=find_packages(),
    description='A lightweight JSON-based database.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
