from setuptools import setup, find_packages

setup(
    name="joke_gen",  # Имя пакета (должно быть уникальным на PyPI)
    version="0.1.4",  # Версия пакета
    author="AndrewCo",
    description="A library for random jokes with translation support.",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),  # Автоматически находит пакеты в директории
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "certifi==2024.8.30",
        "charset-normalizer==3.4.0",
        "click==8.1.7",
        "colorama==0.4.6",
        "idna==3.10",
        "libretranslatepy==2.1.1",
        "lxml==5.3.0",
        "requests==2.32.3",
        "translate==3.6.1",
        "urllib3==2.2.3",
    ],
)
