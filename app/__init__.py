from flask import Flask
import os

def create_app():
    # 建立與設定 Flask App
    app = Flask(__name__, instance_relative_config=True)
    
    # 預設基本設定
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
        DATABASE=os.path.join(app.instance_path, 'database.db'),
    )

    # 確保 instance 資料夾存在，用於存放 SQLite 資料庫
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 註冊 Blueprints (路由)
    from .routes.main import main_bp
    from .routes.auth import auth_bp
    from .routes.donation import donation_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(donation_bp)

    return app

def init_db():
    app = create_app()
    import sqlite3
    with app.app_context():
        db_path = app.config['DATABASE']
        # 確保資料庫路徑存在
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        conn = sqlite3.connect(db_path)
        
        # 讀取 schema.sql 並執行建表
        schema_path = os.path.join(app.root_path, '..', 'database', 'schema.sql')
        with open(schema_path, 'r', encoding='utf-8') as f:
            conn.executescript(f.read())
        
        conn.commit()
        conn.close()
        print(f"Database initialized at {db_path}")
