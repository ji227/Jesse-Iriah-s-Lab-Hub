import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
from adafruit_rgb_display.rgb import color565
import colorsys
import calendar
import math

# Configuration for CS and DC pins (FeatherWing defaults on M0/M4)
cs_pin = digitalio.DigitalInOut(board.D5)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24MHz)
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI
spi = board.SPI()

# Create the ST7789 display
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

# Button setup
btnA = digitalio.DigitalInOut(board.D23)
btnB = digitalio.DigitalInOut(board.D24)

# Set buttons as inputs, with pull-up resistors
btnA.direction = digitalio.Direction.INPUT
btnB.direction = digitalio.Direction.INPUT
btnA.pull = digitalio.Pull.UP
btnB.pull = digitalio.Pull.UP

# Create blank image for drawing (rotate to landscape)
height = disp.width
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90
draw = ImageDraw.Draw(image)

# Clear screen
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)

# Fonts
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)
label_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 8)
key_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)

# Backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True


def draw_axes_clock():
    # Clear screen with white background
    draw.rectangle((0, 0, width, height), outline=0, fill=(255, 255, 255))

    # Padding and borders
    border_width = 2
    padding_left, padding_right, padding_top, padding_bottom = 25, 15, 15, 15

    draw.rectangle((0, 0, width - 1, height - 1),
                   outline=color565(255, 0, 0), width=border_width)

    # Plot area
    plot_left = padding_left
    plot_top = padding_top
    plot_right = width - padding_right
    plot_bottom = height - padding_bottom
    plotting_width = plot_right - plot_left
    plotting_height = plot_bottom - plot_top

    # Axis colours and thickness
    axis_color = color565(0, 0, 0)
    line_thickness = 1

    # Horizontal axis (minutes)
    draw.line((plot_left, plot_bottom, plot_right, plot_bottom),
              fill=axis_color, width=line_thickness)

    # Vertical axis (hours)
    draw.line((plot_left, plot_bottom, plot_left, plot_top),
              fill=axis_color, width=line_thickness)

    # Markers
    marker_size = 3
    text_offset = 2

    # Minute markers (every 15 minutes)
    for minute_val in range(0, 61, 15):
        x_pos = plot_left + int(minute_val / 60 * plotting_width)
        draw.line((x_pos, plot_bottom - marker_size, x_pos,
                   plot_bottom + marker_size), fill=axis_color, width=line_thickness)
        text_bbox = draw.textbbox((0, 0), str(minute_val), font=label_font)
        text_width = text_bbox[2] - text_bbox[0]
        if minute_val == 60:
            draw.text((x_pos - text_width, plot_bottom + text_offset),
                      str(minute_val), font=label_font, fill=axis_color)
        else:
            draw.text((x_pos - text_width / 2, plot_bottom + text_offset),
                      str(minute_val), font=label_font, fill=axis_color)

    # Hour markers (every 3 hours)
    for hour_val in range(0, 13, 3):
        y_pos = plot_bottom - int(hour_val / 12 * plotting_height)
        draw.line((plot_left - marker_size, y_pos,
                   plot_left + marker_size, y_pos),
                  fill=axis_color, width=line_thickness)

        if hour_val == 12:
            hour_label = "12"
        elif hour_val == 0:
            hour_label = "0"
        else:
            hour_label = str(hour_val)

        text_bbox = draw.textbbox((0, 0), hour_label, font=label_font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        draw.text((plot_left - marker_size - text_offset - text_width,
                   y_pos - text_height / 2),
                  hour_label, font=label_font, fill=axis_color)

    # Arrowheads
    arrow_size = 5
    # X-axis arrow
    draw.polygon([(plot_right, plot_bottom),
                  (plot_right - arrow_size, plot_bottom - arrow_size),
                  (plot_right - arrow_size, plot_bottom + arrow_size)],
                 fill=axis_color)
    # Y-axis arrow
    draw.polygon([(plot_left, plot_top),
                  (plot_left - arrow_size, plot_top + arrow_size),
                  (plot_left + arrow_size, plot_top + arrow_size)],
                 fill=axis_color)

    # Current time
    current_time = time.localtime()
    current_hour_24 = current_time.tm_hour
    current_minute = current_time.tm_min

    # Convert to 12-hour format
    hour_12 = current_hour_24 % 12
    if hour_12 == 0:
        hour_12 = 12

    # Map minutes to X and hours to Y
    x_plot = plot_left + int(current_minute / 59 * plotting_width)
    y_plot = plot_bottom - int((hour_12 - 1) / 11 * plotting_height)

    # Draw 'X'
    text_bbox = draw.textbbox((0, 0), 'X', font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    draw.text((x_plot - text_width / 2, y_plot - text_height / 2),
              'X', font=font, fill="#FF0000")


def draw_key_screen():
    draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
    title = "GRAPH CLOCK"
    key_text = "X = Time"
    hours_key = "Y-Axis = Hours"
    minutes_key = "X-Axis = Minutes"

    draw.text((width / 2 - 30, 20), title, font=key_font, fill="#FFFFFF")
    draw.text((width / 2 - 30, height / 2 - 20), key_text, font=key_font, fill="#FF0000")
    draw.text((width / 2 - 30, height / 2), hours_key, font=key_font, fill="#FFFFFF")
    draw.text((width / 2 - 30, height / 2 + 20), minutes_key, font=key_font, fill="#FFFFFF")

    disp.image(image, rotation)


while True:
    if not btnB.value:  # Button B pressed
        draw_key_screen()
    else:
        draw_axes_clock()

    disp.image(image, rotation)
    time.sleep(0.1)
