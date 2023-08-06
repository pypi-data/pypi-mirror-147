from setuptools import setup

setup(
    name="jobdec",
    version="0.0.1",
    author="Gareth Williams",
    author_email="gareth.m.j.williams@gmail.com",
    packages=["jobdec"],
    package_data={"jobdec": ["static/*"]},
    url="http://pypi.python.org/pypi/jobdec/",
    license="LICENCE.txt",
    description="Creates and runs scheduled jobs from Python functions",
    long_description=open("README.md").read(),
    install_requires=[
        "Flask>=2",
        "networkx>=2",
        "Pebble>=4",
        "pygraphviz>=1",
        "schedule>=1",
    ],
)
