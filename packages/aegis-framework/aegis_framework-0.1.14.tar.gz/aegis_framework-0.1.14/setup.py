from setuptools import setup, find_packages

setup(
    name="aegis-framework",
    version="0.1.14",
    packages=find_packages(),
    install_requires=[
        "typing>=3.7.4",
        "requests>=2.25.0",
        "fuzzywuzzy>=0.18.0",
        "python-Levenshtein>=0.12.0",
        "sqlite3-api>=2.0.1",
    ],
    author="Metis Analytics",
    author_email="cjohnson@metisos.com",
    description="A comprehensive, extensible AI agent framework with local LLM integration",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/metisos/aegis-framework",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.7",
    extras_require={
        "web": ["flask>=2.0.0", "flask-socketio>=5.0.0"],
    }
)
