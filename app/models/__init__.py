import sqlite3
import os

def get_db_connection():
    """
    建立並回傳一個資料庫連線。
    回傳的連線具備 sqlite3.Row 功能，可以使用欄位名稱進行資料存取。
    如果在連線過程中發生問題，會接住錯誤並列印出資訊。
    """
    try:
        db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'instance', 'database.db')
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None
