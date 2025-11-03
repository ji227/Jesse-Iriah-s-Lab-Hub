# thumb_counter.py - Polling system that counts thumbs up/down votes
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

# Load fonts - SMALLER for 240x135 screen
font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
font_count = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
font_label = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)

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

# ============ Vote Counting State Machine ============
vote_state = "neutral"  # States: neutral, counted_up, counted_down, no_hand
thumbs_up_count = 0
thumbs_down_count = 0
STATE_HOLD_TIME = 0.5  # Must hold gesture for 0.5s to register vote
gesture_start_time = None
last_detected_gesture = "neutral"

def draw_up_arrow(x, y, size=15, color=(0, 255, 0)):
    """Draw simple up arrow"""
    # Triangle pointing up
    draw.polygon([
        (x + size//2, y),           # top point
        (x, y + size),               # bottom left
        (x + size, y + size)         # bottom right
    ], fill=color)

def draw_down_arrow(x, y, size=15, color=(255, 0, 0)):
    """Draw simple down arrow"""
    # Triangle pointing down
    draw.polygon([
        (x, y),                      # top left
        (x + size, y),               # top right
        (x + size//2, y + size)      # bottom point
    ], fill=color)

def update_display(current_gesture, up_count, down_count):
    """Update PiTFT display with vote counts - optimized for 240x135"""
    draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 50))  # Dark blue background
    
    # Title
    title = "THUMB COUNTER"
    bbox = draw.textbbox((0, 0), title, font=font_title)
    title_width = bbox[2] - bbox[0]
    x_centered = (width - title_width) // 2
    draw.text((x_centered, 2), title, font=font_title, fill=(255, 255, 255))
    
    # Divider line
    draw.line([(5, 22), (width-5, 22)], fill=(100, 100, 100), width=1)
    
    # UP COUNT - with arrow
    y_pos = 28
    draw_up_arrow(8, y_pos, size=12, color=(0, 255, 0))
    draw.text((25, y_pos-3), "Up:", font=font_label, fill=(200, 200, 200))
    draw.text((130, y_pos-5), str(up_count), font=font_count, fill=(0, 255, 0))
    
    # DOWN COUNT - with arrow
    y_pos = 52
    draw_down_arrow(8, y_pos, size=12, color=(255, 0, 0))
    draw.text((25, y_pos-3), "Down:", font=font_label, fill=(200, 200, 200))
    draw.text((130, y_pos-5), str(down_count), font=font_count, fill=(255, 0, 0))
    
    # Divider line
    draw.line([(5, 75), (width-5, 75)], fill=(100, 100, 100), width=1)
    
    # STATS - Total and Net (side by side)
    total = up_count + down_count
    net = up_count - down_count
    net_sign = "+" if net >= 0 else ""
    
    y_pos = 82
    draw.text((8, y_pos), f"Total: {total}", font=font_label, fill=(255, 255, 255))
    
    # Net with color coding
    net_color = (0, 255, 0) if net > 0 else (255, 0, 0) if net < 0 else (200, 200, 200)
    draw.text((125, y_pos), f"Net: {net_sign}{net}", font=font_label, fill=net_color)
    
    # Divider line
    draw.line([(5, 102), (width-5, 102)], fill=(100, 100, 100), width=1)
    
    # Current state indicator at bottom
    if current_gesture == "thumbs_up":
        status_text = "Voting Up..."
        status_color = (0, 255, 0)
    elif current_gesture == "thumbs_down":
        status_text = "Voting Down..."
        status_color = (255, 0, 0)
    elif current_gesture == "counted_up" or current_gesture == "counted_down":
        status_text = "Vote Counted!"
        status_color = (255, 255, 0)
    elif current_gesture == "neutral":
        status_text = "Ready"
        status_color = (200, 200, 200)
    elif current_gesture == "no_hand":
        status_text = "No hand"
        status_color = (150, 150, 150)
    else:
        status_text = "Waiting..."
        status_color = (200, 200, 200)
    
    bbox = draw.textbbox((0, 0), status_text, font=font_small)
    text_width = bbox[2] - bbox[0]
    x_centered = (width - text_width) // 2
    draw.text((x_centered, 110), status_text, font=font_small, fill=status_color)
    
    # Show "Press R to reset" hint
    hint = "Press R: Reset"
    bbox = draw.textbbox((0, 0), hint, font=font_small)
    text_width = bbox[2] - bbox[0]
    x_centered = (width - text_width) // 2
    draw.text((x_centered, 123), hint, font=font_small, fill=(100, 100, 100))
    
    disp.image(image, rotation)

