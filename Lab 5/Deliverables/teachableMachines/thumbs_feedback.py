# thumbs_feedback.py
import cv2
import time
import numpy as np
import HandTrackingModule as htm
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789

# ============ PiTFT Setup ============
cs_pin = digitalio.DigitalInOut(board.D5) 
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None
BAUDRATE = 64000000
spi = board.SPI()

disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

# Create image for drawing
height = disp.width
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90
draw = ImageDraw.Draw(image)

# Load font
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 48)

# Turn on backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

# ============ Camera Setup ============
wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = htm.handDetector(detectionCon=int(0.7))

def update_display(status):
    """Update PiTFT display based on gesture"""
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    
    if status == "thumbs_up":
        # Green background with thumbs up
        draw.rectangle((0, 0, width, height), fill=(0, 255, 0))
        draw.text((60, 40), "👍", font=font, fill=(255, 255, 255))
        draw.text((15, 100), "Thumbs Up!", font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36), fill=(255, 255, 255))
    elif status == "thumbs_down":
        # Red background with thumbs down
        draw.rectangle((0, 0, width, height), fill=(255, 0, 0))
        draw.text((60, 40), "👎", font=font, fill=(255, 255, 255))
        draw.text((5, 100), "Thumbs Down!", font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 32), fill=(255, 255, 255))
    else:
        # Black/neutral
        draw.rectangle((0, 0, width, height), fill=(0, 0, 0))
        draw.text((20, 60), "Waiting...", font=font, fill=(100, 100, 100))
    
    disp.image(image, rotation)

def detect_thumbs_orientation(lmList):
    """Detect if thumb is pointing up or down"""
    if len(lmList) == 0:
        return "neutral"
    
    # Get thumb tip (4) and thumb base (2)
    thumb_tip_y = lmList[4][2]
    thumb_base_y = lmList[2][2]
    
    # Get other fingertips to check if fist is closed
    pointer_tip_y = lmList[8][2]
    middle_tip_y = lmList[12][2]
    ring_tip_y = lmList[16][2]
    pinky_tip_y = lmList[20][2]
    
    # Get knuckle positions (approximate base of fingers)
    pointer_knuckle_y = lmList[6][2]
    middle_knuckle_y = lmList[10][2]
    ring_knuckle_y = lmList[14][2]
    pinky_knuckle_y = lmList[18][2]
    
    # Check if other fingers are closed (tips below knuckles)
    fingers_closed = (
        pointer_tip_y > pointer_knuckle_y and
        middle_tip_y > middle_knuckle_y and
        ring_tip_y > ring_knuckle_y and
        pinky_tip_y > pinky_knuckle_y
    )
    
    # Thumbs up: thumb tip is above thumb base, other fingers closed
    if thumb_tip_y < thumb_base_y - 30 and fingers_closed:
        return "thumbs_up"
    # Thumbs down: thumb tip is below thumb base, other fingers closed
    elif thumb_tip_y > thumb_base_y + 30 and fingers_closed:
        return "thumbs_down"
    else:
        return "neutral"

# Initialize display
update_display("neutral")

print("Starting thumbs detection... Press 'q' to quit")

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    
    # Detect gesture
    gesture = detect_thumbs_orientation(lmList)
    
    # Update display
    update_display(gesture)
    
    # Show debug info on camera feed
    if len(lmList) != 0:
        thumb_tip_y = lmList[4][2]
        thumb_base_y = lmList[2][2]
        cv2.putText(img, f'Gesture: {gesture}', (40, 50), cv2.FONT_HERSHEY_COMPLEX,
                    1, (0, 255, 0), 2)
        cv2.putText(img, f'Thumb: {thumb_tip_y - thumb_base_y}', (40, 90), cv2.FONT_HERSHEY_COMPLEX,
                    1, (0, 255, 0), 2)
    
    # Calculate FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime) if pTime > 0 else 0
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (40, 130), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 2)
    
    cv2.imshow("Thumbs Detection", img)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
