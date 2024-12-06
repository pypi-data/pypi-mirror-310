from setuptools import setup, find_packages

# Read the README for the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="aegis-framework",
    version="0.1.15",
    packages=find_packages(),
    install_requires=[
        "typing>=3.7.4",
        "requests>=2.25.0",
        "fuzzywuzzy>=0.18.0",
        "python-Levenshtein>=0.12.0",
        "sqlite3-api>=2.0.1",
        "numpy>=1.19.0",
        "pandas>=1.3.0",
    ],
    author="Metis Analytics",
    author_email="cjohnson@metisos.com",
    description="A comprehensive, extensible AI agent framework with local LLM integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/metisos/aegis-framework",
    project_urls={
        "Bug Tracker": "https://github.com/metisos/aegis-framework/issues",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.7",
    extras_require={
        "web": [
            "flask>=2.0.0",
            "flask-socketio>=5.0.0",
            "eventlet>=0.30.0"
        ],
        "data": [
            "numpy>=1.19.0",
            "pandas>=1.3.0",
            "matplotlib>=3.3.0",
            "seaborn>=0.11.0"
        ],
        "dev": [
            "pytest>=6.0.0",
            "black>=21.0.0",
            "isort>=5.0.0",
            "mypy>=0.900",
            "flake8>=3.9.0"
        ]
    },
    include_package_data=True,
    keywords=[
        "ai",
        "agents",
        "llm",
        "machine-learning",
        "artificial-intelligence",
        "multi-agent",
        "ollama"
    ],
)
