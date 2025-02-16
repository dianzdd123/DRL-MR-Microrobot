import socket
from sensapex import UMP
import math
from collections import deque
from filterpy.kalman import KalmanFilter
import numpy as np

# 创建TCP套接字
server_ip = "0.0.0.0"  # 监听所有网络接口
server_port = 22345  # 与Unity脚本中的端口一致
buffer_size = 1024

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip, server_port))
server_socket.listen(1)
print("TCP server up and listening")

# 获取UMP实例
ump = UMP.get_ump()

# 获取两个机器人设备
robot1 = ump.get_device(1)
robot2 = ump.get_device(2)

# 初始中心坐标和角度
center_x, center_y = 10000, 10000
theta = 0.0
L = 2000  # 两个机器人之间的固定距离

# 准备缓冲区
buffer = ""

# 初始化卡尔曼滤波器
kf_x = KalmanFilter(dim_x=2, dim_z=1)
kf_y = KalmanFilter(dim_x=2, dim_z=1)
kf_theta = KalmanFilter(dim_x=2, dim_z=1)

# 配置卡尔曼滤波器
def initialize_kf(kf):
    kf.x = np.array([[0.], [0.]])  # 初始状态
    kf.F = np.array([[1., 1.], [0., 1.]])  # 状态转移矩阵
    kf.H = np.array([[1., 0.]])  # 观测矩阵
    kf.P *= 1000.  # 初始化协方差矩阵
    kf.R = 5  # 观测噪声协方差
    kf.Q = np.array([[0.01, 0.], [0., 0.01]])  # 过程噪声协方差

initialize_kf(kf_x)
initialize_kf(kf_y)
initialize_kf(kf_theta)

def calculate_positions(x, y, theta, L):
    # 将theta转换为弧度
    theta_rad = math.radians(theta)
    
    # 计算两个机器人的新位置
    x1 = x - (L / 2) * math.cos(theta_rad)
    x2 = x + (L / 2) * math.cos(theta_rad)
    y1 = y - (L / 2) * math.sin(theta_rad)
    y2 = y + (L / 2) * math.sin(theta_rad)
    
    return (x1, y1), (x2, y2)

# 接受一个新连接
conn, addr = server_socket.accept()
print(f"Connected to {addr}")

try:
    while True:
        # 接收数据并添加到缓冲区
        buffer += conn.recv(buffer_size).decode('utf-8')

        # 处理缓冲区中的每一条完整消息
        while '\n' in buffer:
            # 按照换行符分割消息
            line, buffer = buffer.split('\n', 1)

            # 解析消息
            parts = line.split(',')
            if len(parts) == 3:
                deltax, deltay, deltaz = map(float, parts)
                
                # 使用卡尔曼滤波来平滑数据
                kf_x.predict()
                kf_x.update(deltax)
                smooth_deltax = kf_x.x[0][0]

                kf_y.predict()
                kf_y.update(deltay)
                smooth_deltay = kf_y.x[0][0]
                
                # 计算新的theta角（仅使用x和y）
                if smooth_deltax != 0:
                    theta = math.degrees(math.atan2(smooth_deltay, smooth_deltax))
                    # 确保theta在0到180度之间
                    if theta < 0:
                        theta += 180  # 如果theta小于0，加180度
                    elif theta > 180:
                        theta = (theta + 180) % 360  # 如果theta大于180度，加180度后取模360
                    
                    theta -= 90
                    
                    kf_theta.predict()
                    kf_theta.update(theta)
                    smooth_theta = kf_theta.x[0][0]
                else:
                    smooth_theta = 0  # 如果没有变化，则假设theta为0

                # 将角度按10度向下取整
                corrected_theta = math.floor(smooth_theta / 10) * 10

                # 使用修正后的角度修正增量
                corrected_theta_rad = math.radians(corrected_theta)
                corrected_deltax = smooth_deltax * math.cos(corrected_theta_rad) - smooth_deltay * math.sin(corrected_theta_rad)
                corrected_deltay = smooth_deltax * math.sin(corrected_theta_rad) + smooth_deltay * math.cos(corrected_theta_rad)

                # 更新中心坐标
                center_x += corrected_deltax * 20000  # 这里的因子根据实际情况调整
                center_y += corrected_deltay * 20000

                # 计算两个机器人的新位置
                pos1, pos2 = calculate_positions(center_x, 20000-center_y, corrected_theta, L)
                
                # 发送命令给机器人
                # robot1.goto_pos((pos1[0], pos1[1], 11500, 10000), 10000)
                # robot2.goto_pos((20000-pos2[0], 20000-pos2[1],11500, 10000), 10000)
                
                # 打印调试信息
                # print("pos1[0], pos1[1]", pos1[0], pos1[1])
                # print("pos2[0], pos2[1]", 20000-pos2[0], 20000-pos2[1])
                print("center_x", center_x, "center_y", 20000-center_y, "theta", corrected_theta)
            else:
                # 如果消息格式不正确，打印错误信息
                print(f"Unexpected data format: {line}")

except KeyboardInterrupt:
    print("Server stopped by user")

finally:
    # 关闭连接和套接字
    conn.close()
    server_socket.close()
