# pylint: disable=missing-module-docstring
from setuptools import setup

requirements = [
    "flask",
    "flask-sqlalchemy",
    "flask-marshmallow",
    "stomp.py",
]

setup_requirements = []

test_requirements = [
    "flask-pytest",
    "pytest",
]

extra_requirements = {
    "dev": [
        "pytest",
        "black",
        "pylint",
        "pylint-flask-sqlalchemy",
        "pre-commit",
    ]
}

setup(
    author="Jack Deeth",
    author_email="developer@jackdeeth.org.uk",
    python_requires=">=3.7",
    description="Collates SimSig gateway messages behind an API",
    licence="MIT license",
    install_requires=requirements,
    setup_requires=setup_requirements,
    tests_require=test_requirements,
    extras_require=extra_requirements,
    test_suite="tests",
    version="0.0.1",
    name="simsig-collate-api",
)
