from setuptools import setup, find_packages

setup(
    name='cas_python_sdk',              # Replace with your project name
    version='0.0.2',                # Version of your package
    description='A Python package that provides an abstraction layer to the Rust Crypto suite of algorithms',
    author='Mike Mulchrone',
    author_email='',
    url='https://github.com/yourusername/my_project',  # Project URL
    packages=find_packages(),       # Automatically find packages
    install_requires=[              # List of dependencies
        'requests'            # Example
    ],
    classifiers=[                   # Optional classifiers (helps PyPI categorize your project)
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',         # Minimum Python version required
)