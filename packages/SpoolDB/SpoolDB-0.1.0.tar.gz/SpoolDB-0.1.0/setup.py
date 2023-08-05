import setuptools as st
__project__ = "SpoolDB"
__version__ = "0.1.0"
__description__ = "Python persistent dictionary (a key value store)"
__packages__ = ["spooldb"]
__author__ = "MXPSQL"
__author__email__ = "2000onetechguy@gmail.com"
__keywords__ = ["Dict", "Persistent", "Database", "JSON", "CSV", "Shelf", "Pickle"]
__source__ = "https://github.com/MOALib/SpoolDB"
__classifiers__ = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3.6",
]

st.setup(
    name=__project__,
    version=__version__,
    description=__description__,
    packages=__packages__,
    author=__author__,
    author_email=__author__email__,
    url=__source__,
    keywords=__keywords__,
    classifiers=__classifiers__,
)