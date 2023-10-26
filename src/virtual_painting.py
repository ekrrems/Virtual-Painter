import cv2
import mediapipe as mp
import numpy as np
import utils

# Initialize MediaPipe Hands module and set up drawing utilities
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Read the header image and resize it
header_img = cv2.imread(r"images\virtual_painter.png")
header_img = cv2.resize(header_img, (640, 120))
header_img_2 = cv2.resize(cv2.imread(r"images\virtual_painter.png"), (640, 120))

# Open the webcam (camera)
cap = cv2.VideoCapture(0)

# Create a canvas for drawing
canvas = np.zeros((480, 640, 3), dtype=np.uint8)
xp, yp = 0, 0
color_id = 1
drawing_color = utils.draw_color(color_id)
change = False

def finger_distance(x1, y1, x2, y2, frame):
    # Calculate the distance between two finger points
    w = frame.shape[1]
    h = frame.shape[0]
    dist = round(np.sqrt((x2 * w - x1 * w)**2 + (y2 * h - y1 * h)**2), 2)
    return dist

# Initialize the MediaPipe Hands module
with mp_hands.Hands(model_complexity=0, min_detection_confidence=0.5, min_tracking_confidence=0.5, max_num_hands=1) as hands:
    while cap.isOpened():
        if change:
            header_img = header_img_2.copy()
            utils.choose_color(color_id, header_img)
            change = False
        
        success, frame = cap.read()
        w = frame.shape[1]
        h = frame.shape[0]

        if not success:
            print("Empty camera frame.")
            continue

        # Flip the frame horizontally
        frame = cv2.flip(frame, 1)
        frame.flags.writeable = False
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame)

        # Draw the hand annotations on the image
        frame.flags.writeable = True
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]

                # Calculate the distance between two finger points
                distance = finger_distance(index_tip.x, index_tip.y, middle_tip.x, middle_tip.y, frame=frame)

                # Display the distance on the frame
                cv2.putText(frame, f"Distance: {distance:.2f}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

                if xp == 0 and yp == 0:
                    xp, yp = index_tip.x * w, index_tip.y * h

                if distance > 70:
                    start_point = (int(xp), int(yp))
                    end_point = (int(index_tip.x * w), int(index_tip.y * h))

                    if color_id == 6:
                        cv2.line(canvas, start_point, end_point, drawing_color, 10)
                    else:
                        cv2.line(canvas, start_point, end_point, drawing_color, 3)
                else: 
                    change, color_id = utils.select_pen((index_tip.x * w, index_tip.y * h))
                    drawing_color = utils.draw_color(color_id)
                    
                xp, yp = index_tip.x * w, index_tip.y * h

        # Prepare the canvas for overlay
        grayscale_canvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
        _, canvas_inv = cv2.threshold(grayscale_canvas, 10, 255, cv2.THRESH_BINARY_INV)
        canvas_inv = cv2.cvtColor(canvas_inv, cv2.COLOR_GRAY2BGR)
        frame = cv2.bitwise_and(frame, canvas_inv)
        frame = cv2.bitwise_or(frame, canvas)
        
        # Overlay the header image on top of the frame
        frame[:120, :] = header_img

        # Display the frame with the canvas
        cv2.imshow('Canvas', frame)

        if cv2.waitKey(5) & 0xFF == ord("q"):
            break

# Release the camera and close OpenCV windows
cap.release()
cv2.destroyAllWindows()