from app import create_app

app = create_app()

if __name__ == '__main__':
    # 以 debug 模式啟動開發伺服器
    app.run(debug=True)
