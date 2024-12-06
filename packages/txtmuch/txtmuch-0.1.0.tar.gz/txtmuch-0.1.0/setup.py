from setuptools import setup, find_packages

setup(
    name="txtmuch",  
    version="0.1.0",  
    author="theoyu314159",  
    author_email="sladersyuyu@gmail.com",  # 作者聯絡方式
    description="A txt model,it is my first model,use for test.",  #
    long_description=open("readme.md", "r", encoding="utf-8").read(),  
    long_description_content_type="text/markdown",  
    url="https://github.com/theoyu314159/txtmuch/tree/main",  
    packages=find_packages(),  
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  
)

