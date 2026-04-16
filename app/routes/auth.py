from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    [GET] 顯示登入與註冊頁面 (共用同一頁 `login.html`)
    [POST] 驗證登入
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('請填寫帳號與密碼')
            return redirect(url_for('auth.login'))
            
        user = User.get_by_username(username)
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            flash('登入成功！')
            return redirect(url_for('main.index'))
            
        flash('帳號或密碼錯誤')
        return redirect(url_for('auth.login'))
        
    return render_template('login.html')

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    [POST] 接收註冊表單，寫入資料庫
    """
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email', '')
    
    if not username or not password:
        flash('帳號密碼為必填')
        return redirect(url_for('auth.login'))
        
    existing_user = User.get_by_username(username)
    if existing_user:
        flash('此帳號已存在')
        return redirect(url_for('auth.login'))
        
    hashed_pwd = generate_password_hash(password)
    user_id = User.create({'username': username, 'password_hash': hashed_pwd, 'email': email})
    
    if user_id:
        session['user_id'] = user_id
        flash('註冊成功並已自動登入！')
        return redirect(url_for('main.index'))
    else:
        flash('系統發生錯誤，註冊失敗，請稍後再試')
        return redirect(url_for('auth.login'))

@auth_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    """
    清除 Session，完成登出
    """
    session.clear()
    flash('您已成功登出')
    return redirect(url_for('main.index'))
