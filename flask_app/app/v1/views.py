from flask_app.app.v1 import app , api

@app.route('/')
def index():
    return 'Hello World !'

@app.route('/healthz')
def health():
    return 'Up and Running !!!'