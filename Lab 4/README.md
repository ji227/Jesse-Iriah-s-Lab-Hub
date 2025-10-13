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
  The five sketches explore different physical forms inspired by classic 90s retro gaming devices and handheld consoles, focusing on a simple, recognizable style suitable for a 2D platformer game. The designs reflect iconic shapes such as a Gameboy, PSP, arcade machine, laptop keyboard layout, and a video game controller, each incorporating buttons and dials positioned for intuitive jump/duck and volume control interactions. These different formats raise design questions related to ergonomics, button placement, user comfort, and control intuitiveness. For example, the portability of the Gameboy contrasts with the immersive feel of an arcade machine setup. The sketches also highlight challenges in balancing screen visibility, control accessibility, and housing size.
  
  Key questions for prototyping include how button size and spacing affect rapid jump/duck input, the dial placement’s ease of use for volume control, and how different device shapes accommodate sustained gameplay without fatigue.
  
  Physical prototypes are needed to test button spacing, size, and placement relative to hand reach and movement. Also, the dialing mechanism for volume control requires testing for tactile feedback and ease of adjustment.   

- **Prototype Selection:**    
  The Gameboy-inspired layout was selected for prototyping due to its compact size, ergonomic button placement, and familiarity, which promises a user-friendly interaction experience.  

---

### D. Display & Housing

- **Sketches:**  
  *Placeholder for 5 display/button/knob positioning sketches.*
  ![Interactive Devices-23 2](https://github.com/user-attachments/assets/ca7dce17-5ad0-4295-b5bd-63cbbeaec3d7)
  - *Content:* Five layout designs were created for the Gameboy-style device, varying the physical positions of the OLED display, jump and duck buttons, and the rotary volume dial:

- **Reflection:**  
  *Short explanation about questions raised during sketching, and what needs to be prototyped to answer those questions.*
  These sketches raised design questions including:  
  - How does the positioning of buttons affect reachability and prevent accidental presses?
  - What button sizes best balance quick access and comfort?
  - Where should the rotary dial be placed for intuitive volume control without interfering with gameplay?
  - How visible is the display from natural holding angles during active use?
  - Does the form factor allow comfortable grip and sustained interaction without fatigue?  
  
  Physical cardboard prototypes are needed to test the ergonomics of button and dial placement, the comfort of the grip while holding the device, and display visibility at typical viewing angles. Prototyping will help answer tactile feedback and spacing challenges that sketches alone cannot resolve.  

- **Integrated Design Selection:**  
  *Note which display/housing design will be used in your prototype and the rationale for selection (e.g. size, simple interface, visibility).*  
  The Gameboy-inspired layout was initially selected for prototyping due to its compact size, ergonomic button placement, and familiarity.  The first layout—centered display with symmetrical buttons below and rotary dial on the top edge—was chosen. This design balances symmetry for easy ambidextrous use and places controls where thumbs naturally rest while holding the device. The size and positioning ensure the screen is clearly visible during play.  

- **Final Prototype:**  
  *Include photos or video documenting your prototype. Paste link, image, or video embed here.*
  The final design incorporates a **Waveshare 2.23-inch OLED Hat** and replaces the capacitive buttons with the **Rotary Encoder** and **Joystick** for a robust, dedicated control interface.
  - Component update & connectivity: The final configuration utilizes the **Waveshare 2.23-inch OLED Hat** (wide screen), which mounts directly onto the Raspberry Pi's **40 GPIO pins**. An **I2C SHIM** is physically sandwiched between the display and the Pi to provide accessible I2C connections for the external **Rotary Encoder** and **Joystick**. All three components (Display, Encoder, Joystick) communicate using the I2C protocol.
  - Component measurements (approximate):  
	<img src="https://github.com/ji227/Jesse-Iriah-s-Lab-Hub/blob/Fall2025/Lab%204/Deliverables/encoder_measurements.jpg?raw=true" width="250" alt="Rotary Encoder Measurements" />  
    <img src="https://github.com/ji227/Jesse-Iriah-s-Lab-Hub/blob/Fall2025/Lab%204/Deliverables/joystick_measurements.jpg?raw=true" width="250" alt="Joystick Measurements" />  
    <img src="https://github.com/ji227/Jesse-Iriah-s-Lab-Hub/blob/Fall2025/Lab%204/Deliverables/pi%2Bdisplay_measurements.jpg?raw=true" width="350" alt="Pi and OLED Assembly Measurements" />  

  - Final layout sketch:  
    - Description: *The sketch below shows the fixed physical arrangement of components: The **OLED Display** is centered at the top. The **Raspberry Pi** is mounted upside down to route the USB-C power cable out the top-right corner. The rotary encoder is on the bottom-left, and the joystick is on the bottom-right. The I2C SHIM's role as the connection point is highlighted.*
	![Interactive Devices-28](https://github.com/user-attachments/assets/0b0e5342-9a9e-4d17-8bef-cb3b0161a3cd)
	 <img src="https://github.com/ji227/Jesse-Iriah-s-Lab-Hub/blob/Fall2025/Lab%204/Deliverables/partD_prototypeSketch.jpg?raw=true" width="350" alt="Pi and OLED Assembly Measurements" />  
  - Cardboard prototype:
    
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
