# Interactive Prototyping: The Clock of Pi

**Collaborators:**  
N/A.

---

## Project Overview

This project involves creating a simple clock on the Raspberry Pi using CLI and an RGB display, exploring novel ways to represent time and adding interactivity using the MiniPiTFT screen and buttons.

---

## Part A. Connect to Your Pi

- Connected via SSH to the Raspberry Pi.
- Created and activated Python virtual environment (`venv`) for development.
- Configured Git personal access tokens for secure pushing and pulling to/from GitHub.
![connectedPI](https://github.com/user-attachments/assets/e341a653-5c4b-44a0-b4dc-1f60dd5c9c5b)


---

## Part B. Try Out the Command Line Clock

- Cloned personal fork of Interactive-Lab-Hub repo onto the Pi.
- Installed all Python dependencies from `requirements.txt`.
- Ran `cli_clock.py` to display a terminal clock.
- Verified the time output, and exited cleanly with `Ctrl-C`.
<img width="517" height="140" alt="commandLineClock" src="https://github.com/user-attachments/assets/e5c36916-ffa6-4ced-b234-627e9ef2443b" />


---

## Part C. Set Up Your RGB Display

- Assembled and attached the MiniPiTFT to the Raspberry Pi 5.
- Disabled conflicting Piscreen service before running custom display scripts.
- Ran `screen_test.py` to test color display and button response.
- Explored example scripts:
  - `screen_boot_script.py` for text display.
  - `image.py` for showing images on the screen.
![whiteScreenTest](https://github.com/user-attachments/assets/3f4727c1-94d5-414a-9225-db0ffaacbcbe)


### Text Display Test Output
![textTest_hellojesse](https://github.com/user-attachments/assets/5f42812f-fb72-4daa-ad51-8daea44bfdb7)


---

## Part D. Set Up the Display Clock Demo

- Modified `screen_clock.py` to show current time on the MiniPiTFT by filling in the display update loop.
- Used code references from `cli_clock.py` and `stats.py`.
- Edited code on Pi via Nano editor, VNC with Thonny IDE, or VS Code remote for convenience.
![displayClockDemo_PI](https://github.com/user-attachments/assets/af143b16-efe2-4fab-944a-99cb2bbeed79)


---

## Part G. Sketch and Brainstorm Further Features for Part 2

- Planned features to add include:
  - Personalized greeting.
  - Display of date, weather, and location.
  - A user key or manual for clock functions.
- Incorporated peer feedback to focus on clarity and readability given the small screen size.
- Conceptualized dotted grid lines to improve time reading accuracy.

### Clock Mind Map

![Clock Mind Map](clockMindMap.jpg)

### Peer Feedback

- Received helpful suggestions from classmates Iqra and Kyle.
- Emphasized priority on clear, readable display of the current time.
- Recommended avoiding overcrowding the small screen with too many features.
- Suggested adding visual aids like dotted grid lines to ease reading.
- Feedback led to refining and focusing the design for usability and clarity.

---

## Part 2: Modified Barebones PiClock

- Implemented an interactive visual clock with graphical markers distinct from traditional digital or analog clocks.
- Added functionality to toggle display elements (graph key with title, axis, and markers) using MiniPiTFT buttons.
- Full code documented in `screen_clock.py`.

### Code Documentation PDF
[graphClockCode.pdf](https://github.com/user-attachments/files/22784258/graphClockCode.pdf)


### Clock Sketch Image
![myClockSketch](https://github.com/user-attachments/assets/c5f8d4cf-7b28-4eca-9984-67bdbe5c3b0e)


---

## Video Demonstration

- Recorded demonstration video of the modified PiClock interaction.

https://github.com/user-attachments/assets/95dab6c3-2320-4121-b357-19cc9854fde3



---

## Additional Notes

- Feedback helped prioritize feature clarity and effective use of interface space.
- Future work could include adding sensors or utilizing more interactive modalities.

---

