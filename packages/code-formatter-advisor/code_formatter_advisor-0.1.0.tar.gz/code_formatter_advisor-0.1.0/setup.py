from setuptools import setup, find_packages

setup(
    name="code_formatter_advisor", 
    version="0.1.0", 
    author="Elisa",
    author_email="eeelisa122.tw@gmail.com",
    description="A tool to analyze code and provide formatting improvement suggestions",
    long_description=open("README.md", encoding="utf-8").read(), 
    long_description_content_type="text/markdown",
    url="https://github.com/Elisassa/code-formatter-advisor",  
    packages=find_packages(),  
    install_requires=[
        "groq==0.11.0",
        "boto3",
        "pydantic",
        "pytest",
        "flask",
        
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',  
)
