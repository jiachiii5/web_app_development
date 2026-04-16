from . import get_db_connection

class Poem:
    """提供針對 Poem (籤詩) 資料表的 CRUD 靜態方法"""
    @staticmethod
    def create(data):
        """新增一筆籤詩記錄。data 為 dict。"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO poems (poem_no, title, content, explanation) VALUES (?, ?, ?, ?)",
                (data.get('poem_no'), data.get('title'), data.get('content'), data.get('explanation'))
            )
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error creating poem: {e}")
            return None
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def get_all():
        """取得所有籤詩"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM poems ORDER BY poem_no ASC")
            rows = cursor.fetchall()
            return [dict(r) for r in rows]
        except Exception as e:
            print(f"Error fetching poems: {e}")
            return []
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def get_by_id(poem_id):
        """根據 ID 取得特定籤詩"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM poems WHERE id = ?", (poem_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
        except Exception as e:
            print(f"Error fetching poem by id: {e}")
            return None
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def update(poem_id, data):
        """更新單筆籤詩記錄。data = {'title': ..., 'explanation': ...}"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            set_clause = ", ".join([f"{k} = ?" for k in data.keys()])
            if not set_clause:
                return False
            values = list(data.values())
            values.append(poem_id)
            cursor.execute(f"UPDATE poems SET {set_clause} WHERE id = ?", values)
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating poem: {e}")
            return False
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def delete(poem_id):
        """刪除單筆籤詩記錄"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM poems WHERE id = ?", (poem_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting poem: {e}")
            return False
        finally:
            if 'conn' in locals() and conn:
                conn.close()

class History:
    """針對過往抽籤歷史 (History) 資料表的 CRUD 靜態方法"""
    @staticmethod
    def create(data):
        """新增一筆抽籤記錄"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO history (user_id, poem_id) VALUES (?, ?)",
                (data.get('user_id'), data.get('poem_id'))
            )
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error creating history: {e}")
            return None
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def get_all():
        """取得系統所有抽籤記錄"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM history ORDER BY created_at DESC")
            rows = cursor.fetchall()
            return [dict(r) for r in rows]
        except Exception as e:
            print(f"Error fetching all history: {e}")
            return []
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def get_by_id(history_id):
        """取得單筆歷史紀錄"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM history WHERE id = ?", (history_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
        except Exception as e:
            print(f"Error fetching history by id: {e}")
            return None
        finally:
            if 'conn' in locals() and conn:
                conn.close()
                
    @staticmethod
    def get_by_user(user_id):
        """取得特定人員的所有抽籤紀錄 (包含籤詩詳細資訊)"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = '''
                SELECT h.id, h.created_at, p.poem_no, p.title, p.content, p.explanation
                FROM history h
                JOIN poems p ON h.poem_id = p.id
                WHERE h.user_id = ?
                ORDER BY h.created_at DESC
            '''
            cursor.execute(query, (user_id,))
            rows = cursor.fetchall()
            return [dict(r) for r in rows]
        except Exception as e:
            print(f"Error fetching user histroy: {e}")
            return []
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def update(history_id, data):
        """歷史紀錄一般不可修改，但這裡為了一致性提供 CRUD 功能。"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            set_clause = ", ".join([f"{k} = ?" for k in data.keys()])
            if not set_clause:
                return False
            values = list(data.values())
            values.append(history_id)
            cursor.execute(f"UPDATE history SET {set_clause} WHERE id = ?", values)
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating history: {e}")
            return False
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def delete(history_id):
        """刪除單一歷史紀錄"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM history WHERE id = ?", (history_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting history: {e}")
            return False
        finally:
            if 'conn' in locals() and conn:
                conn.close()
