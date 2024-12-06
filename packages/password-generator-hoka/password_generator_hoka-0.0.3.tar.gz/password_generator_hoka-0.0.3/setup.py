from setuptools import setup, find_packages

with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="password-generator-hoka",
    version="0.0.3",
    author="Oybek",
    author_email="tolqinovoybek92@gmail.com",
    long_description=long_description,
    url="https://github.com/HoKa03/password-generator",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "password_generate = password_generator:generate_password"
        ]
    }
)
