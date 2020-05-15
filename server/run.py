import time, json
from flask import Flask, render_template, request, redirect, url_for
from server.cache import ExtendedLFUCache
from logging import FileHandler, Formatter
import server.catifierAdapter as catifierAdapter
import server.dataBaseAdapter as dataBaseAdapter
import server.serverHelper as serverHelper


# Create cache
cache = ExtendedLFUCache(maxsize=10)


# Initialize cache
# logger.info('Accounts retrieved: ')
# logger.info(accounts)
for account in dataBaseAdapter.get_accounts_from_bucket():
    data = dataBaseAdapter.get_results_from_bucket(account)
    cache[account] = data


# Create Flask app
flask_app = Flask(__name__)


# Logging initialization
# file_handler = FileHandler('./logs/server.log')
#file_formatter = Formatter(
    # fmt='%(name)s %(levelname)s %(asctime)s %(message)s',
    # datefmt='%d-%m-%Y %I:%M:%S')
# file_handler.setFormatter(file_formatter)
# flask_app.logger.addHandler(file_handler)
# logger = flask_app.logger 


# === Errors ===


@flask_app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@flask_app.errorhandler(Exception)
def error_page(e):
    return render_template('error.html'), 500


# === Home page ===


# falsk uses GET request for every page by default, so there is no need to use it
# explicitly
@flask_app.route('/')
@flask_app.route('/index.html')
def index():
    return render_template('index.html')


@flask_app.route('/submit_form')
def submit_form():
    if (instagramAccount:= request.args.get('instagramAccount')):
        if not serverHelper.validateInstagramAccount(instagramAccount):
            return redirect(url_for('error'))
    else:
        return redirect(url_for('error'))

    if (userEmail:= request.args.get('userEmail')):
        if serverHelper.validateEmail(userEmail):
            # logger.info(f'Incoming request: {str(instagramAccount)}, {str(userEmail)}')
            return redirect(url_for('result', instagramAccount=instagramAccount, userEmail=userEmail))
        else:
            return redirect(url_for('error'))
    else:
        # logger.info(f'Incoming request: {str(instagramAccount)}')
        return redirect(url_for('processing', instagramAccount=instagramAccount))


# === A generic stub for orphan pages ===


@flask_app.route('/<string:page_name>.html')
def generic(page_name=None):
    return render_template(f'{page_name}.html')


@flask_app.route('/redirect_to_<string:page_name>')
def redirect_to(page_name=None):
    time.sleep(1)
    data = {'redirect': f'{page_name}.html'}
    return data, 200


# === Processing page ===


@flask_app.route('/processing.html')
def processing():
    instagramAccount = request.args.get('instagramAccount')
    return render_template('processing.html', instagramAccount=instagramAccount)


@flask_app.route('/scraping_ready')
def recognition_ready():
    instagramAccount = request.args.get('instagramAccount')
    if instagramAccount in cache:
            return '', 200

    catifierAdapter.scrapePhotos(instagramAccount)
    return '', 200


@flask_app.route('/modification_ready')
def modification_ready():
    instagramAccount = request.args.get('instagramAccount')
    if instagramAccount in cache:
        return '', 200

    catifierAdapter.add_cats(instagramAccount)
    return '', 200


@flask_app.route('/redirect_to_gallery')
def redirect_to_gallery():
    time.sleep(1)
    instagramAccount = request.args.get('instagramAccount')
    data = {'redirect': url_for('gallery', instagramAccount=instagramAccount)}
    return data, 200 


# === Gallery page ===


@flask_app.route('/gallery.html')
def gallery():
    instagramAccount = request.args.get('instagramAccount')
    return render_template('gallery.html', instagramAccount=instagramAccount)


@flask_app.route('/get_photos')
def get_photos():
    instagramAccount = request.args.get('instagramAccount')

    if instagramAccount in cache:
        data = cache[instagramAccount]
        return data, 200

    data = dataBaseAdapter.get_results_from_bucket(instagramAccount)
    cache[instagramAccount] = data
    # logger.info(f'Get photos is finished: {str(instagramAccount)}')
    return data, 200


# === Result page ===


@flask_app.route('/result.html')
def result():
    instagramAccount = request.args.get('instagramAccount')
    userEmail = request.args.get('userEmail')
    return render_template('result.html', instagramAccount=instagramAccount, userEmail=userEmail)


@flask_app.route('/send_task', methods=['POST'])
def send_task():
    instagramAccount = request.form.get('instagramAccount')
    userEmail = request.form.get('userEmail')
    # logger.info(f'Send task is finished: {str(instagramAccount)}, {str(userEmail)}')
    return '', 200


if __name__ == "__main__":
    # Run app
    flask_app.run() 