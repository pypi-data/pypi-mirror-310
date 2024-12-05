from setuptools import setup, find_packages

setup(
    name='rbxlx-export',
    version='1.0.0',
    description='A tool to extract scripts from Roblox XML files.',
    author='Your Name',
    author_email='your.email@example.com',
    packages=find_packages(),
    install_requires=[
        'xmltodict>=0.12.0',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
)
