# setup.py
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="worldtimeconverter",
    version="1.0.1",
    author="Oren Grinker",
    author_email="orengr4@gmail.com",
    description="Advanced time conversion and timezone management library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/OrenGrinker/worldtimeconverter",
    project_urls={
        "Bug Tracker": "https://github.com/OrenGrinker/worldtimeconverter/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "."},
    packages=find_packages(where="."),
    python_requires=">=3.7",
    install_requires=[
        "pytz>=2021.1",
        "python-dateutil>=2.8.2",
    ],
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