from . import get_db_connection

class Donation:
    """香油錢(Donation)相關記錄的 CRUD 靜態方法"""
    @staticmethod
    def create(data):
        """新增一筆捐款紀錄。data 參數支援 amount, message, user_id"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO donations (user_id, amount, message) VALUES (?, ?, ?)",
                (data.get('user_id'), data.get('amount'), data.get('message'))
            )
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error creating donation: {e}")
            return None
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def get_all():
        """取得系統所有捐款記錄"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM donations ORDER BY created_at DESC")
            rows = cursor.fetchall()
            return [dict(r) for r in rows]
        except Exception as e:
            print(f"Error fetching donations: {e}")
            return []
        finally:
            if 'conn' in locals() and conn:
                conn.close()
                
    @staticmethod
    def get_by_id(donation_id):
        """取得單一筆捐款記錄"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM donations WHERE id = ?", (donation_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
        except Exception as e:
            print(f"Error fetching donation by id: {e}")
            return None
        finally:
            if 'conn' in locals() and conn:
                conn.close()
                
    @staticmethod
    def get_by_user(user_id):
        """取得特定人員的所有香油錢紀錄"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM donations WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
            rows = cursor.fetchall()
            return [dict(r) for r in rows]
        except Exception as e:
            print(f"Error fetching donations by user: {e}")
            return []
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def update(donation_id, data):
        """更新捐款紀錄。允許動態更新 data 內的鍵值"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            set_clause = ", ".join([f"{k} = ?" for k in data.keys()])
            if not set_clause:
                return False
            values = list(data.values())
            values.append(donation_id)
            cursor.execute(f"UPDATE donations SET {set_clause} WHERE id = ?", values)
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating donation: {e}")
            return False
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def delete(donation_id):
        """刪除單筆捐項紀錄"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM donations WHERE id = ?", (donation_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting donation: {e}")
            return False
        finally:
            if 'conn' in locals() and conn:
                conn.close()
