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

### Image of Setup Here

![Connected Pi](connectedPI.jpg)

---

## Part B. Try Out the Command Line Clock

- Cloned personal fork of Interactive-Lab-Hub repo onto the Pi.
- Installed all Python dependencies from `requirements.txt`.
- Ran `cli_clock.py` to display a terminal clock.
- Verified the time output, and exited cleanly with `Ctrl-C`.

### Command Line Clock Screenshot

![Command Line Clock](comandLineClock.png)

---

## Part C. Set Up Your RGB Display

- Assembled and attached the MiniPiTFT to the Raspberry Pi 5.
- Disabled conflicting Piscreen service before running custom display scripts.
- Ran `screen_test.py` to test color display and button response.
- Explored example scripts:
  - `screen_boot_script.py` for text display.
  - `image.py` for showing images on the screen.

### MiniPiTFT White Screen Test

![White Screen Test](whiteScreenTest.jpg)

### Text Display Test Output

![Text Test Hello Jesse](textTest_hellojesse.jpg)

### Image Display Test

![Image Test](image_test.jpg)

---

## Part D. Set Up the Display Clock Demo

- Modified `screen_clock.py` to show current time on the MiniPiTFT by filling in the display update loop.
- Used code references from `cli_clock.py` and `stats.py`.
- Edited code on Pi via Nano editor, VNC with Thonny IDE, or VS Code remote for convenience.

### Display Clock Demo on Pi

![Display Clock Demo](displayClockDemo_PI.jpg)

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

[Graph Clock Code (PDF)](graphClockCode.pdf)

### Clock Sketch Image

![My Clock Sketch](myClockSketch.jpg)

---

## Video Demonstration

- Recorded demonstration video of the modified PiClock interaction.

### Clock Demo Video

<video width="640" height="480" controls>
  <source src="graphClockDemo.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

---

## Additional Notes

- Feedback helped prioritize feature clarity and effective use of interface space.
- Future work could include adding sensors or utilizing more interactive modalities.

---

