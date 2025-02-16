import asyncio
import websockets
import cv2
import numpy as np
import base64

def find_ball_position(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_color = np.array([0, 231, 40])
    upper_color = np.array([25, 255, 151])
    mask = cv2.inRange(hsv, lower_color, upper_color)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        area = cv2.contourArea(contour)
        if area > 10 and perimeter != 0:
            circularity = 4 * np.pi * (area / (perimeter ** 2))
            if circularity > 0.8:
                (x, y), _ = cv2.minEnclosingCircle(contour)
                return int(x), int(y)
    return None

def pixel_to_space(x_pixel, y_pixel, x1, y1, x2, y2, space1, space2):
    x_space = (x_pixel - x1) / (x2 - x1) * (space2[0] - space1[0]) + space1[0]
    y_space = (y_pixel - y1) / (y2 - y1) * (space2[1] - space1[1]) + space1[1]
    return x_space, y_space

async def video_server(websocket, path):
    cap = cv2.VideoCapture(0)
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame")
                break
            _, buffer = cv2.imencode('.jpg', frame)
            jpeg_as_text = base64.b64encode(buffer).decode('utf-8')
            await websocket.send(jpeg_as_text)  # 发送视频帧
            print("haha/n")
    finally:
        cap.release()

async def position_server(websocket, path):
    cap = cv2.VideoCapture(0)
    x1, y1, x2, y2 = 119, 454, 548, 29
    space1, space2 = (-0.125, 0.875), (0, 1)
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame")
                break
            position = find_ball_position(frame)
            if position:
                x, y = position
                space_position = pixel_to_space(x, y, x1, y1, x2, y2, space1, space2)
                position_message = f"{space_position[0]},{space_position[1]}"
                await websocket.send(position_message)  # 发送位置信息
    finally:
        cap.release()

async def main():
    video_task = websockets.serve(video_server, 'localhost', 8765)
    position_task = websockets.serve(position_server, 'localhost', 8766)
    await asyncio.gather(video_task, position_task)

asyncio.run(main())
