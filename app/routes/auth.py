from flask import Blueprint

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    [GET] /auth/login
    顯示會員註冊與登入的表單頁面 login.html

    [POST] /auth/login
    接收登入表單，向資料庫比對 Username 與 Password_hash。
    驗證成功則寫入 session 並導向首頁 /。
    """
    pass

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    [POST] /auth/register
    接收註冊表單，檢查 Username 唯一性，雜湊密碼後寫入 Users 表。
    成功後可直接寫入 session 登入或導回 /auth/login 要求重登。
    """
    pass

@auth_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    """
    [GET / POST] /auth/logout
    清除 session 中紀錄的使用者狀態，完成登出並導向 /。
    """
    pass
