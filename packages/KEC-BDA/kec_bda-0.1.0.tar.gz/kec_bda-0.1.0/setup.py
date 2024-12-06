from setuptools import setup, find_packages

setup(
    name="KEC_BDA",
    version="0.1.0",
    author="TVK-VIJAY",
    author_email="tvkvijay03@gmail.com",
    description="A simple Python module that prints 'Hello, World!'",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),  # Automatically find sub-packages like "my_module"
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
