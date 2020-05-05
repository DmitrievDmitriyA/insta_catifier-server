from setuptools import setup, find_packages

setup(
    name="catifier-server",
    version="0.1",
    packages=find_packages(),,
    install_requires=["catifier", "Flask", "Flask-Script", "minio"],
    dependency_links=['git+https://github.com/DmitrievDmitriyA/insta_catifier.git@e11c9e22548fedd3504cd24d9d765a10316cc47f']
    package_data={
        "catifier": ["statis/*", "templates/*"],
    }
)