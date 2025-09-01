#!/usr/bin/env python3
"""
Setup script for Python Vibium Library
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), '..', 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "Python Vibium Library for UI Automation"

# Read requirements
def read_requirements():
    requirements_path = os.path.join(os.path.dirname(__file__), '..', 'requirements.txt')
    if os.path.exists(requirements_path):
        with open(requirements_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return []

setup(
    name="python-vibium",
    version="1.0.0",
    description="A comprehensive Python testing framework for UI automation built on top of Playwright",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="Vibium Team",
    author_email="team@vibium.com",
    url="https://github.com/vibium/python-vibium",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Quality Assurance",
        "Framework :: Pytest",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-html>=3.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
        ],
        "test": [
            "pytest>=7.0.0",
            "pytest-playwright>=0.4.0",
            "pytest-html>=3.0.0",
            "pytest-cov>=4.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "vibium=python_vibium.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords=[
        "testing",
        "automation",
        "ui",
        "web",
        "playwright",
        "selenium",
        "e-commerce",
        "quality-assurance",
        "test-automation",
    ],
    project_urls={
        "Bug Reports": "https://github.com/vibium/python-vibium/issues",
        "Source": "https://github.com/vibium/python-vibium",
        "Documentation": "https://vibium.readthedocs.io/",
    },
)
