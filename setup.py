#!/usr/bin/python3
#setup
#by inoro

from setuptools import setup, find_packages

setup(
    # Application name:
    name="dyipd",

    # Version number (initial):
    version=open("version.txt").read().replace('\n',''),

    # Application author details:
    author="inoro",
    author_email="nothing@addr.ess",
    keywords="",

    # Packages
    packages=find_packages(),

    python_requires=">=3.5",

    # Include additional files into the package
    include_package_data=True,

    # Details
    url="https://github.com/boot1110001/dyipd",
    license="GPL v3.0",
    description="...",
    long_description=open("README.md").read(),

    # Dependent packages (distributions)
    install_requires=[
        "socket",
        "ssl",
        "base64",
        "datetime"
    ],

    data_files=[
        ('', [
            'dyipd',
            'version.txt'
        ])
    ],

    entry_points={  # Optional
        "console_scripts": [
            "dyipd=utils:main"
        ]
    },

    project_urls={  # Optional
        "Source": "https://github.com/boot1110001/dyipd"
    }
)
