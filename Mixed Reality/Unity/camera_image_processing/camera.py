# import cv2
# import numpy as np

# def find_ball_position(frame):
#     # 转换到HSV色彩空间
#     hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

#     # 定义小球的颜色范围
#     lower_color = np.array([0, 231, 40])
#     upper_color = np.array([25, 255, 151])

#     # 根据颜色创建掩膜
#     mask = cv2.inRange(hsv, lower_color, upper_color)

#     # 应用掩膜
#     masked_frame = cv2.bitwise_and(frame, frame, mask=mask)

#     # 寻找掩膜上的轮廓
#     contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

#     # 初始化最接近圆形的轮廓
#     ball_contour = None
#     max_circularity = 0
    
#     for contour in contours:
#         perimeter = cv2.arcLength(contour, True)
#         area = cv2.contourArea(contour)
        
#         # 忽略过小的轮廓
#         if area < 10:
#             continue
            
#         # 计算轮廓的圆形度（circularity）
#         if perimeter == 0:
#             continue
#         circularity = 4 * np.pi * (area / (perimeter * perimeter))
        
#         # 检查圆形度是否大于某个阈值，例如0.8
#         if circularity > 0.8 and circularity > max_circularity:
#             ball_contour = contour
#             max_circularity = circularity

#     # 如果找到了小球轮廓
#     if ball_contour is not None:
#         # 找到最小覆盖圆形的中心和半径
#         (x, y), radius = cv2.minEnclosingCircle(ball_contour)
#         center = (int(x), int(y))
#         radius = int(radius)
#         # 画出最小覆盖圆
#         cv2.circle(frame, center, radius, (0, 255, 0), 2)

#         # 画出方框
#         x1 = int(x - radius)
#         y1 = int(y - radius)
#         x2 = int(x + radius)
#         y2 = int(y + radius)
#         cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        
#         # 返回带有标记的帧和小球位置
#         return frame, center
#     return frame, None

# def pixel_to_space(x_pixel, y_pixel, x1, y1, x2, y2, space1, space2):


#     x_space1, y_space1 = space1
#     x_space2, y_space2 = space2

#     x_space= x_space1+ (x_pixel-x1)*(x_space2-x_space1)/(x2-x1)
#     y_space= y_space1+ (y_pixel-y1)*(y_space2-y_space1)/(y2-y1)


#     return (x_space, y_space)

# # 用摄像头捕捉视频
# cap = cv2.VideoCapture(0)

# # # 假设已知的正方形顶点的像素坐标和空间坐标
# x1, y1 = 130, 451  # 左下角像素坐标
# x2, y2 = 556, 23  # 右上角像素坐标
# space1 = (-0.125, 0.875)  # 左下角空间坐标
# space2 = (0, 1)           # 右上角空间坐标

# while True:
#     # 捕捉帧-by-帧
#     ret, frame = cap.read()

#     if not ret:
#         break

#     # 调用函数找到小球位置
#     frame_with_ball, position = find_ball_position(frame)

#     # 显示结果帧
#     cv2.imshow('Frame with Ball', frame_with_ball)

#     # 打印小球位置
#     if position is not None:
#         # 将小球的像素坐标转换为空间坐标
#         space_position = pixel_to_space(position[0], position[1], x1, y1, x2, y2, space1, space2)
#         print("Ball Position in Space Coordinates:", space_position)

#     # 按'q'退出循环
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # 当一切完成后，释放捕捉
# cap.release()
# cv2.destroyAllWindows()

import cv2
import numpy as np
import socket

def find_ball_position(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_color = np.array([0, 231, 40])
    upper_color = np.array([25, 255, 140])
    mask = cv2.inRange(hsv, lower_color, upper_color)
    masked_frame = cv2.bitwise_and(frame, frame, mask=mask)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    ball_contour = None
    max_circularity = 0

    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        area = cv2.contourArea(contour)
        if area < 10 or perimeter == 0:
            continue
        circularity = 4 * np.pi * (area / (perimeter ** 2))
        if circularity > 0.9 and circularity > max_circularity:
            ball_contour = contour
            max_circularity = circularity

    if ball_contour is not None:
        (x, y), radius = cv2.minEnclosingCircle(ball_contour)
        center = (int(x), int(y))
        radius = int(radius)
        cv2.circle(frame, center, radius, (0, 255, 0), 2)
        x1 = int(x - radius)
        y1 = int(y - radius)
        x2 = int(x + radius)
        y2 = int(y + radius)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        return frame, center
    return frame, None

def pixel_to_space(x_pixel, y_pixel, x1, y1, x2, y2, space1, space2):
    x_space1, y_space1 = space1
    x_space2, y_space2 = space2
    x_space = x_space1 + (x_pixel - x1) * (x_space2 - x_space1) / (x2 - x1)
    y_space = y_space1 + (y_pixel - y1) * (y_space2 - y_space1) / (y2 - y1)
    return (x_space, y_space)

# Setup TCP client
host = 'localhost'
port = 12345
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

# Capture video
cap = cv2.VideoCapture(0)
x1, y1 = 134, 467
x2, y2 = 593, 13
space1 = (-0.125, 0.875)
space2 = (0, 1)
last_position = None  # Store the last valid position

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_with_ball, position = find_ball_position(frame)
        cv2.imshow('Frame with Ball', frame_with_ball)

        if position is not None:
            if last_position is None or (abs(position[0] - last_position[0]) <= 20 and abs(position[1] - last_position[1]) <= 50):
                space_position = pixel_to_space(position[0], position[1], x1, y1, x2, y2, space1, space2)
                print("Ball Position in Space Coordinates:", space_position)
                message = f"{space_position[0]},{space_position[1]}\n"
                client_socket.sendall(message.encode())
                last_position = position  # Update last valid position
            else:
                print("Detected position jump, skipping this position")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    cap.release()
    cv2.destroyAllWindows()
    client_socket.close()
