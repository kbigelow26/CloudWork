# [START gae_python38_app]
from flask import Flask, render_template


# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)


@app.route('/')
def hello():
    """Return home page"""
    return render_template('home.html')


@app.route('/home.html')
def secondhome():
    """Return home page"""
    return render_template('home.html')


@app.route('/one.html')
def one():
    """Return page one"""
    return render_template('/one.html')


@app.route('/two.html')
def two():
    """Return page two"""
    return render_template('two.html')


@app.route('/404.html')
def badlink():
    """Return 404 page"""
    return render_template('404.html')


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python38_app]
