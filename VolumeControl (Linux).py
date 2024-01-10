#The same fuction but for linux with pulsectl

import cv2
import mediapipe as mp
import pulsectl

def change_volume():
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)

    cap = cv2.VideoCapture(0)
    screen_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    screen_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    image_rgb = np.zeros((screen_height, screen_width, 3), dtype=np.uint8)

    pulse = pulsectl.Pulse('volume-control')

    top_margin = 10
    bottom_margin = 10
    max_volume_y = screen_height - top_margin
    min_volume_y = bottom_margin

    while True:
        success, frame = cap.read()
        if not success:
            print("Issues in Camera")
            break

        frame = cv2.flip(frame, 1)
        image_rgb[:,:,:] = frame

        results = hands.process(image_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                index_finger_landmark = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                index_finger_x = int(index_finger_landmark.x * screen_width)
                index_finger_y = int(index_finger_landmark.y * screen_height)

                new_volume = (index_finger_y - min_volume_y) / (max_volume_y - min_volume_y)
                new_volume = max(0.0, min(1.0, new_volume))

                sink_input = pulse.sink_input_list()[0]
                pulse.volume_change_all_chans(sink_input, new_volume)

                cv2.rectangle(image_rgb, (index_finger_x - 10, index_finger_y - 10), (index_finger_x + 10, index_finger_y + 10), (255, 255, 255), 2)
                cv2.line(image_rgb, (0, index_finger_y), (screen_width, index_finger_y), (0, 255, 0), 3)

        cv2.imshow('Live Video', image_rgb)

        if cv2.waitKey(1) & 0xFF == ord(' '):
            break

    cap.release()
    cv2.destroyAllWindows()

    pulse.close()

if __name__ == "__main__":
    print("To close this [Press Space bar].")
    change_volume()
