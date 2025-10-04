# Chatterboxes: Speech-Enabled Conversational Device

**Collaborators:**  
N/A.

---

## Project Overview

This project involves designing interaction with a speech-enabled device that listens and talks, excluding control of lights (covered in a prior lab). The focus is on audio as the main interaction modality, using speech-to-text, text-to-speech, and AI-powered conversation to create engaging dialogues.

---

# Part 1. Setup & Technical Demos

This section covers coding tasks demonstrating proficiency with the core technologies.  

### Text-to-Speech Demo

- **Greeting Script:** [my_greeting.sh](https://github.com/ji227/Jesse-Iriah-s-Lab-Hub/blob/Fall2025/Lab%203/Deliverables/my_greeting.sh)  
- **Contents:** A shell script using a text-to-speech engine to output ""Greetings, Jesse Iriah. Welcome to Lab Three."  

### Speech-to-Text Demo

- **Numerical Input Script:** [numerical_input.sh](https://github.com/ji227/Jesse-Iriah-s-Lab-Hub/blob/Fall2025/Lab%203/Deliverables/numerical_input.sh)   
- **Contents:** A shell script that verbally requests a 5 digit zip code and records the user's response via STT.  

### AI-Powered Conversations with Ollama

- **Voice Assistant Documentation:** [OLLAMA Voice Assistant Documentation](https://docs.google.com/document/d/1MC8Soh6y-xnqsH4-R49oLbx3axFsuhnrAuuwzcrkruw/edit?tab=t.0)  
- **Contents:** Documentation outlining technical challenges like STT/TTS issues, Ollama latency, and voice clarity improvements.  
- **Ollama Voice Assistant Script:** [final_voice_assistant.py](https://github.com/ji227/Jesse-Iriah-s-Lab-Hub/blob/Fall2025/Lab%203/Deliverables/final_voice_assistant.py)

---

# Part 1. Design & Dialogue Elicitation

This section focuses on initial design and role-playing exercises.

### Storyboard & Initial Design

- **Design Documentation:** [Wordbot Documentation (Pt1)](https://docs.google.com/document/d/13Gwjj5X3j9nWW3U7r54Km0AkHF1IowsGNWMSfG7pEe8/edit?tab=t.0)  
- **Contents:** Complete (collated) documentation for the Wordbot project which includes design process, scripts, storyboard, peer review etc.    
- **Storyboard/Diagram:** [Storyboard Google Doc](https://github.com/ji227/Jesse-Iriah-s-Lab-Hub/blob/Fall2025/Lab%203/Deliverables/WordBot%20StoryBoard.jpg)

### Dialogue Script

- **Initial Script:** [WORDBOT Script](https://docs.google.com/document/d/1t9Ip9DpQih5_yKYYBYtNqrnhIPVMiVl7mqFzCLVfRVg/edit?tab=t.0)  
- **Process Description:** [Development Process](https://github.com/ji227/Jesse-Iriah-s-Lab-Hub/blob/Fall2025/Lab%203/Deliverables/Wordbot%20Design%3AProcess.png)

### Acting out the Dialogue

- **Dialogue Recording:** [Wordbot Dialogue.mp3](https://github.com/user-attachments/files/22690623/Wordbot.Dialogue.mp3)
- **Reflection/ Review:** [Wordbot Review/Reflection](https://github.com/ji227/Jesse-Iriah-s-Lab-Hub/blob/Fall2025/Lab%203/Deliverables/Wordbot%20Peer-Review.pdf)

### Wizarding with the Pi (Optional)

- (Include your notes or delete if not completed.)

---

# Lab 3 Part 2. Redesign and Testing

This section addresses the prototype redesign and testing phases.

### Prep for Part 2 (Redesign Rationale)

- **Improvements:** Break complex final responses into summaries with prompts for more detail.  
- **Other Interaction Modes:** Suggested blinking lights or color changes indicate processing vs listening states.  
- **New Storyboard/Script:** [Updated Storyboard/Script](link_to_updated_storyboard)

### Prototype your system

- **System Documentation:** [System Design Document](link_to_system_doc) detailing sensors used, component interactions (Pi, Ollama, STT/TTS).  
- **Video/Screencaptures:** [System Demo Videos](link_to_video_or_screencaps)

---

# Testing and Evaluation

### Webserver Functionality Screenshot

From a remote browser on the same network, the webserver was verified at:  
`http://<YourPiIPAddress>:5000` displaying "Hello World".

![Webserver Running Screenshot](relative/or/full/path/to/webserver_screenshot.png)

### Speech-to-Text Demo Video

Here is a demonstration video of the speech-to-text function, where the user asks:  
*“What’s the largest continent?”* and the system responds appropriately.

[![Speech-to-Text Demo](https://img.youtube.com/vi/YOUR_VIDEO_ID/0.jpg)](https://www.youtube.com/watch?v=YOUR_VIDEO_ID)

---

### What worked well about the system and what didn't?

***your answer here***

### What worked well about the controller and what didn't?

***your answer here***

### What lessons can you take away from the WoZ interactions for designing a more autonomous version of the system?

***your answer here***

### How could you use your system to create a dataset of interaction? What other sensing modalities would make sense to capture?

***your answer here***

---

# Sources

- List any references, tutorials, libraries, or resources used.

---

**Note:** Replace all placeholder links `link_to_...`, YouTube IDs, and file paths with your actual URLs, paths, and video IDs.

---

This README uses Markdown headings for clear sectioning, bullet points for concise info, embedded images and videos to show proof, and placeholders for your testing reflections and sources. It is ready for direct use or further customization. Let me know if you want me to generate this with your specific links included.
