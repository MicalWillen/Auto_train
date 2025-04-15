import socket
import threading
import time

class PDCA:
    def __init__(self):
        self.socket = None
        self.server_socket = None
        self.ip_endpoint = None
        self.is_pdca_error = False
        self.now_pdca_status = "NA"
        self.result = bytearray(1024)
        self.port = 1111

    def init(self):
        self.ip_endpoint = ("127.0.0.1", 8080)
        self._create_socket(timeout=30)

    def init_robot(self):
        self.ip_endpoint = ("192.168.1.100", 8885)
        self._create_socket(timeout=60)

    def init_readbar(self):
        self.ip_endpoint = ("192.168.20.10", 23)
        self._create_socket(timeout=30)

    def _create_socket(self, timeout):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(timeout)

    def init_server(self):
        ip = "192.168.1.157"
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((ip, self.port))
        self.server_socket.listen(10)
        print(f"启动监听 {ip}:{self.port} 成功")
        threading.Thread(target=self.listen_client_connect, daemon=True).start()

    def listen_client_connect(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            client_socket.send(b"123")
            threading.Thread(target=self.receive_message, args=(client_socket,), daemon=True).start()

    def receive_message(self, client_socket):
        while True:
            try:
                receive_number = client_socket.recv_into(self.result)
                message = self.result[:receive_number].decode("ascii")
                print(f"接收客户端 {client_socket.getpeername()} 消息: {message}")
                time.sleep(0.05)
                client_socket.send(b"234")
            except Exception as ex:
                print(f"错误: {ex}")
                client_socket.close()
                break

    def connect(self, target):
        if target == "Robot":
            self.init_robot()
        elif target == "PDCA":
            self.init()
        elif target == "ReadBar":
            self.init_readbar()

        connect_attempts = 0
        while connect_attempts < 5:
            try:
                self.socket.connect(self.ip_endpoint)
                self.now_pdca_status = "Connected to PMM Server"
                self.is_pdca_error = False
                break
            except Exception as ex:
                connect_attempts += 1
                self.now_pdca_status = f"No PMM server connected. ERROR: {ex}"
                self.is_pdca_error = True
                time.sleep(0.05)

    def disconnect(self):
        if self.socket:
            self.socket.close()
            self.socket = None

    def recv_msg_by_client(self):
        try:
            recv_msg = self.socket.recv(1024)
            message = recv_msg.decode("utf-8")
            if "ERROR" in message:
                self.is_pdca_error = True
            else:
                self.now_pdca_status = message
        except Exception as ex:
            self.now_pdca_status = str(ex)
            self.is_pdca_error = True

    def send_msg_by_client(self, message):
        message = message.replace("\r\n", "").encode("utf-8")
        try:
            self.socket.sendall(message)
        except Exception as ex:
            self.is_pdca_error = True
            self.now_pdca_status = str(ex)

    def check_status(self):
        return self.is_pdca_error
if __name__ == "__main__":
    Tom=PDCA()
    Tom.connect("PDCA")
    Tom.send_msg_by_client("1234567890")
    Tom.recv_msg_by_client()
    # time.sleep(400)
    print(Tom.now_pdca_status)
    
