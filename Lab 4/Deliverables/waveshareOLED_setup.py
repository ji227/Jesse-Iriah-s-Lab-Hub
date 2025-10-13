"""
Simple Raspberry Pi OLED display script for Waveshare 2.23" OLED HAT (128x32 pixels).

Key info for development:
- Display resolution: 128 (width) × 32 (height) pixels.
- Picel size: Approximately 0.41mm × 0.39mm per pixel
- Interface: SPI by default
- Display color: Monochrome (white pixels on black background)
- Uses Adafruit CircuitPython SSD1305_SPI driver.
- Draw graphics and text with Pillow (PIL) on 1-bit images.
- Initialize display with SPI pins: CS=GPIO17, DC=GPIO24, RESET=GPIO25.
- Use disp.image(image) and disp.show() to update the display.
- Font size 10 fits about 4 lines of text vertically.
- Flip or rotate the image with Pillow if needed (e.g., image.rotate(180)).

Dependencies to install in your Python environment (virtualenv recommended):
  pip install adafruit-circuitpython-ssd1305 adafruit-blinka pillow

You may need to run this also if running outside a venv:
  sudo apt-get install libopenjp2-7 libopenjp2-7-dev libjpeg-dev
"""


import time
import subprocess
import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
from adafruit_ssd1305 import SSD1305_SPI

# Pin setup
spi = board.SPI()
cs_pin = digitalio.DigitalInOut(board.D17)
dc_pin = digitalio.DigitalInOut(board.D24)
reset_pin = digitalio.DigitalInOut(board.D25)

# Initialize display
disp = SSD1305_SPI(128, 32, spi, dc_pin, reset_pin, cs_pin)
disp.fill(0)
disp.show()

# Font for small text (fits 4 lines on 32px height)
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)
width = disp.width
height = disp.height

# Helper function to get system info lines
def get_sys_info_lines():
    IP = "IP: " + subprocess.check_output("hostname -I | cut -d' ' -f1", shell=True).decode().strip()
    try:
        Network = "Net: " + subprocess.check_output("iwgetid -r", shell=True).decode().strip()
    except subprocess.CalledProcessError:
        Network = "Net: Error"
    MAC = "MAC: " + subprocess.check_output("cat /sys/class/net/wlan0/address", shell=True).decode().strip()
    CPU = subprocess.check_output("top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'", shell=True).decode()
    Mem = subprocess.check_output("free -m | awk 'NR==2{printf \"Mem: %s/%s MB  %.1f%%\", $3,$2,$3*100/$2}'", shell=True).decode()
    Disk = subprocess.check_output('df -h | awk \'$NF=="/"{printf "Disk: %d/%d GB  %s", $3,$2,$5}\'', shell=True).decode()
    Temp_raw = subprocess.check_output("cat /sys/class/thermal/thermal_zone0/temp", shell=True).decode().strip()
    Temp = f"CPU Temp: {int(Temp_raw)/1000:.1f} C"

    return [
        [IP, Network, MAC],
        [CPU, Mem, Disk, Temp]
    ]

def draw_screen(lines):
    image = Image.new("1", (width, height))
    draw = ImageDraw.Draw(image)
    y = 0
    for line in lines:
        draw.text((0, y), line, font=font, fill=255)
        y += 12  # line height
    disp.image(image)
    disp.show()

def main():
    while True:
        sys_info = get_sys_info_lines()
        # Show page 1
        draw_screen(sys_info[0])
        time.sleep(5)
        # Show page 2
        draw_screen(sys_info[1])
        time.sleep(5)

if __name__ == "__main__":
    main()
