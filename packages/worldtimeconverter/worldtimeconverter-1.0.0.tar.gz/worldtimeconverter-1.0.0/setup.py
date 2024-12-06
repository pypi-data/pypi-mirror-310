# setup.py
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="worldtimeconverter",
    version="1.0.0",
    author="Oren Grinker",
    author_email="orengr4@gmail.com",
    description="Advanced time conversion and timezone management library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/OrenGrinker/worldtimeconverter",
    packages=find_packages(exclude=["tests*"]),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Localization",
    ],
    python_requires=">=3.7",
    install_requires=[
        "pytz>=2021.1",
        "python-dateutil>=2.8.2",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "mypy>=0.910",
            "pylint>=2.8",
        ],
    },
    keywords=[
        "timezone",
        "time-conversion",
        "business-hours",
        "working-hours",
        "holiday-calendar",
        "python",
        "pytz",
        "time-management",
        "date-time",
        "world-clock",
    ],
)
