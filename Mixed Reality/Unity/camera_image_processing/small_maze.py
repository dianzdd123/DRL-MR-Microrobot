import cv2
import numpy as np

def find_ball_position(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_color = np.array([15, 6, 43])
    upper_color = np.array([95,95, 80])
    mask = cv2.inRange(hsv, lower_color, upper_color)
    masked_frame = cv2.bitwise_and(frame, frame, mask=mask)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    ball_contour = None
    max_circularity = 0

    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        area = cv2.contourArea(contour)
        if area < 50  or perimeter == 0:
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

# def pixel_to_space(x_pixel, y_pixel, x1, y1, x2, y2, space1, space2):
#     x_space1, y_space1 = space1
#     x_space2, y_space2 = space2
#     x_space = x_space1 + (x_pixel - x1) * (x_space2 - x_space1) / (x2 - x1)
#     y_space = y_space1 + (y_pixel - y1) * (y_space2 - y_space1) / (y2 - y1)
#     return (x_space, y_space)

def pixel_to_space(x_pixel, y_pixel, x1, y1, x2, y2, space1, space2):
    x_space1, y_space1 = space1
    x_space2, y_space2 = space2
    x_space = x_space1 + (x_pixel - x1) * (x_space2 - x_space1) / (x2 - x1)
    y_space = y_space1 + (y_pixel - y1) * (y_space2 - y_space1) / (y2 - y1)
    return (y_space,x_space)

# Capture video
cap = cv2.VideoCapture(0)
x1, y1 = 115, 25
x2, y2 = 554, 455
space1 = (0, 0)
space2 = (0.36, 0.36)
last_position = None  # Store the last valid position

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_with_ball, position = find_ball_position(frame)
        cv2.imshow('Frame with Ball', frame_with_ball)

        if position is not None:
            if last_position is None or (abs(position[0] - last_position[0]) <= 30 and abs(position[1] - last_position[1]) <= 30):
                space_position = pixel_to_space(position[0], position[1], x1, y1, x2, y2, space1, space2)
                print("Ball Position in Space Coordinates:", space_position)
                last_position = position  # Update last valid position
            else:
                print("Detected position jump, skipping this position")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    cap.release()
    cv2.destroyAllWindows()
