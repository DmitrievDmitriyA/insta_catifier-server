from setuptools import setup, find_packages

setup(
    name="catifier-server",
    version="0.1",
    packages=find_packages(),
    install_requires=["Flask", "Flask-Script", "minio", "catifier", "cachetools"],
    package_data={
        "catifier-server": ["statis/*", "templates/*"],
    }
)