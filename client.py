import threading
import webview
from app import app

def run_server():
    app.run_server(port=8888)

if __name__ == '__main__':
    t = threading.Thread(target=run_server)
    t.daemon = True
    t.start()
    webview.create_window("Dash客户端", "http://127.0.0.1:8888")
    webview.start()
