# setup.py

from setuptools import setup, find_packages

setup(
    name="jnjrender",
    version="0.2.0",
    packages=find_packages(),
    description="An utility to render Jinja2 templates in rendered text",
    author="Andrea Michelotti",
    install_requires=[
        "jinja2",
        "pyyaml",
    ],
    entry_points={
        "console_scripts": [
            "jnjrender=jnjrender.cli:main",
        ],
    },
)
