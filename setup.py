from setuptools import setup, find_packages

setup(
    name="catifier-server",
    version="0.1",
    packages=find_packages(),
    install_requires=["Flask", "minio", "catifier", "cachetools", "gunicorn"],
    package_data={
        "catifier-server": ["static/*", "templates/*", "secret.json"],
    }
)