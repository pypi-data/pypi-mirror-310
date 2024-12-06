from setuptools import setup, find_packages

setup(
    name="getmyqr",
    version="1.0",
    description="A simple QR code generator using a free API",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="MrFidal",
    author_email="mrfidal@proton.me",
    url="https://https://mrfidal.in/py/getmyqr",
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'getmyqr=getmyqr.cli:main',
        ],
    },
)
