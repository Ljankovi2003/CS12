import cv2
import numpy as np
import apriltag
import serial
import time

# Set up serial connection to Arduino
# Replace '/dev/ttyUSB0' with your actual serial port (e.g., '/dev/ttyACM0' or 'COMx' for Windows)
arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)  # Update to correct port
time.sleep(2)  # Give Arduino time to initialize

# Initialize Webcam
cap = cv2.VideoCapture(0)  # Use 0 for the default camera

# Initialize AprilTag Detector
options = apriltag.DetectorOptions(families="tag36h11")  # Standard family
detector = apriltag.Detector(options)

# Function to handle detected tags and send messages to Arduino
def send_to_arduino(tag_id):
    # Send the tag ID to Arduino over the serial connection
    arduino.write(f"{tag_id}\n".encode())  # Add a newline to mark the end of the message
    print(f"Sent to Arduino: {tag_id}")

# Main loop to detect AprilTags and send messages to Arduino
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert to Grayscale (AprilTag requires grayscale images)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect AprilTags
    results = detector.detect(gray)

    # Handle detected tags
    for result in results:
        tag_id = result.tag_id
        print(tag_id)
        
        if tag_id == 558:

            # Send the tag ID to Arduino over serial
            send_to_arduino(tag_id)
        if tag_id == 570:
            print("SENT")
            send_to_arduino(558)

        # Optional: Draw bounding box and center (for visualization if needed)
        for i in range(4):
            pt1 = tuple(result.corners[i].astype(int))
            pt2 = tuple(result.corners[(i+1) % 4].astype(int))
            cv2.line(frame, pt1, pt2, (0, 255, 0), 2)

        # Draw center point
        center = tuple(result.center.astype(int))
        cv2.circle(frame, center, 5, (0, 0, 255), -1)

        # Display Tag ID (Optional, can be skipped in headless mode)
        cv2.putText(frame, f"ID: {tag_id}", (center[0] - 10, center[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    # Optionally save the frame for debugging (uncomment if needed)
    # cv2.imwrite("captured_image.jpg", frame)

    # If you need to process data or send it to Arduino or a server, you can do it here
    # Example: send_to_arduino(tag_id)  # Tag ID has already been sent above

    # Exit on some condition (for example, after a number of iterations or time)
    # You can add your own condition to stop the loop, e.g.:
    # if some_condition:
    #     break

# Release the camera and close the serial connection
cap.release()
arduino.close()
