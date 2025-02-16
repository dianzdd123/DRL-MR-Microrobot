import cv2
import numpy as np

def nothing(x):
    pass

# 创建一个窗口
cv2.namedWindow('image')

# 创建轨迹条，分别为H、S、V的上下界
cv2.createTrackbar('H_low', 'image', 0, 179, nothing)
cv2.createTrackbar('H_high', 'image', 0, 179, nothing)
cv2.createTrackbar('S_low', 'image', 0, 255, nothing)
cv2.createTrackbar('S_high', 'image', 0, 255, nothing)
cv2.createTrackbar('V_low', 'image', 0, 255, nothing)
cv2.createTrackbar('V_high', 'image', 0, 255, nothing)

# 加载图片
# 这里你需要替换为你自己的图片路径
img = cv2.imread('C:\\Users\\maoyudong\\Desktop\\sensapexUmp\\image\\image.PNG')
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

while(True):
    # 获取轨迹条的位置
    h_low = cv2.getTrackbarPos('H_low', 'image')
    h_high = cv2.getTrackbarPos('H_high', 'image')
    s_low = cv2.getTrackbarPos('S_low', 'image')
    s_high = cv2.getTrackbarPos('S_high', 'image')
    v_low = cv2.getTrackbarPos('V_low', 'image')
    v_high = cv2.getTrackbarPos('V_high', 'image')

    # 创建HSV阈值范围
    lower_bound = np.array([h_low, s_low, v_low])
    upper_bound = np.array([h_high, s_high, v_high])

    # 应用阈值
    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    result = cv2.bitwise_and(img, img, mask=mask)

    # 显示结果
    cv2.imshow('mask', mask)
    cv2.imshow('image', result)

    # 按'q'键退出循环
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放所有窗口
cv2.destroyAllWindows()
