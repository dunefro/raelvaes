from app import app

@app.route('/')
def index():
    return 'Hello World !'

@app.route('/healthz')
def health():
    return 'Up and Running !!!'