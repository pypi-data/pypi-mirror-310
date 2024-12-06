from setuptools import setup, find_packages

setup(
    name="maintenance_utils",  
    version="0.1.1",           
    packages=find_packages(),  
    install_requires=[],       
    description="Utility functions for vehicle service scheduling",
    long_description=open('README.md').read(),  
    long_description_content_type='text/markdown',
    author="Ajay Panwar",
    author_email="ajay.gemini90@gmail.com", 
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  
)
