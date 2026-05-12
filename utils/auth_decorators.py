import os
from functools import wraps
from flask import session, redirect, url_for, flash, jsonify, request

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            if request.path.startswith('/api/'):
                return jsonify({"status": "error", "message": "Unauthorized access - Please log in."}), 401
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function
