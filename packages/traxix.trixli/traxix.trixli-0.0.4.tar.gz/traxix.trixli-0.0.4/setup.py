import os
from setuptools import setup, find_namespace_packages

with open("requirements.txt") as f:
    required = f.read().splitlines()

    setup(
        name="traxix.trixli",
        version="0.0.4",
        url="https://gitlab.com/traxix/trixli",
        packages=find_namespace_packages(include=["traxix.*"]),
        install_requires=required,
        scripts=[
            "traxix/again",
            "traxix/f",
            "traxix/fr",
            "traxix/fp",
            "traxix/fe",
            "traxix/ec2l",
        ],
        author="trax Omar Givernaud",
        author_mail="o.givernaud@gmail.com",
    )
