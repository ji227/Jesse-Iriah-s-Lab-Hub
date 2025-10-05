import sys
import time
from datetime import date

import pyaudio
import speech_recognition as sr
from gtts import gTTS
from io import BytesIO

import digitalio
import busio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_vcnl4040
import adafruit_rgb_display.st7789 as st7789
from ollama import Client

# --- CONFIGURATION ---
# Note: Ensure Ollama is running and the model is pulled ('ollama pull phi3')
LLM_MODEL = 'phi3'
OLLAMA_HOST = 'http://127.0.0.1:11434' # Default Ollama Host
LLM_WOTD_PROMPT = "Provide a single word of the day, its spelling, definition, and a brief example. Format this strictly as: WORD|SPELLING|DEFINITION|EXAMPLE"

cs_pin = digitalio.DigitalInOut(board.D5) 
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None
BAUDRATE = 64000000
spi = board.SPI()

# --- INITIALIZATION ---
# Sensor setup
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_vcnl4040.VCNL4040(i2c, address=0x60)
PROXIMITY_THRESHOLD = 200

# Mini PiTFT Display setup
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

# Date/time setup
last_delivery_date = None
current_word = None
word_given = False

# Color and text setup
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
except IOError:
    font = ImageFont.load_default()
  
COLOR_READY_GREEN       = (0, 255, 0)
COLOR_DETECTED_RED      = (255, 0, 0)
COLOR_PROCESSING_YELLOW = (255, 255, 0)

# Olama setup
try:
    ollama_client = Client(host=OLLAMA_HOST)
    # Check if a model exists by listing them 
    ollama_client.list() 
except Exception as e:
    print(f"FATAL ERROR: Could not connect to Ollama at {OLLAMA_HOST}. Is the service running? Details: {e}")
    sys.exit(1)

# PyAudio setup
p = pyaudio.PyAudio()
MIC_DEVICE_INDEX = 0 

def speak(text, source="THE WORDBOT"):
    """Converts text to speech and plays it."""
    print(f"{source}: {text}")
    try:
        # Generate speech
        mp3_fp = BytesIO()
        tts = gTTS(text, lang='en')
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        
    except Exception as e:
        # gTTS or playback failed, just print the error and continue
        # print(f"TTS Error: {e}") 
        pass

def listen_for_keyword(keyword="yes", timeout=15):
    """Uses the microphone to listen for a keyword."""

    r = sr.Recognizer()
    
    print(f"(Listening for response... {timeout}s timeout)")
    
    # Use the SpeechRecognition's built-in Microphone class
    with sr.Microphone(device_index=MIC_DEVICE_INDEX) as source:
        r.adjust_for_ambient_noise(source)
        
        try:
            print("Say 'yes' now...")
            audio = r.listen(source, timeout=timeout)
            
            # This requires internet connectivity (Google Speech API)
            transcript = r.recognize_google(audio)
            
            print(f"User heard: {transcript}")
            
            if keyword in transcript.lower():
                return keyword
            
        except sr.WaitTimeoutError:
            print("Timeout reached: No speech detected.")
            return None
        except Exception as e:
            # Handles sr.UnknownValueError, sr.RequestError, etc.
            print(f"Mic Error/No speech: {e}")
            return None
    
    return None

def get_word_details():
    """Gets the WOTD details from Ollama and parses the structured response."""
    today_str = date.today().strftime("%B %d, %Y")  # Format like "October 05, 2025"
    prompt = f"Provide a single word of the day for {today_str}, its spelling, definition, and a brief example. Format this strictly as: WORD|SPELLING|DEFINITION|EXAMPLE"
    
    speak("Accessing the Archives of the Day. Please stand by.")
    set_status_screen(COLOR_PROCESSING_YELLOW, "PROCESSING: LLM", sensor.proximity)OCESSING: LLM", sensor.proximity) 
    
    time.sleep(1)
    try:
        response = ollama_client.generate(
            model=LLM_MODEL, 
            prompt=prompt,  # Use dynamic prompt with today's date 
            system="You are a linguistic archivist. Output *only* the requested pipe-separated data and nothing else."
        )
        
        raw_text = response['response'].strip()

        
        # Clean up any headers/prefixes and replace newlines with a separator if needed
        clean_text = raw_text.replace('\n', '|').replace('\r', '|')
        clean_text = clean_text.replace('WORD|', '').replace('Word|', '')
        
        # Split the text into parts and remove whitespace
        parts = [p.strip() for p in clean_text.split('|') if p.strip()]
        
        # Take the last 4 parts only.
        if len(parts) >= 4:
            data_parts = parts[-4:]
        else:
            data_parts = parts

        if len(data_parts) == 4:
            # Clean up the word part from any unexpected conversational lead-in
            word_part = data_parts[0].split(' ')[-1].upper() # Take only the last word
            
            return {
                'word': word_part,
                'spelling': data_parts[1].strip().replace('-', ' - ').upper(),
                'definition': data_parts[2].strip(),
                'example': data_parts[3].strip()
            }
        
        speak("I had trouble parsing the word data. Please try again later.", "SYSTEM ERROR")
        print(f"DEBUG: Failed to parse. Final parts: {data_parts}")
        return None
        
    except Exception as e:
        speak(f"Ollama connection error: {e}", "SYSTEM ERROR")
        print(f"DEBUG: Exception: {e}")
        return None

