# 📄 setup.py
from setuptools import setup, find_packages

setup(
    name="chrome-profile-manager",  # This should match PyPI package name
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "rich>=10.0.0",
    ],
    entry_points={
        "console_scripts": [
            "chrome-profile-manager=chrome_profile_manager.__main__:main",
            "pybro-chrome=chrome_profile_manager.__main__:main",
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A friendly Chrome profile manager for quick profile switching",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/chrome-profile-manager",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.8",
)