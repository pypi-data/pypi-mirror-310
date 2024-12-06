from setuptools import setup, find_namespace_packages

setup(
    name="aegis_framework",  # Name of your package (should be unique on PyPI)
    version="0.1.12",  # Version of your package
    description="A framework for creating multi-agent colonies",  # Short description
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Metis Analytics",  # Your name or organization
    author_email="cjohnson@metisos.com",  # Your email address
    url="https://github.com/metisos/aegis_framework.git",  # URL for your project
    packages=find_namespace_packages(include=["aegis_framework", "aegis_framework.*"]),  # Explicitly find packages under aegis_framework
    package_data={
        "aegis_framework": ["py.typed", "*.pyi", "**/*.pyi"],
    },
    install_requires=[
        "flask",
        "flask-socketio",
        "fuzzywuzzy",
        "python-socketio",
        "schedule",
        "python-Levenshtein",  # Added for better fuzzywuzzy performance
    ],  # List your package's dependencies
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",  # License for your package
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires='>=3.7',
    include_package_data=True,
    zip_safe=False,
)
