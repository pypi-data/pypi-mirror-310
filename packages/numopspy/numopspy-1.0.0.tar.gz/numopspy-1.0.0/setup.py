from setuptools import setup

setup(
    name="numopspy",
    version="1.0.0",
    description="A comprehensive numerical operations library in pure Python",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Sai Pavan Velidandla",
    author_email="connectwithpavan@gmail.com",
    py_modules=["numopspy"],
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[],
)