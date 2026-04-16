from flask import Blueprint

donation_bp = Blueprint('donation', __name__, url_prefix='/donation')

@donation_bp.route('/', methods=['GET'])
def index():
    """
    [GET] /donation
    顯示香油錢與回饋說明的表單頁面 donation.html。
    如有登入，預設可載入使用者的稱呼。
    """
    pass

@donation_bp.route('/submit', methods=['POST'])
def submit():
    """
    [POST] /donation/submit
    接收表單的 amount 與 message，存入 donations 資料表。
    成功後重導向至感謝頁面 /donation/success。
    """
    pass

@donation_bp.route('/success', methods=['GET'])
def success():
    """
    [GET] /donation/success
    感謝信或成果展示頁面 donation_success.html。
    """
    pass
