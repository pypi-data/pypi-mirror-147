from setuptools import setup, find_packages
import codecs
import os


here = os.path.abspath(os.path.dirname(__file__))


with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()


VERSION = "0.0.2"
DESCRIPTION = "Translate unlimited text using DeepL's advanced translation engine."
LONG_DESCRIPTION = "Translate unlimited text using DeepL's advanced translation engine."


setup(
    name="deepltransl8",
    version=VERSION,
    author="Nyaanity (Sascha Ehret)",
    author_email="no@mail.wow",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[],
    keywords=["python", "translation", "deepl"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)