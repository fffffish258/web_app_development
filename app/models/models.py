import sqlite3
import os

def get_db_connection():
    """
    建立並回傳資料庫連線。
    設定 row_factory = sqlite3.Row 以便透過欄位名稱存取資料。
    """
    # 取得目前檔案的絕對路徑，再推導出 instance/database.db
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(current_dir, '..', '..', 'instance', 'database.db')
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

class AdminModel:
    @staticmethod
    def create(username, password_hash):
        """
        新增一筆管理者記錄。
        參數: username (str), password_hash (str)
        回傳: 成功回傳新增的 id，失敗回傳 None
        """
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO admins (username, password_hash) VALUES (?, ?)',
                (username, password_hash)
            )
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Database error in AdminModel.create: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_by_username(username):
        """
        根據帳號取得管理者記錄。
        參數: username (str)
        回傳: sqlite3.Row 或 None
        """
        conn = get_db_connection()
        try:
            return conn.execute('SELECT * FROM admins WHERE username = ?', (username,)).fetchone()
        except sqlite3.Error as e:
            print(f"Database error in AdminModel.get_by_username: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_by_id(admin_id):
        """
        根據 ID 取得管理者記錄。
        參數: admin_id (int)
        回傳: sqlite3.Row 或 None
        """
        conn = get_db_connection()
        try:
            return conn.execute('SELECT * FROM admins WHERE id = ?', (admin_id,)).fetchone()
        except sqlite3.Error as e:
            print(f"Database error in AdminModel.get_by_id: {e}")
            return None
        finally:
            conn.close()

class ActivityModel:
    @staticmethod
    def create(data):
        """
        新增一筆活動記錄。
        參數: data (dict)，包含 title, description, event_time, location, capacity
        回傳: 成功回傳新增的 id，失敗回傳 None
        """
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                '''
                INSERT INTO activities (title, description, event_time, location, capacity, is_full)
                VALUES (?, ?, ?, ?, ?, 0)
                ''',
                (data.get('title'), data.get('description'), data.get('event_time'), 
                 data.get('location'), data.get('capacity'))
            )
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Database error in ActivityModel.create: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_all():
        """
        取得所有活動記錄。
        回傳: list of sqlite3.Row
        """
        conn = get_db_connection()
        try:
            return conn.execute('SELECT * FROM activities ORDER BY created_at DESC').fetchall()
        except sqlite3.Error as e:
            print(f"Database error in ActivityModel.get_all: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def get_by_id(activity_id):
        """
        取得單筆活動記錄。
        參數: activity_id (int)
        回傳: sqlite3.Row 或 None
        """
        conn = get_db_connection()
        try:
            return conn.execute('SELECT * FROM activities WHERE id = ?', (activity_id,)).fetchone()
        except sqlite3.Error as e:
            print(f"Database error in ActivityModel.get_by_id: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def update(activity_id, data):
        """
        更新單筆活動記錄。
        參數: activity_id (int), data (dict) 包含要更新的欄位
        回傳: boolean 代表是否成功
        """
        conn = get_db_connection()
        try:
            conn.execute(
                '''
                UPDATE activities 
                SET title = ?, description = ?, event_time = ?, location = ?, capacity = ?, is_full = ?
                WHERE id = ?
                ''',
                (data.get('title'), data.get('description'), data.get('event_time'), 
                 data.get('location'), data.get('capacity'), data.get('is_full', 0), activity_id)
            )
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database error in ActivityModel.update: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def update_full_status(activity_id, is_full):
        """
        更新單筆活動的額滿狀態。
        參數: activity_id (int), is_full (int/bool)
        回傳: boolean 代表是否成功
        """
        conn = get_db_connection()
        try:
            conn.execute('UPDATE activities SET is_full = ? WHERE id = ?', (is_full, activity_id))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database error in ActivityModel.update_full_status: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def delete(activity_id):
        """
        刪除單筆活動記錄。
        參數: activity_id (int)
        回傳: boolean 代表是否成功
        """
        conn = get_db_connection()
        try:
            conn.execute('DELETE FROM activities WHERE id = ?', (activity_id,))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database error in ActivityModel.delete: {e}")
            return False
        finally:
            conn.close()

class RegistrationModel:
    @staticmethod
    def create(data):
        """
        新增一筆報名記錄。
        參數: data (dict)，包含 activity_id, name, student_id, email, phone
        回傳: 成功回傳新增的 id，失敗回傳 None
        """
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                '''
                INSERT INTO registrations (activity_id, name, student_id, email, phone)
                VALUES (?, ?, ?, ?, ?)
                ''',
                (data.get('activity_id'), data.get('name'), data.get('student_id'), 
                 data.get('email'), data.get('phone'))
            )
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Database error in RegistrationModel.create: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_all():
        """
        取得所有報名記錄。
        回傳: list of sqlite3.Row
        """
        conn = get_db_connection()
        try:
            return conn.execute('SELECT * FROM registrations ORDER BY created_at DESC').fetchall()
        except sqlite3.Error as e:
            print(f"Database error in RegistrationModel.get_all: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def get_by_id(registration_id):
        """
        取得單筆報名記錄。
        參數: registration_id (int)
        回傳: sqlite3.Row 或 None
        """
        conn = get_db_connection()
        try:
            return conn.execute('SELECT * FROM registrations WHERE id = ?', (registration_id,)).fetchone()
        except sqlite3.Error as e:
            print(f"Database error in RegistrationModel.get_by_id: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_by_activity_id(activity_id):
        """
        根據活動 ID 取得報名記錄。
        參數: activity_id (int)
        回傳: list of sqlite3.Row
        """
        conn = get_db_connection()
        try:
            return conn.execute(
                'SELECT * FROM registrations WHERE activity_id = ? ORDER BY created_at ASC',
                (activity_id,)
            ).fetchall()
        except sqlite3.Error as e:
            print(f"Database error in RegistrationModel.get_by_activity_id: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def count_by_activity_id(activity_id):
        """
        取得單一活動的目前報名人數。
        參數: activity_id (int)
        回傳: int (報名人數)
        """
        conn = get_db_connection()
        try:
            result = conn.execute(
                'SELECT COUNT(*) as count FROM registrations WHERE activity_id = ?',
                (activity_id,)
            ).fetchone()
            return result['count'] if result else 0
        except sqlite3.Error as e:
            print(f"Database error in RegistrationModel.count_by_activity_id: {e}")
            return 0
        finally:
            conn.close()

    @staticmethod
    def update(registration_id, data):
        """
        更新單筆報名記錄。
        參數: registration_id (int), data (dict) 包含要更新的欄位
        回傳: boolean 代表是否成功
        """
        conn = get_db_connection()
        try:
            conn.execute(
                '''
                UPDATE registrations 
                SET name = ?, student_id = ?, email = ?, phone = ?
                WHERE id = ?
                ''',
                (data.get('name'), data.get('student_id'), data.get('email'), data.get('phone'), registration_id)
            )
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database error in RegistrationModel.update: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def delete(registration_id):
        """
        刪除單筆報名記錄。
        參數: registration_id (int)
        回傳: boolean 代表是否成功
        """
        conn = get_db_connection()
        try:
            conn.execute('DELETE FROM registrations WHERE id = ?', (registration_id,))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database error in RegistrationModel.delete: {e}")
            return False
        finally:
            conn.close()
