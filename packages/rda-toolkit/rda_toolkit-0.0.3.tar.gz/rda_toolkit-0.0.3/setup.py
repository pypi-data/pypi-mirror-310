from setuptools import setup

setup(
    name="rda-toolkit",
    version="0.0.3",
    description="Redistricting analysis tools",
    url="https://github.com/rdatools/rdatools",
    author="alecramsay",
    author_email="alec@davesredistricting.org",
    license="MIT",
    packages=[
        "rdatools",
        "rdatools.base",
        "rdatools.score",
        "rdatools.dccvt",
        # TODO - More ...
    ],
    install_requires=[
        "Fiona",
        "geopandas",
        "libpysal",
        "pytest",
        "scipy",
        "shapely",
    ],
    zip_safe=False,
)
