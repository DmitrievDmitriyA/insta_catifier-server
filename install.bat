pip install virtualenv
virtualenv venv --system-site-packages
call .\venv\Scripts\activate.bat
pip install instagram-scraper
pip install opencv-python
pip install pillow
pip install Flask
pip install Flask-Script
pip install minio
pip install ..\insta_catifier\dist\catifier-0.1.tar.gz
pip install -U "dramatiq[all]"