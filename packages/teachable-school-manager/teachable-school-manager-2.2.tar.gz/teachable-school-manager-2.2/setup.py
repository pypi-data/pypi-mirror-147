"""A setuptools based setup module.
See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
Modified by Madoshakalaka@Github (dependency links added)
"""

# io.open is needed for projects that support Python 2.7
# It ensures open() defaults to text mode with universal newlines,
# and accepts an argument to specify the text encoding
# Python 3 only projects can skip this import
from io import open
from os import path

# Always prefer setuptools over distutils
from setuptools import setup, find_namespace_packages

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="teachable-school-manager",  # Required
    version="2.2",  # Required
    description="Manage your Teachable school using the unofficial Teachable API",  # Optional
    long_description=long_description,  # Optional
    long_description_content_type="text/markdown",  # Optional (see note above)
    url="https://github.com/stezz/teachable-scripts",  # Optional
    author="Stefano Mosconi",  # Optional
    author_email="stefano.mosconi@gmail.com",  # Optional
    package_dir={"": "src"},
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 4 - Beta",
        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        "Topic :: Education",
        # Pick your license as you wish
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    keywords="scripts teachable",  # Optional
    packages=find_namespace_packages("src", exclude=["contrib", "docs", "tests"]),  # Required
    # packages=["teachable"],  # Required
    python_requires=">3.7, <4",
    install_requires=[
        "jinja2>=3.0.3",
        "pyexcel>=0.6.7",
        "pyexcel-xlsx>=0.6.0",
        "pytablewriter[excel,html]>=0.64.1",
        "requests>=2.26.0",
        "schedule>=1.1.0",
        "enlighten>=1.10.1"
    ],  # Optional
    extras_require={"dev": []},  # Optional
    dependency_links=[],
    # these directories need to be synced with whatever is in TeachableAPI as DEFAULT_DIRS
    data_files=[(path.join("teachable", "etc" ), ["src/etc/config_example.ini", "src/etc/logconf.ini",
                                                  "src/etc/scheduler_example.ini"]),
                (path.join('teachable', 'templates'), ["templates/email_inactive.txt",
                                                       "templates/email_notstarted.txt",
                                                       "templates/weekly_report.html",
                                                       "templates/unenroll.txt",
                                                       "templates/change_password.txt",
                                                       "templates/auto_unenroll.txt"])],
    entry_points={"console_scripts": ["teachable_scheduler=teachable.scripts.scheduler:main",
                                      "teachable=teachable.scripts.teachable:main"]},  # Optional
    # scripts=["scripts/remind.py"],  # Optional
    project_urls={  # Optional
        "Bug Reports": "https://github.com/stezz/teachable-scripts/issues",
        #        "Funding": "https://donate.pypi.org",
        #        "Say Thanks!": "http://saythanks.io/to/example",
        "Source": "https://github.com/stezz/teachable-scripts/",
    },
)
