from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.admin import AdminModel

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Username and Password are required!', 'error')
            return render_template('register.html')

        if AdminModel.create_admin(username, password):
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Username already exists.', 'error')
            
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        admin = AdminModel.verify_admin(username, password)
        if admin:
            session['admin_id'] = admin['id']
            session['username'] = admin['username']
            flash('Logged in successfully.', 'success')
            return redirect(url_for('candidates.index'))
        else:
            flash('Invalid username or password.', 'error')
            
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth.login'))
