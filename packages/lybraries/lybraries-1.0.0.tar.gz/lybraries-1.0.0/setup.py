from setuptools import setup

setup(
    name = "lybraries",
    author = "weerdy15",
    url = "https://github.com/weerdy15/lybraries",
    project_urls = {
        "Issue tracker": "https://github.com/weerdy15/lybraries/issues"
    },
    version = "1.0.0",
    packages = [
        "lybraries",
    ],
    license = "MIT",
    description = "API wrapper for libraries.io",
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
