from app.v1 import app 

@app.route('/healthz')
def health():
    return 'Up and Running !!!' , 200