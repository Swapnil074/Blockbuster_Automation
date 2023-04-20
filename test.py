import cv2
import numpy as np
import subprocess
import time

# Specify the package name and activity name of the game
package_name = "com.block.juggle"
activity_name = "org.cocos2dx.javascript.AppActivity"

# Define a function to send ADB commands
def adb(cmd):
    output = subprocess.check_output(["adb"] + cmd.split()).decode()
    return output.strip()

# Launch the game
adb("shell am start -n {}/{}".format(package_name, activity_name))
time.sleep(2)

# Define constants for screen size and block size
SCREEN_WIDTH = 720
SCREEN_HEIGHT = 1280
BLOCK_SIZE = 72

# Define a function to find the location of the current block
def find_block_location(frame):
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Threshold the grayscale image to create a binary image
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

    # Find the contours in the binary image
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Loop over the contours to find the largest rectangle that corresponds to the block
    max_area = 0
    max_rect = None
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > max_area:
            rect = cv2.minAreaRect(contour)
            box = cv2.boxPoints(rect)
            box=np.int8(box)
            # box = np.int0(box)
            w, h = rect[1]
            if abs(w - BLOCK_SIZE) < 10 and abs(h - BLOCK_SIZE) < 10:
                max_area = area
                max_rect = box

    # Return the location of the block
    if max_rect is not None:
        x, y = np.mean(max_rect, axis=0).astype(int)
        return x, y
    else:
        return None

# Define a function to send a swipe command to move the block left or right
def swipe(direction):
    if direction == "left":
        adb("shell input swipe 300 800 100 800")
    elif direction == "right":
        adb("shell input swipe 100 800 300 800")

# Open the device's camera and start capturing frames
cap = cv2.VideoCapture(0)
while True:
    # Capture a frame from the camera
    _, frame = cap.read()

    # Resize the frame to the desired screen size
    frame = cv2.resize(frame, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Find the location of the current block
    block_location = find_block_location(frame)

    # If the block location is found, move the block left or right depending on its position
    if block_location is not None:
        x, y = block_location
        if x < SCREEN_WIDTH / 2:
            swipe("left")
        else:
            swipe("right")

    # Display the frame for debugging purposes
    cv2.imshow("frame", frame)
    if cv2.waitKey(1) == ord('q'):
        break

# Release the camera and close the window
cap.release()
cv2.destroyAllWindows()

# Quit the game
adb("shell am force-stop {}".format(package_name))
