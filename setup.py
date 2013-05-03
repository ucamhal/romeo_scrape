from setuptools import setup

setup(
    name="romeo_scrape",
    version="0.0.1",
    description="A command line tool to screen scrape Journal titles from "
                "SHERPA RoMEO.",
    url="https://bitbucket.org/caret/romeo_scrape",
    author="Hal Blackburn",
    author_email="hal@caret.cam.ac.uk",
    license="Apache",
    scripts=["romeo_scrape.py"],
    install_requires=[
        "requests",
        "lxml",
        "docopt"
    ],
    zip_safe=False,
    classifiers=[
        "Intended Audience :: Developers",
        "Environment :: Console",
        "License :: OSI Approved :: Apache Software License",
    ]
)
