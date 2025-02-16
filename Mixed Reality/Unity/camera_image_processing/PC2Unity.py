import cv2
import socket
import struct
import pickle

# 初始化摄像头
cap = cv2.VideoCapture(0)
# 创建 socket 对象
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print('HOST IP:', host_ip)
port = 9999
socket_address = (host_ip, port)

# 绑定端口
server_socket.bind(socket_address)

# 监听请求
server_socket.listen(5)
print("监听端口:", socket_address)

# 等待客户端连接
while True:
    client_socket, addr = server_socket.accept()
    print('连接地址:', addr)
    if client_socket:
        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                a = pickle.dumps(frame)
                message = struct.pack("Q", len(a)) + a
                client_socket.sendall(message)
                
            else:
                break
        client_socket.close()
