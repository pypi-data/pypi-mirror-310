from setuptools import setup, find_packages

setup(
    name="mylatexlib-itmo-367",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[],  # Нет зависимостей
    description="A library for generating LaTeX tables and images.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/mylatexlib",
    author="Your Name",
    author_email="your.email@example.com",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
