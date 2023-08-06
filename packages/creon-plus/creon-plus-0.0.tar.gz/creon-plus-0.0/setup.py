from setuptools import setup, find_packages

setup(
    name             = 'creon-plus',
    version          = '0.0',
    description      = '대신증권 Creon Plus API',
    long_description = open('README.md').read(),
    author           = 'jihogrammer',
    author_email     = 'jihogrammer@gmail.com',
    license          = 'MIT',
    packages         = find_packages(),
    install_requires = ['pywin32'],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows"
    ],
)
