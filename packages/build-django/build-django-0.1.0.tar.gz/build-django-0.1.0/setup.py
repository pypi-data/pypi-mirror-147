import os
import codecs
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.1.0'

DESCRIPTION = 'Command line utility for building Django projects'

# Setting up
setup(
    name="build-django",
    version=VERSION,
    author="Kapustlo",
    description=DESCRIPTION,
    url='https://notabug.org/kapustlo/build-django',
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    keywords=['python', 'django', 'build', 'cli', 'generate', 'code'],
    entry_points={
        'console_scripts': [
            'build-django=build_django.__main__:main'
        ]
    },
    classifiers=[
        "Framework :: Django",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Topic :: Software Development :: Code Generators",
        "Environment :: Console",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3 :: Only",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.8",
    install_required=(
        'django',
    )
)


