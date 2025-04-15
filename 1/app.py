from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import time
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

def generate_logs():
    """ 模拟生成日志的后台线程 """
    while True:
        socketio.sleep(1)
        log_message = f"Log entry at {time.strftime('%Y-%m-%d %H:%M:%S')}"
        socketio.emit('log', {'data': log_message})

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('start_process')
def start_process():
    """ 处理客户端的启动请求 """
    emit('log', {'data': 'Starting process...'})
    # 启动后台线程来生成日志
    thread = threading.Thread(target=generate_logs)
    thread.daemon = True
    thread.start()

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5001)
