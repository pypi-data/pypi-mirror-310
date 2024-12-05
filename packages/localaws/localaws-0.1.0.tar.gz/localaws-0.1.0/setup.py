from setuptools import setup, find_packages

setup(
    name="localaws",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "boto3>=1.26.0",
        "click>=8.0.0"
    ],
    entry_points={
        'console_scripts': [
            'localaws=localaws.cli:main',
        ],
    },
    python_requires=">=3.7",
    description="Run local Python scripts with AWS profiles - perfect for local testing with different AWS environments",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/localaws",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Testing",
        "Topic :: System :: Systems Administration",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="aws, profile, local development, testing, aws-cli, boto3",
)
