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
