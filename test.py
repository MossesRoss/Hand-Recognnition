import mediapipe as mp
import cv2

# Create a MediaPipe hand gesture recognizer
gestureRecognizer = mp.solutions.hands.Hands(maxNumHands=2, minDetectionConfidence=0.5, minTrackingConfidence=0.5)

# Define the important hand gestures
importantHandGestures = ["Fist", "Open Palm", "Thumbs Up", "Thumbs Down"]

# Start the video capture
cap = cv2.VideoCapture(0)

while True:
    # Capture a frame from the video
    ret, frame = cap.read()

    # Convert the frame to RGB
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with the gesture recognizer
    results = gestureRecognizer.process(frame)

    # Get the hand landmarks
    handLandmarks = results.multiHandLandmarks

    # Iterate over the hand landmarks
    for handLandmark in handLandmarks:
        # Get the hand gesture
        handGesture = results.multiHandLandmarks[0].handLandmarks.classification[0].label

        # Check if the hand gesture is one of the important gestures
        if handGesture in importantHandGestures:
            # Display the hand gesture on the frame
            cv2.putText(frame, handGesture, (handLandmark.indexFingerTip.x, handLandmark.indexFingerTip.y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Display the frame
    cv2.imshow("Frame", frame)

    # If the user presses the Q key, break the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture
cap.release()

# Close all windows
cv2.destroyAllWindows()
