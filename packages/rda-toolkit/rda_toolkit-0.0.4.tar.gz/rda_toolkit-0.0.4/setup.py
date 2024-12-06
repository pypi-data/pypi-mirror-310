from setuptools import setup

setup(
    name="rda-toolkit",
    version="0.0.4",
    description="Redistricting analysis tools",
    url="https://github.com/rdatools/rdatools",
    author="alecramsay",
    author_email="alec@davesredistricting.org",
    license="MIT",
    packages=[
        "rdatools",
        "rdatools.base",
        "rdatools.dccvt",
        "rdatools.ei",
        "rdatools.ensemble",
        "rdatools.rootmap",
        "rdatools.score",
    ],
    install_requires=[
        "Fiona",
        "geopandas",
        "libpysal",
        "pytest",
        "scipy",
        "shapely",
        "rdapy",
        "gerrychain",
    ],
    zip_safe=False,
)
