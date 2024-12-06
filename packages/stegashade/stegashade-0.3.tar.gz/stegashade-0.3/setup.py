# setup.py

from setuptools import setup, find_packages

setup(
    name='stegashade',
    version='0.3',
        include_package_data=True,

    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'stegashade=stegashade.cli:main',
        ],
    },
        classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    install_requires=[
"Pillow",
"rich",
"numpy",
"cryptography"
    ],
    description='Stega Shade CLI is a user-friendly command-line interface tool designed for image-based steganography. With a focus on simplicity and security, it provides functionality to encode and decode messages into images, including password-protected encoding for enhanced privacy. The tool is built using Python and leverages robust algorithms to ensure data integrity and secrecy.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/merwin-asm/StegaShade',
    author='Merwin M',
    license='MIT'

)

