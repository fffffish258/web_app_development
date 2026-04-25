import os
import sqlite3
from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # 基本設定
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    app.config['DATABASE'] = os.path.join(app.root_path, '..', 'instance', 'database.db')

    # 確保 instance 資料夾存在
    os.makedirs(os.path.join(app.root_path, '..', 'instance'), exist_ok=True)

    # 註冊 Blueprints
    from app.routes.main import main_bp
    from app.routes.admin import admin_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)

    return app

def init_db():
    """初始化資料庫結構 (會清空現有資料)"""
    import os
    db_path = os.path.join(os.path.dirname(__file__), '..', 'instance', 'database.db')
    schema_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'schema.sql')
    
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    with open(schema_path, 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
        
    # 建立預設管理者帳號以便測試 (帳號: admin, 密碼: admin123)
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO admins (username, password_hash) VALUES ('admin', 'admin123')")
    
    conn.commit()
    conn.close()
    print("Database initialized successfully.")
