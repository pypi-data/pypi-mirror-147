
import os
from setuptools import find_packages, setup

REQUIREMENTS_PATH = "requirements.txt"


with open(REQUIREMENTS_PATH) as our_file:
    required_libraries = our_file.read().splitlines()

setup(
    name="ekhusainov_cv_football_task_a",
    version="0.1.7",
    description="Test exercise. CV. Classification.",
    long_description="README.md",
    packages=["ekhusainov_cv_football_task_a"],
    author="Khusainov Eldar",
    install_requires=required_libraries,
    requirements=["requests<=2.21.0"],
    license="MIT",
    license_files="LICENSE",
    author_email="xluttiy@gmail.com",
    zip_safe=False,
)
