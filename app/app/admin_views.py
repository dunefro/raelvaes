from app import app

@app.route('/admin/healthz')
def admin_health():
    return "Admin is up and Running !!!"

@app.route('/admin/dashboard')
def admin_dashboard():
    return 'This is admin dashboard !!!'