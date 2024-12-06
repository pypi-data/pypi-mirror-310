from setuptools import setup, find_packages

setup(
    name="bizfylabs",
    version="0.1.2", 
    author="Bizfy Labs",
    author_email="dm.bizfylabs@gmail.com",
    description="A large language model module named Yukti by Bizfy Labs",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/bizfylabs/bizfylabs",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.115.5",
        "uvicorn==0.32.1",
        "transformers==4.46.3",
        "torch==2.2.0",  
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
