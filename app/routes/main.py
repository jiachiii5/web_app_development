from flask import Blueprint

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def index():
    """
    [GET] /
    顯示首頁歡迎畫面、介紹與準備抽籤入口。
    會讀取 Session 判斷使用者是否登入，以改變導覽列。
    """
    pass

@main_bp.route('/fortune/draw', methods=['POST'])
def fortune_draw():
    """
    [POST] /fortune/draw
    處理隨機抽籤邏輯。
    抽出籤號後，重導向至 /fortune/result/<id>。
    """
    pass

@main_bp.route('/fortune/result/<int:id>', methods=['GET'])
def fortune_result(id):
    """
    [GET] /fortune/result/<id>
    顯示對應 ID 的籤詩內容與詳解。
    """
    pass

@main_bp.route('/fortune/save', methods=['POST'])
def fortune_save():
    """
    [POST] /fortune/save
    接收表單傳入的 poem_id，驗證登入權限。
    若已登入則將抽籤結果寫入 history 資料表，並重導向至 /profile。
    若未登入，導向至登入頁面並快閃(flash) 提示。
    """
    pass

@main_bp.route('/fortune/share/<int:id>', methods=['GET'])
def fortune_share(id):
    """
    [GET] /fortune/share/<id>
    為了社群平台 (FB/Line/IG) 提供帶有 OpenGraph meta tags 的專屬分享頁。
    """
    pass

@main_bp.route('/profile', methods=['GET'])
def profile():
    """
    [GET] /profile
    從庫中讀取該登入使用者的歷史算命紀錄並於 history.html 顯示。
    若未登入將導出至登入頁。
    """
    pass
