import time
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
import busio
import adafruit_vcnl4040 # The Proximity Sensor Library

# --- HARDWARE CONFIGURATION ---
cs_pin = digitalio.DigitalInOut(board.D5) 
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None
BAUDRATE = 64000000
spi = board.SPI()

# Initialize the Mini PiTFT Display
disp = st7789.ST7789(spi, cs=cs_pin, dc=dc_pin, rst=reset_pin, baudrate=BAUDRATE,
                     width=135, height=240, x_offset=53, y_offset=40)
height = disp.width 
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90
draw = ImageDraw.Draw(image)
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

# Load font
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
except IOError:
    font = ImageFont.load_default()

# --- SENSOR INITIALIZATION ---
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_vcnl4040.VCNL4040(i2c, address=0x60)
print("VCNL4040 Sensor and Mini PiTFT Initialized.")

# --- COLOR & TEXT FUNCTIONS ---
COLOR_READY_GREEN       = (0, 255, 0)
COLOR_DETECTED_RED      = (255, 0, 0)
COLOR_PROCESSING_YELLOW = (255, 255, 0)
PROXIMITY_THRESHOLD = 200

def set_status_screen(color_rgb, label, proximity_value):
    """Updates the screen with color and status text, including sensor reading."""
    draw.rectangle((0, 0, width, height), outline=0, fill=color_rgb)
    
    # Text for Status
    draw.text((10, 10), label, font=font, fill=(0, 0, 0)) 
    
    # Text for Proximity Value (for live feedback)
    prox_text = f"Prox: {proximity_value}"
    draw.text((10, 40), prox_text, font=font, fill=(0, 0, 0))

    disp.image(image, rotation)


# --- MAIN TEST LOOP ---
try:
    print("Screen is GREEN (Idle). Move hand close to sensor to see RED.")
    while True:
        proximity_value = sensor.proximity
        
        if proximity_value > PROXIMITY_THRESHOLD:
            # Proximity Detected: Show RED
            set_status_screen(COLOR_DETECTED_RED, "RED: DETECTED!", proximity_value)
        else:
            # Idle State: Show GREEN
            set_status_screen(COLOR_READY_GREEN, "GREEN: READY", proximity_value)
            
        time.sleep(0.1) # Small delay for CPU break

except KeyboardInterrupt:
    print("\nTest stopped by user.")
except Exception as e:
    print(f"\nAn unexpected error occurred: {e}")
finally:
    print("Clearing screen and exiting.")
    draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
    disp.image(image, rotation)
    backlight.value = False
