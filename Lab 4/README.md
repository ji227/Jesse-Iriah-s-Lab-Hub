# Ph-UI!!!

**Collaborators:**  
Kyle Li.

---

## Lab Overview

This project explores physical user interfaces on the Raspberry Pi, focusing on sensor integration and prototyping new device forms. The goal is to use capacitive, light/proximity, gesture, rotary encoder, joystick, and distance sensors—then design the physical interaction and display for a new device.

---

## Part 1 Deliverables

### A. Capacitive Sensing

- **Setup:** Connected capacitive sensor to Pi using conductive materials from kit.
- **Test Video:**  
  [Capacitive Sensor Test](https://drive.google.com/drive/folders/1k5EjLj52QXkYCU0cCGVUmvABz0LI8WAS)  
  *This video shows the sensor hardware, Pi, and terminal output as clips are touched.*
- **Code:**  
  [cap_test.py](https://github.com/ji227/Jesse-Iriah-s-Lab-Hub/blob/Fall2025/Lab%204/cap_test.py)
- **Terminal Output:**  
  - Touching black alligator clip:  
    `Twizzler 0 touched!`
  - Touching white alligator clip:  
    `Twizzler 1 touched!`
  
---

### B. More Sensors

#### 1. Light/Proximity/Gesture Sensor (Adafruit APDS-9960)
- **Videos:**  
  - [Light Test](https://drive.google.com/file/d/1ynyXdRq7TfnPcbY4HaUFE6u_20OG_65H/view?usp=sharing)
  - [Proximity Test](https://drive.google.com/file/d/1AJwVIZ33KkiBfIbnyfk7PMNJ0pQdXZVZ/view?usp=sharing)
  - [Gesture Test](https://drive.google.com/file/d/1MKmHFrpkHARHvOo0EEXghPhEa9gxnTVY/view?usp=sharing)
- **Code:**  
  - [color_test.py](https://github.com/IRL-CT/Interactive-Lab-Hub/blob/Fall2025/Lab%204/color_test.py)
  - [proximity_test.py](https://github.com/IRL-CT/Interactive-Lab-Hub/blob/Fall2025/Lab%204/proximity_test.py)
  - [gesture_test.py](https://github.com/ji227/Jesse-Iriah-s-Lab-Hub/blob/Fall2025/Lab%204/gesture_test.py)
- **Terminal Output:**  
  - Color sensor output (~0.5s updates):
    ```
    red:  145
    green:  223
    blue:  124
    clear:  300
    color temp 5600
    light lux 290
    ```
  - Proximity sensor output (~0.2s updates):
    ```
    38
    40
    39
    ```
  - Gesture sensor output on detected gestures:
    ```
    up
    down
    left
    right
    ```

#### 2. Rotary Encoder
- **Video:**  
  [Rotary Encoder Test](https://drive.google.com/drive/folders/1k5EjLj52QXkYCU0cCGVUmvABz0LI8WAS)
- **Code:**  
  [encoder_test.py](https://github.com/ji227/Jesse-Iriah-s-Lab-Hub/blob/Fall2025/Lab%204/encoder_test.py)
- **Terminal Output:**
  	```
  	Found product 4991
	Position: 0
	Position: 1
	Position: 2
	Button pressed
	Button released
  	```

#### 3. Joystick
- **Video:**  
  [Joystick Test](https://drive.google.com/file/d/12tLrw4grtVd-AorB-V6PifySKMY9VJEA/view?usp=sharing)
- **Code:**  
  [joystick_test.py](https://github.com/IRL-CT/Interactive-Lab-Hub/blob/Fall2025/Lab%204/joystick_test.py)
- **Terminal Output:**  
	```
  	X: 507, Y: 524, Button: 1
	X: 750, Y: 300, Button: 1
	X: 512, Y: 512, Button: 0
 	```

#### 4. Distance Sensor
- **Video:**  
  [Distance Sensor Test](https://drive.google.com/file/d/1x9kApo4Re5UTOoBUEivQTzrcoP8KNI6Q/view?usp=sharing)
- **Code:**  
  [qwiic_distance.py](https://github.com/IRL-CT/Interactive-Lab-Hub/blob/Fall2025/Lab%204/qwiic_distance.py)
- **Terminal Output:**  
	```
  	SparkFun Proximity Sensor VCN4040 Example 1
	Proximity Value: 38
	Proximity Value: 40
	Proximity Value: 39
 	```

---

### C. Physical Sensing Design

- **Sketches:**  
	![Interactive Devices-23](https://github.com/user-attachments/assets/1b06e81c-b99a-4a97-9f11-be572ccb34b5)

- **Reflection - What are some things these sketches raise as questions? What do you need to physically prototype to understand how to anwer those questions?**  
  The five sketches explore various physical forms for the game controller interface: a classic Gameboy, a PSP-like handheld, an arcade machine, a laptop keyboard layout, and a video game controller. These different formats raise design questions related to ergonomics, button placement, user comfort, and control intuitiveness. For example, the portability of the Gameboy contrasts with the immersive feel of an arcade machine setup. The sketches also highlight challenges in balancing screen visibility, control accessibility, and housing size.
  Key questions for prototyping include how button size and spacing affect rapid jump/duck input, the dial placement’s ease of use for volume control, and how different device shapes accommodate sustained gameplay without fatigue.
  Physical prototypes are needed to test button spacing, size, and placement relative to hand reach and movement. Also, the dialing mechanism for volume control requires testing for tactile feedback and ease of adjustment.  

- **Prototype Selection:**    
  The Gameboy-inspired layout was selected for prototyping due to its compact size, ergonomic button placement, and familiarity, which promises a user-friendly interaction experience.

---

### D. Display & Housing

- **Sketches:**  
  *Placeholder for 5 display/button/knob positioning sketches.*

- **Reflection:**  
  *Short explanation about questions raised during sketching, and what needs to be prototyped to answer those questions.*

- **Integrated Design Selection:**  
  *Note which display/housing design will be used in your prototype and the rationale for selection (e.g. size, simple interface, visibility).*

- **Cardboard Prototype:**  
  *Include photos or video documenting your prototype. Paste link, image, or video embed here.*

---

## Structure for Part 2 

### E. Multi-Device Demo

- **Demo Code & Video:**  
  *To be added after completion.*

- **Interaction Diagram/Sketch:**  
  *To be added after completion.*

- **Reflection:**  
  *To be added after completion.*

---

### F. Final Documentation

- **Photos/Videos of Final Prototype:**  
  *To be added after completion.*

- **Summary & Reflection:**  
  *To be added after completion.*

---

## Additional Notes


---

ons or if you want an example of how to embed media using markdown tags!
