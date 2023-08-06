from setuptools import setup

setup(
    name = "Rimma",
    author = "weerdy15",
    url = "https://github.com/weerdy15/Rimma",
    project_urls = {
        "Issue tracker": "https://github.com/weerdy15/Rimma/issues"
    },
    version = "1.0.0",
    packages = [
        "Rimma",
    ],
    license = "MIT",
    description = "API wrapper & bot framework for Discord",
    long_description = open('README.md', 'r').read(),
    long_description_content_type = "text/markdown",
    install_requires = [],
    extras_require = {},
    python_requires = ">=3.8.0",
    classifiers = [
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Utilities",
    ]
)
