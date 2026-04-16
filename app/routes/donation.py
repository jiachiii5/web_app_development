from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from app.models.donation import Donation

donation_bp = Blueprint('donation', __name__, url_prefix='/donation')

@donation_bp.route('/', methods=['GET'])
def index():
    """顯示香油錢捐贈說明與表單"""
    user_id = session.get('user_id')
    return render_template('donation.html', user_id=user_id)

@donation_bp.route('/submit', methods=['POST'])
def submit():
    """處理捐款請求"""
    amount = request.form.get('amount')
    message = request.form.get('message', '')
    user_id = session.get('user_id') # Guest allowed if user_id is None
    
    if not amount or not amount.isdigit() or int(amount) <= 0:
        flash('請輸入有效的捐款金額')
        return redirect(url_for('donation.index'))
        
    donation_id = Donation.create({
        'user_id': user_id,
        'amount': int(amount),
        'message': message
    })
    
    if donation_id:
        flash('感謝您的香油錢回饋！')
        return redirect(url_for('donation.success'))
    else:
        flash('系統發生錯誤，稍後再試。')
        return redirect(url_for('donation.index'))

@donation_bp.route('/success', methods=['GET'])
def success():
    """感謝頁面"""
    return render_template('donation_success.html')
