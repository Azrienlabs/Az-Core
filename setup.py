"""
Setup configuration for Azcore..
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = ""
if readme_file.exists():
    try:
        # Try UTF-8 with BOM first
        long_description = readme_file.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        # Fallback to UTF-8 without BOM
        long_description = readme_file.read_text(encoding="utf-8", errors="ignore")

# Core requirements (flexible versions for compatibility)
requirements = [
    "langchain>=1.0.0",
    "langchain-core>=1.0.0",
    "langchain-openai>=1.0.0",
    "langgraph>=1.0.0",
    "langgraph-checkpoint>=3.0.0",
    "openai>=2.0.0",
    "pydantic>=2.0.0",
    "pydantic-settings>=2.0.0",
    "python-dotenv>=1.0.0",
    "PyYAML>=6.0",
    "click>=8.0.0",
    "requests>=2.31.0",
    "numpy>=1.24.0",
]

setup(
    name="azcore",
    version="0.0.6",
    author="Azrienlabs team",
    author_email="info@azrianlabs.com",
    description="A professional hierarchical multi-agent framework built on python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Azrienlabs/Az-Flow",
    license="MIT",
    packages=find_packages(exclude=["tests", "tests.*", "examples", "examples.*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.12",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "mcp": [
            "langchain-mcp-adapters>=0.1.0",
        ],
        "rl": [
            "torch>=2.0.0",
            "sentence-transformers>=2.0.0",
            "scikit-learn>=1.0.0",
        ],
    },
    include_package_data=True,
    package_data={
        "azcore": ["py.typed"],
    },
    entry_points={
        "console_scripts": [
            "azcore=azcore.cli.__main__:main",
        ],
    },
    zip_safe=False,
    keywords="Multi-agent agents ai framework hierarchical azcore reinforcement-learning",
    project_urls={
        "Bug Reports": "https://github.com/Azrienlabs/Az-Flow/issues",
        "Source": "https://github.com/Azrienlabs/Az-Flow",
        "Documentation": "https://github.com/Azrienlabs/Az-Flow",
    },
)
