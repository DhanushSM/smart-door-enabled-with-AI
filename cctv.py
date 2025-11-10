import cv2
import requests
import base64

# Initialize the camera
cap = cv2.VideoCapture(0)  # 0 for the default camera (change if needed)

# Initialize the face recognition model (you need to train this model)
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

allow_entry = False  # Flag to control entry

while True:
    # Read a frame from the camera
    ret, frame = cap.read()

    # Detect faces in the frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

    # Capture and send a single face image
    if len(faces) > 0:
        (x, y, w, h) = faces[0]  # Capture the first detected face
        face_img = frame[y:y+h, x:x+w]  # Extract the face image

        # Encode the face image as base64
        _, encoded_face = cv2.imencode('.jpg', face_img)
        face_base64 = base64.b64encode(encoded_face).decode('utf-8')

        # Send the encoded face image to a server (replace with your server details)
        server_url = 'https://your-server-url.com/upload_face'
        data = {'face_image': face_base64}
        response = requests.post(server_url, data=data)

        # Handle the response from the server as needed
        print("Face image sent to server. Response:", response.text)

        # Check if the user wants to allow entry
        if allow_entry:
            # Implement logic to open the door or take appropriate action
            print("Entry allowed. Opening the door.")
            allow_entry = False  # Reset the flag

    # Display the frame with face rectangles
    cv2.imshow('Smart Door Camera', frame)

    # Check for user input ('a' key for allow)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('a'):
        allow_entry = True  # Set the flag to allow entry

    # Break the loop if 'q' key is pressed
    elif key == ord('q'):
        break

# Release the camera and close the OpenCV window
cap.release()
cv2.destroyAllWindows()