from flask import Blueprint, request, render_template, redirect, url_for, flash, session
import random
from app.models.fortune import Poem, History

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def index():
    """首頁：顯示介紹與抽籤按鈕"""
    user_id = session.get('user_id')
    return render_template('index.html', user_id=user_id)

@main_bp.route('/fortune/draw', methods=['POST'])
def fortune_draw():
    """執行隨機抽籤並前往解答"""
    poems = Poem.get_all()
    if not poems:
        flash('系統中尚無籤詩資料，請聯繫管理員！')
        return redirect(url_for('main.index'))
        
    chosen_poem = random.choice(poems)
    return redirect(url_for('main.fortune_result', id=chosen_poem['id']))

@main_bp.route('/fortune/result/<int:id>', methods=['GET'])
def fortune_result(id):
    """顯示抽籤結果"""
    poem = Poem.get_by_id(id)
    if not poem:
        flash('找不到該籤詩')
        return redirect(url_for('main.index'))
        
    user_id = session.get('user_id')
    return render_template('result.html', poem=poem, user_id=user_id)

@main_bp.route('/fortune/save', methods=['POST'])
def fortune_save():
    """將目前的籤詩存進歷史紀錄"""
    user_id = session.get('user_id')
    if not user_id:
        flash('請先登入後才能儲存籤詩！')
        return redirect(url_for('auth.login'))
        
    poem_id = request.form.get('poem_id')
    if not poem_id:
        flash('缺少籤詩資訊')
        return redirect(url_for('main.index'))
        
    history_id = History.create({'user_id': user_id, 'poem_id': poem_id})
    if history_id:
        flash('儲存成功！查看您的個人紀錄。')
        return redirect(url_for('main.profile'))
    else:
        flash('儲存失敗，請稍後再試')
        return redirect(url_for('main.fortune_result', id=poem_id))

@main_bp.route('/fortune/share/<int:id>', methods=['GET'])
def fortune_share(id):
    """回傳供爬蟲抓取 og-tags 的分享專屬頁面"""
    poem = Poem.get_by_id(id)
    if not poem:
        return "Target not found", 404
    return render_template('share.html', poem=poem)

@main_bp.route('/profile', methods=['GET'])
def profile():
    """顯示會員的所有過往抽籤歷史"""
    user_id = session.get('user_id')
    if not user_id:
        flash('需要登入才能觀看過往歷史。')
        return redirect(url_for('auth.login'))
        
    histories = History.get_by_user(user_id)
    return render_template('history.html', histories=histories, user_id=user_id)
