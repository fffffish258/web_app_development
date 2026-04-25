import sqlite3

DATABASE = 'instance/database.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

class AdminModel:
    @staticmethod
    def create(username, password_hash):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                'INSERT INTO admins (username, password_hash) VALUES (?, ?)',
                (username, password_hash)
            )
            conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None # Username already exists
        finally:
            conn.close()

    @staticmethod
    def get_by_username(username):
        conn = get_db_connection()
        admin = conn.execute('SELECT * FROM admins WHERE username = ?', (username,)).fetchone()
        conn.close()
        return admin

    @staticmethod
    def get_by_id(admin_id):
        conn = get_db_connection()
        admin = conn.execute('SELECT * FROM admins WHERE id = ?', (admin_id,)).fetchone()
        conn.close()
        return admin


class ActivityModel:
    @staticmethod
    def create(title, description, event_time, location, capacity):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''
            INSERT INTO activities (title, description, event_time, location, capacity, is_full)
            VALUES (?, ?, ?, ?, ?, 0)
            ''',
            (title, description, event_time, location, capacity)
        )
        conn.commit()
        activity_id = cursor.lastrowid
        conn.close()
        return activity_id

    @staticmethod
    def get_all():
        conn = get_db_connection()
        activities = conn.execute('SELECT * FROM activities ORDER BY created_at DESC').fetchall()
        conn.close()
        return activities

    @staticmethod
    def get_by_id(activity_id):
        conn = get_db_connection()
        activity = conn.execute('SELECT * FROM activities WHERE id = ?', (activity_id,)).fetchone()
        conn.close()
        return activity

    @staticmethod
    def update(activity_id, title, description, event_time, location, capacity, is_full):
        conn = get_db_connection()
        conn.execute(
            '''
            UPDATE activities 
            SET title = ?, description = ?, event_time = ?, location = ?, capacity = ?, is_full = ?
            WHERE id = ?
            ''',
            (title, description, event_time, location, capacity, is_full, activity_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def update_full_status(activity_id, is_full):
        conn = get_db_connection()
        conn.execute(
            'UPDATE activities SET is_full = ? WHERE id = ?',
            (is_full, activity_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def delete(activity_id):
        conn = get_db_connection()
        conn.execute('DELETE FROM activities WHERE id = ?', (activity_id,))
        conn.commit()
        conn.close()


class RegistrationModel:
    @staticmethod
    def create(activity_id, name, student_id, email, phone):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''
            INSERT INTO registrations (activity_id, name, student_id, email, phone)
            VALUES (?, ?, ?, ?, ?)
            ''',
            (activity_id, name, student_id, email, phone)
        )
        conn.commit()
        registration_id = cursor.lastrowid
        conn.close()
        return registration_id

    @staticmethod
    def get_by_activity_id(activity_id):
        conn = get_db_connection()
        registrations = conn.execute(
            'SELECT * FROM registrations WHERE activity_id = ? ORDER BY created_at ASC',
            (activity_id,)
        ).fetchall()
        conn.close()
        return registrations

    @staticmethod
    def count_by_activity_id(activity_id):
        conn = get_db_connection()
        result = conn.execute(
            'SELECT COUNT(*) as count FROM registrations WHERE activity_id = ?',
            (activity_id,)
        ).fetchone()
        conn.close()
        return result['count']

    @staticmethod
    def delete(registration_id):
        conn = get_db_connection()
        conn.execute('DELETE FROM registrations WHERE id = ?', (registration_id,))
        conn.commit()
        conn.close()
