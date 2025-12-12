# SCENE: The Art of Ambiance

**Team Members:**  
Jesse Iriah, Iqra Khan

## Team Contributions
| Team Member | Contributions |
|-------------|---------------|
| **Jesse Iriah** | Hardware enclosure design (TinkerCAD modeling, 3D printing), hardware testing, software development, system integration, hardware assembly, user testing, documentation, video recording |
| **Iqra Khan** | Software architecture (Flask web app, Arduino communication, Spotify integration), voice control implementation, system integration, core feature development, user testing, documentation |

---

## Project Overview

SCENE is a smart ambient lighting and sound system that transforms any space through synchronized light and audio experiences. The device combines a spherical diffuser lamp with a modular control system, offering three interaction modes: Studio Mode for precise manual control via web interface, Voice Mode for hands-free activation using speech commands, and Party Mode for real-time audio-reactive lighting synchronized with music playback.

**Core Features:**
- Web-based timeline editor for creating custom lighting sequences
- Voice-activated scene triggering
- Real-time audio analysis with microphone-driven LED reactions
- Spotify integration with music-synced lighting effects
- Persistent scene storage with JSON configuration files

**Demo Videos:** [SCENE Videos - Project Folder](https://drive.google.com/drive/folders/12Zgj43E09HnoGVaSLpz_glJq2OIJacpn?usp=drive_link)

---

## Project Plan

### Ideation

Create an all-in-one ambient device that eliminates the need for multiple smart home products by combining customizable lighting, synchronized sound, and intelligent voice control into a single elegant form factor. SCENE addresses the fragmentation of modern smart home ecosystems where users need separate apps for lights (Philips Hue), speakers (Sonos), and voice assistants (Alexa) - instead offering a unified, programmable ambiance system.

**Target Use Cases:**
- **Morning routines:** Gradual sunrise simulation with nature sounds
- **Focus sessions:** Steady blue lighting with white noise or lofi music
- **Entertainment:** Music-reactive party lighting synced to Spotify playback
- **Relaxation:** Warm tones with rainfall or meditation audio
- **Voice convenience:** Hands-free scene activation while cooking, working, or winding down

### Initial Concept Sketch

![Initial Sketch](Assets/media/concept/scene_sketch.jpg)

*Early hardware concept showing sphere diffuser on cube base with integrated microphone and USB-C power*

### Storyboard Design

![Storyboard](Assets/media/concept/scene_storyboard.jpg)

*User interaction flow: (1) Setup & power on, (2) Create custom scene via UI, (3) Save and name scene, (4) Voice activation, (5) Device executes programmed sequence*

### Timeline

| Milestone | Target Date | Status |
|-----------|-------------|--------|
| Project plan submission | Nov 10 | Complete |
| Hardware prototyping (breadboard + sensors) | Nov 17 | Complete |
| Enclosure CAD design & 3D printing | Nov 24 | Complete |
| Core software features (web UI, serial comm) | Nov 24 | Complete |
| Voice control integration | Dec 1 | Complete |
| Spotify + audio-reactive mode | Dec 1 | Complete |
| Functional check-off | Dec 1 | Complete |
| User testing with 2+ participants | Dec 5 | Complete |
| Final documentation & video | Dec 8 | Complete |

### Parts & Components

**Electronics:**
- Raspberry Pi 4 (main controller)
- Arduino Uno (LED driver via serial)
- Adafruit NeoPixel Ring - 24 LEDs (RGB lighting)
- Adafruit MPR121 Capacitive Touch Sensor (color mixing input)
- USB Microphone (voice commands + audio analysis)
- USB-C Power Supply (5V, 3A)

**Physical Materials:**
- 3D printed cube enclosure (PLA, white)
- Spherical lamp diffuser (frosted acrylic, 6" diameter)
- Jumper wires, USB cables
- Mounting hardware (screws, standoffs)

**Software Dependencies:**
```
Flask (web server)
pyserial (Arduino communication)
adafruit-circuitpython-mpr121 (touch sensor)
SpeechRecognition (voice commands)
sounddevice + numpy (audio analysis)
spotipy (Spotify API integration)
```

### Fall-Back Plan

**If voice recognition fails:**
- Rely on web UI with saved scene library for quick access
- Add physical buttons for 3-5 preset scenes

**If Spotify integration fails:**
- Use local MP3 uploads with audio-reactive lighting
- Microphone-driven effects work independently of music source

**If 3D printing delays occur:**
- Use cardboard/foamcore prototype enclosure
- Focus on functional software demo with exposed hardware

**If audio analysis is too CPU-intensive:**
- Simplify algorithm to basic volume-based brightness control
- Pre-compute FFT at lower sample rates

---

## Design Process

### Hardware Evolution

#### Phase 1: Arduino LED Testing (Nov 10-14)

**Step 1: Standalone Arduino + NeoPixel**

Connected NeoPixel ring to Arduino Uno to verify basic LED control before adding Raspberry Pi complexity.

**Wiring Configuration:**
- Power → 5V
- Ground → GND  
- Data In → Digital Pin 6

![Arduino LED Setup](Assets/media/build/arduino_led_test.png)

*Initial breadboard setup with Arduino Uno controlling 24-LED NeoPixel ring*

![Arduino Wiring Detail](Assets/media/build/arduino_wiring.png)

*Diagram of NeoPixel connections - note 5V power requirement and Pin 6 data line*

**Testing Process:**
1. Installed Adafruit NeoPixel library in Arduino IDE
2. Uploaded `led_test.ino` sketch
3. Verified all 24 LEDs respond to color commands
4. Tested RGB color cycling (Red → Green → Blue → White → Off)

**Result:** LED ring works correctly with Arduino control


#### Phase 2: Raspberry Pi Serial Communication (Nov 14-17)


**Step 2: Pi ↔ Arduino Integration**

Connected Arduino to Raspberry Pi via USB cable to enable Python-based control.

![Pi + Arduino + LED Setup](Assets/media/build/arduino_pi_led_test.png)

*Complete system integration: Raspberry Pi connected to Arduino via USB, controlling NeoPixel ring through serial commands*

![Serial Terminal Output](Assets/media/build/pi_serial_test.png)

*Terminal showing successful RGB command transmission: Python script → Serial → Arduino → LEDs*

**Testing Script:**
Ran `led_control.py` on Pi to send color commands:
```python
# Format: "R,G,B\n" sent at 9600 baud
ser.write(b"255,0,0\n")  # Red
ser.write(b"0,255,0\n")  # Green
ser.write(b"0,0,255\n")  # Blue
```

**Architecture Decision:**
A **Pi + Arduino hybrid** rather than direct Pi GPIO control was chosen for the following reasons:
1. Arduino handles time-critical NeoPixel refresh without Linux OS interruptions
2. Pi focuses on compute-heavy tasks (speech recognition, FFT, web server)
3. Serial provides clean 9600 baud interface with ~30 FPS refresh rate
4. Arduino can run standalone if Pi crashes (failsafe mode)

**Result:** Serial communication working reliably


#### Phase 3: Sensor Integration (Nov 17-24)


**Step 3: Adding Microphone for Voice & Audio**

With the LED control pipeline validated, microphone input was added for voice commands and audio-reactive lighting.

**Microphone Configuration:**

Installing required audio libraries on Raspberry Pi:
```bash
# Core audio dependencies
sudo apt-get install -y libportaudio2 portaudio19-dev flac i2c-tools python3-dev

# Enable I2C for sensor communication
sudo raspi-config nonint do_i2c 0

# Python audio packages
pip install sparkfun-qwiic sounddevice numpy SpeechRecognition
```

**Library Troubleshooting:**
- `portaudio19-dev` → Fixed `AttributeError: Could not find PyAudio` crash
- `flac` → Fixed `OSError: FLAC conversion utility not available` crash  
- `python3-dev` → Ensures headers available for compiling `spidev`

**Microphone Feature Development:**

Implemented two distinct audio modes:
1. **Voice Commands:** Speech-activated scene triggering ("Deep Focus", "Wicked", etc.)
2. **Audio-Reactive (Party Mode):** Real-time volume/frequency analysis drives LED color/brightness based on music playback

#### Phase 4: Enclosure Design (Nov 20-28)

**TinkerCAD Modeling:**

![TinkerCAD Design](Assets/media/build/scene_tinkerCAD.png)

*Parametric cube base (139.7mm sides) with centered 100mm sphere cutout for lamp diffuser*

Design requirements:
- Conceal all electronics (Pi, Arduino, breadboard, wiring)
- Front-facing microphone port for voice pickup
- Side-mounted USB-C power access
- Top cutout precisely sized for sphere friction-fit
- Ventilation gaps for heat dissipation

**3D Model Visualization:**

![Autodesk Viewer](Assets/media/build/scene_autodeskViewer.png)

*Final CAD model rendered in Autodesk Viewer*

**Physical Build:**

![Final Device](Assets/media/build/scene_photo.png)


*Completed SCENE device - white PLA enclosure with frosted sphere diffuser, minimalist design inspired by modern smart home products*

**Manufacturing Notes:**
- Printed in white PLA at 0.2mm layer height
- Total print time: ~18 hours
- Post-processing: Light sanding on sphere contact surface for smooth fit
- Sphere sourced from lighting supply store (standard 6" globe shade)

### Software Architecture

**System Diagram:**
```mermaid
graph TD
    subgraph "User Interfaces"
        UI1[Web BrowserTimeline Editor]
        UI2[Voice CommandsSpeech Recognition]
        UI3[Touch Sensor PadsMPR121]
    end

    subgraph "Raspberry Pi 4 - Flask Server"
        SCENE[scene.pyWeb UI & API]
        VOICE[voice_listener.pySpeech Daemon]
        SPOTIFY[spotify_party.pyMusic + Audio FFT]
        MIXER[color_mixer.pyTouch Input Handler]
        HW[hardware.pySerial Controller]
    end

    subgraph "Arduino Uno - LED Driver"
        ARDUINO[Led_Control_arduino.inoNeoPixel Controller]
    end

    subgraph "Output"
        LED[24 NeoPixel LED Ring]
    end

    UI1 --> SCENE
    UI2 --> VOICE
    UI3 --> MIXER
    
    SCENE --> HW
    VOICE --> HW
    SPOTIFY --> HW
    MIXER --> HW
    
    HW -->|USB Serial9600 baud"R,G,B\n"| ARDUINO
    ARDUINO -->|Digital Pin 6| LED
```

**Key Software Components:**

| File | Purpose | Key Functions |
|------|---------|---------------|
| `scene.py` | Flask web server, main UI | Timeline editor, scene playback, Spotify search |
| `hardware.py` | Arduino serial communication | `send_color(r, g, b)`, `init_serial()` |
| `voice_listener.py` | Speech recognition daemon | Listens for "start [scene name]" commands |
| `spotify_party.py` | Music integration + audio FFT | `play_preview_with_analysis()`, `microphone_to_leds()` |
| `color_mixer.py` | Touch sensor color painting | Capacitive input → RGB calculation |
| `Led_Control_arduino.ino` | NeoPixel driver | Serial parser → `strip.setPixelColor()` |

**Data Flow Example (Voice Command):**
```
1. User says: "Hey Scene, start Focus Mode"
2. voice_listener.py captures audio via USB mic
3. Google Speech API returns text: "start focus mode"
4. POST request to Flask: /api/start-by-name/focus
5. scene.py loads saved_scenes.json, finds "Focus Mode"
6. Timeline engine interpolates brightness/hue curves
7. hardware.py sends serial commands: "0,150,255\n" (blue)
8. Arduino parses command, updates all 24 LEDs
9. Result: Device glows steady blue
```

---
