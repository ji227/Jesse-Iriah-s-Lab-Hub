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

#### Phase 1: Breadboard Prototype (Nov 10-17)

Initial testing focused on validating sensor inputs and LED control independently before integration.

**Arduino LED Testing:**

![Arduino LED Test](Assets/media/build/arduino_led_test.png)
*NeoPixel ring successfully controlled via Arduino Uno - all 24 LEDs responding to serial RGB commands*

![Arduino Wiring](Assets/media/build/arduino_wiring.png)
*Wiring configuration: NeoPixel Data → Pin 6, Power → 5V, Ground → GND*

**Key Learnings:**
- NeoPixel requires 5V logic level (Arduino) rather than 3.3V (Pi GPIO)
- Serial communication at 9600 baud provides sufficient refresh rate (~30 FPS)
- RGB values must be clamped to 0-255 range to prevent overflow errors

**Raspberry Pi Serial Communication:**

![Pi Serial Test](Assets/media/build/pi_serial_test.png)
*Python script successfully sending RGB commands to Arduino via USB serial*

![Pi Terminal Output](Assets/media/build/pi_serial_terminal.png)
*Real-time serial monitor showing bidirectional communication and command acknowledgment*

**Architecture Decision:**
We chose a **Pi + Arduino hybrid architecture** rather than Pi-only control because:
1. Arduino handles time-critical LED refresh without OS interruptions
2. Pi focuses on compute-heavy tasks (speech recognition, audio FFT, web server)
3. Serial interface provides clean separation of concerns
4. Arduino can run standalone if Pi crashes (failsafe lighting)

#### Phase 2: Sensor Integration (Nov 17-24)

**MPR121 Capacitive Touch Sensor:**

The color mixer feature uses capacitive touch electrodes to let users "paint" RGB colors by tapping copper pads:
- **Lead 0:** Add red component (+1 drop)
- **Lead 1:** Add green component (+1 drop)
- **Lead 2:** Add blue component (+1 drop)
- **Lead 11:** Reset palette (clear all drops)
```python
# Color mixing algorithm from color_mixer.py
total_drops = red_drops + green_drops + blue_drops
if total_drops > 0:
    r_val = (red_drops / total_drops) * 255
    g_val = (green_drops / total_drops) * 255
    b_val = (blue_drops / total_drops) * 255
```

This "color drops" metaphor makes RGB mixing intuitive - users think in terms of paint mixing rather than abstract 0-255 values.

**Microphone Audio Analysis:**

![Microphone Test](Assets/media/build/mic_test.png)
*Speech recognition diagnostic tool confirming Google Speech API connectivity and ambient noise calibration*

Implemented two audio processing modes:
1. **Voice Commands:** Uses `SpeechRecognition` library with Google API for discrete trigger words
2. **Audio-Reactive:** Real-time FFT analysis maps volume → brightness, frequency → hue
```python
# Audio callback from mic_music.py
volume = np.linalg.norm(indata) * SENSITIVITY
target_speed = MIN_SPEED + volume  # Maps volume to rainbow rotation speed
rainbow_offset = (rainbow_offset + current_speed) % 255
```

**Challenge:** Initial attempts used Pi GPIO PWM for LEDs, but this caused flickering due to Linux scheduling interrupts. Solution: Offload LED control to Arduino's deterministic loop.

#### Phase 3: Enclosure Design (Nov 20-28)

**TinkerCAD Modeling:**

![TinkerCAD Design](Assets/media/build/scene_tinkerCAD.png)
*Parametric cube base (139.7mm sides) with centered 150mm (5.9 inch) sphere cutout for lamp diffuser*

Design requirements:
- Conceal all electronics (Pi, Arduino, breadboard, wiring)
- Front-facing microphone port for voice pickup
- Side-mounted USB-C power access
- Top cutout precisely sized for sphere friction-fit

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
- Sphere sourced from lighting supply store (standard 5.9" globe shade)

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
