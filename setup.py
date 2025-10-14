"""Setup configuration for strands-tools-community package."""

from pathlib import Path

from setuptools import find_packages, setup

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="strands-tools-community",
    version="0.2.0",
    description="Meta-package for Strands community tools (convenience wrapper for strands-deepgram, strands-hubspot, strands-teams)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Eray Keskin",
    author_email="eraykeskinmac@gmail.com",
    url="https://github.com/eraykeskinmac/strands-tools-community",
    packages=find_packages(),
    install_requires=[
        "strands-agents>=1.11.0",
        "strands-deepgram>=0.1.0",
        "strands-hubspot>=0.1.0",
        "strands-teams>=0.1.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "demo": [
            "prompt-toolkit>=3.0.0",
            "halo>=0.0.31",
            "colorama>=0.4.6",
        ],
    },
    python_requires=">=3.9",
    keywords=["strands", "ai", "agents", "deepgram", "hubspot", "teams", "speech-to-text", "crm", "adaptive-cards"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    project_urls={
        "Documentation": "https://github.com/eraykeskinmac/strands-tools-community",
        "Source": "https://github.com/eraykeskinmac/strands-tools-community",
        "Bug Reports": "https://github.com/eraykeskinmac/strands-tools-community/issues",
    },
)