def give_etymology(word):
    """Prompts Ollama for the word's etymology."""
    # Set screen to YELLOW (Processing)
    set_status_screen(COLOR_PROCESSING_YELLOW, "PROCESSING: LLM", sensor.proximity) 

    speak("Consulting the Etymological Vault...")
    
    etymology_prompt = f"Provide the etymology and historical context for the word '{word}' in three to five sentences."
    try:
        response = ollama_client.generate(model=LLM_MODEL, prompt=etymology_prompt, system="You are an etymologist. Be concise and authoritative.")
        speak(response['response'].strip())
    except Exception as e:
        speak("I could not access the Etymological Vault.", "SYSTEM ERROR")

def set_status_screen(color_rgb, label, proximity_value):
    """Updates the screen with color and status text, including sensor reading."""
    # Ensure background is cleared
    draw.rectangle((0, 0, width, height), outline=0, fill=color_rgb)
    
    # Text for Status
    draw.text((10, 10), label, font=font, fill=(0, 0, 0)) 
    
    # Text for Proximity Value (for live feedback)
    prox_text = f"Prox: {proximity_value}"
    draw.text((10, 40), prox_text, font=font, fill=(0, 0, 0))

    disp.image(image, rotation)

# --- MAIN WORD BOT LOOP (The State Machine) ---

def main_loop():
    """The main state machine for the WordBot, triggered by proximity."""
    global last_delivery_date, current_word, word_given 
    
    # Initialize state
    speak("WordBot Initialized. Entering Deep Sleep State. Waiting for proximity.")

    while True:
        today = date.today()
        
        if last_delivery_date != today:
            # New day, fetch new word
            word_data = get_word_details()
            if word_data:
                current_word = word_data
                last_delivery_date = today
                word_given = False
            else:
                current_word = None
                word_given = False
        else:
            # Same day, reuse current_word
            pass
      
        try:
            # 1. DEEP SLEEP / INITIAL WAIT STATE: Wait for proximity detection
            if current_word is None and not word_given:
                
                proximity_value = sensor.proximity 
                
                # Set screen to GREEN (Idle/Ready)
                set_status_screen(COLOR_READY_GREEN, "READY: Deep Sleep", proximity_value) 
                
                if proximity_value > PROXIMITY_THRESHOLD:
                    speak(f"Proximity detected ({proximity_value})! Starting WOTD process.")
                    current_word = "AWAITING_YES" # Move to the Listening state
                    time.sleep(1.0) # Pause to avoid immediate re-trigger
                    continue 

                time.sleep(0.1)

            # 2. LISTENING STATE (AWAITING_YES): Ask for 'yes' if proximity was just detected
            if current_word == "AWAITING_YES":
                speak("Hello! Would you like today's word? (Say 'yes')")
                
                # Set screen to RED (Listening)
                set_status_screen(COLOR_DETECTED_RED, "LISTENING: Say 'Yes'", sensor.proximity) 
                
                trigger = listen_for_keyword("yes", timeout=15)
                
                if trigger == "yes":
                    # Note: get_word_details() will handle setting the screen to YELLOW (Processing)
                    word_data = get_word_details() 
                    if word_data:
                        current_word = word_data
                        word_given = True  
                    else:
                        current_word = None # LLM failed, go back to sleep
                else:
                    speak("No request received. Returning to Deep Sleep.")
                    current_word = None # Timeout/No response, go back to sleep
                    
            # 3. WORD DELIVERY STATE: Speak the word and ask for etymology (runs only once)
            if isinstance(current_word, dict) and word_given:
                word = current_word['word']
                
                # Set screen to GREEN for the delivery phase
                set_status_screen(COLOR_READY_GREEN, "SPEAKING", sensor.proximity) 

                # Deliver all the information ONCE
                speak(f"Today's word is {word.upper()}.") # THIS IS THE WORD
                speak(f"That is: {current_word['spelling']}.") # THIS IS THE SPELLING
                speak(f"The definition is: {current_word['definition']}.") # THIS IS THE DEFINITION
                speak(f"For instance: {current_word['example']}.") # THIS IS THE EXAMPLE
                
                speak("Would you like to hear about its origin? (Say 'yes')")
                
                # Set screen to RED again for follow-up listening
                set_status_screen(COLOR_DETECTED_RED, "LISTENING: Etymology", sensor.proximity) 
                follow_up = listen_for_keyword("yes", timeout=15)
                
                if follow_up == "yes":
                    # The give_etymology function will set the screen to YELLOW (Processing)
                    give_etymology(word)
                
                # Finished delivery. Set the flag to False so this entire block does not repeat.
                word_given = False  
                    
            # 4. POST-DELIVERY STATE: Word was given, now waiting for reset
            if isinstance(current_word, dict) and not word_given:
                
                proximity_value = sensor.proximity
                # The screen is set back to GREEN, but the label is updated to show completion
                set_status_screen(COLOR_READY_GREEN, "DONE: Wait/Reset", proximity_value) 
                
                speak("Word given. Move away and return to get a new word.", "PROMPT")
                
                # Wait for a reset trigger (proximity)
                if proximity_value > PROXIMITY_THRESHOLD:
                    speak("Reset trigger detected. Preparing a new Word of the Day.")
                    current_word = None  
                    word_given = False  
                    time.sleep(1.0)  
                    
                time.sleep(0.1)

        except KeyboardInterrupt:
            speak("Goodbye!")
            # Clear screen and turn off backlight
            draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
            disp.image(image, rotation)
            backlight.value = False
            break
        except Exception as e:
            speak(f"An unexpected error occurred: {e}", "SYSTEM ERROR")
            time.sleep(5)
            current_word = None  
            word_given = False
            
if __name__ == "__main__":
    main_loop() 
