"""Package configuration for img-characterize."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="img-characterize",
    version="0.3.1",
    author="Kodu AI",
    author_email="info@kodu.ai",
    description="Convert images to character art with support for multiple character sets and formats",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kodu-ai/characterize",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Graphics :: Graphics Conversion",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pillow>=10.0.0",
        "numpy>=1.24.0",
    ],
    entry_points={
        "console_scripts": [
            "img-characterize=img_characterize.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "img_characterize": [
            "fonts/*.ttf",
            "fonts/*.ttc",
        ],
    },
    keywords=[
        "image processing",
        "ascii art",
        "character art",
        "image conversion",
        "text art",
    ],
    project_urls={
        "Bug Reports": "https://github.com/kodu-ai/characterize/issues",
        "Source": "https://github.com/kodu-ai/characterize",
        "Documentation": "https://github.com/kodu-ai/characterize/blob/main/README.md",
    },
)