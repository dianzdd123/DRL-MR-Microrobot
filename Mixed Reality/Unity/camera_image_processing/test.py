import cv2  # 导入opencv库

# 定义一个回调函数，用于鼠标点击事件
def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Mouse clicked at position: (x={x}, y={y})")

# 初始化摄像头
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Camera could not be accessed.")
    exit()

# 设置分辨率为640x480
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# 创建一个窗口
cv2.namedWindow("Camera")

# 绑定鼠标点击事件到窗口
cv2.setMouseCallback("Camera", click_event)

# 捕捉摄像头帧
while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break

    # 显示图像帧
    cv2.imshow("Camera", frame)

    # 按'q'退出循环
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放摄像头资源并关闭窗口
cap.release()
cv2.destroyAllWindows()