def detect_thumbs_orientation(lmList):
    """Detect if thumb is pointing up or down"""
    if len(lmList) == 0:
        return "no_hand"
    
    # Get thumb tip (4) and thumb base (2)
    thumb_tip_y = lmList[4][2]
    thumb_base_y = lmList[2][2]
    
    # Get other fingertips to check if fist is closed
    pointer_tip_y = lmList[8][2]
    middle_tip_y = lmList[12][2]
    ring_tip_y = lmList[16][2]
    pinky_tip_y = lmList[20][2]
    
    # Get knuckle positions
    pointer_knuckle_y = lmList[6][2]
    middle_knuckle_y = lmList[10][2]
    ring_knuckle_y = lmList[14][2]
    pinky_knuckle_y = lmList[18][2]
    
    # Check if other fingers are closed
    fingers_closed = (
        pointer_tip_y > pointer_knuckle_y and
        middle_tip_y > middle_knuckle_y and
        ring_tip_y > ring_knuckle_y and
        pinky_tip_y > pinky_knuckle_y
    )
    
    # Thumbs up: thumb tip above base, fingers closed
    if thumb_tip_y < thumb_base_y - 30 and fingers_closed:
        return "thumbs_up"
    # Thumbs down: thumb tip below base, fingers closed
    elif thumb_tip_y > thumb_base_y + 30 and fingers_closed:
        return "thumbs_down"
    else:
        return "neutral"

# Initialize display
update_display("neutral", 0, 0)

print("\n" + "="*50)
print("THUMB COUNTER - Polling System")
print("="*50)
print("\nHow to vote:")
print("1. Show thumbs up or thumbs down")
print("2. Hold for 0.5 seconds")
print("3. Return hand to neutral (or remove from frame)")
print("4. Next person can vote")
print("\nPress 'q' to quit, 'r' to reset counts")
print("="*50 + "\n")


while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    
    # Count hands
    if detector.results and detector.results.multi_hand_landmarks:
        hand_count = len(detector.results.multi_hand_landmarks)
    else:
        hand_count = 0
    
    # Detect gesture (first hand only)
    detected_gesture = detect_thumbs_orientation(lmList)
    current_time = time.time()
    
    # ============ VOTE COUNTING STATE MACHINE ============
    
    if detected_gesture != last_detected_gesture:
        # Gesture changed, reset timer
        gesture_start_time = current_time
        last_detected_gesture = detected_gesture
    
    # Check if gesture held long enough
    gesture_held_time = current_time - gesture_start_time if gesture_start_time else 0
    
    if vote_state == "neutral" or vote_state == "no_hand":
        # Ready to accept new vote
        if detected_gesture == "thumbs_up" and gesture_held_time >= STATE_HOLD_TIME:
            thumbs_up_count += 1
            vote_state = "counted_up"
            print(f"? Vote registered: THUMBS UP (Total: {thumbs_up_count})")
            
        elif detected_gesture == "thumbs_down" and gesture_held_time >= STATE_HOLD_TIME:
            thumbs_down_count += 1
            vote_state = "counted_down"
            print(f"? Vote registered: THUMBS DOWN (Total: {thumbs_down_count})")
    
    elif vote_state == "counted_up" or vote_state == "counted_down":
        # Vote was counted, waiting for return to neutral
        if detected_gesture == "neutral" or detected_gesture == "no_hand":
            vote_state = "neutral"
            print("? Ready for next vote")
    
    # Update display
    display_gesture = detected_gesture if vote_state in ["neutral", "no_hand"] else vote_state
    update_display(display_gesture, thumbs_up_count, thumbs_down_count)
    
    # ============ DEBUG CAMERA FEED ============
    
    # State info
    cv2.putText(img, f'State: {vote_state}', (40, 50), cv2.FONT_HERSHEY_COMPLEX,
                0.9, (255, 255, 0), 2)
    cv2.putText(img, f'Gesture: {detected_gesture}', (40, 90), cv2.FONT_HERSHEY_COMPLEX,
                0.8, (0, 255, 0), 2)
    
    # Vote counts
    cv2.putText(img, f'Up: {thumbs_up_count}  Down: {thumbs_down_count}', (40, 130), 
                cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)
    
    # Gesture timer
    if gesture_held_time < STATE_HOLD_TIME and detected_gesture in ["thumbs_up", "thumbs_down"]:
        progress = int((gesture_held_time / STATE_HOLD_TIME) * 100)
        cv2.putText(img, f'Hold: {progress}%', (40, 170), 
                    cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 255), 2)
    
    # Hand count - MORE DESCRIPTIVE
    cv2.putText(img, f'# of Hands Detected: {hand_count}', (40, 210), cv2.FONT_HERSHEY_COMPLEX,
                0.7, (255, 0, 255), 2)
    
    # FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime) if pTime > 0 else 0
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (40, 430), cv2.FONT_HERSHEY_COMPLEX,
                0.9, (255, 0, 0), 2)
    
    # Show instructions
    cv2.putText(img, 'Press R to reset counts, Q to quit', (40, 250), cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (200, 200, 200), 1)
    
    cv2.imshow("Thumb Counter", img)
    
    # Keyboard controls
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('r') or key == ord('R'):
        thumbs_up_count = 0
        thumbs_down_count = 0
        vote_state = "neutral"
        print("\n*** COUNTS RESET ***\n")

cap.release()
cv2.destroyAllWindows()
