"""
ufile.io
~~~~~~~~~
:copyright: (c) 2021 by Gautam Kumar <https://github.com/gautamajay52>.
:license: MIT, see LICENSE for more details.
:description: Asynchronous Python Wrapper for the Ufile API
"""

from setuptools import find_packages, setup


AUTHOR = "gautamajay52"
EMAIL = "gautamajay52@gmail.com"
URL = "https://github.com/gautamajay52/ufile.io"

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open('ufile/__init__.py', 'r', encoding='utf-8') as fd:
    for line in fd.readlines():
        if line.startswith('__version__'):
            VERSION = line.split('=')[1].strip().replace('"', "")
            break

setup(
    name="ufile.io",
    version=VERSION,
    description="Asynchronous Python Wrapper for the Ufile API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    license="MIT",
    packages=find_packages(),
    keywords="API ufile ufile.io fileuploader storage python",
    project_urls={
        "Source": "https://github.com/gautamajay52/ufile.io",
        "Documentation": "https://github.com/gautamajay52/ufile.io#readme",
        "Tracker": "https://github.com/gautamajay52/ufile.io/issues",
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Internet",
    ],
    python_requires=">=3.6",
    install_requires=["aiohttp"],
)
