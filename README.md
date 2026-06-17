
#  MediBot-Voice-Assistant (AI Doctor with Vision & Voice)

MediBot is an interactive multi-modal AI medical assistant application built with Python and Gradio. The system enables users to speak their symptoms via a microphone and upload an image (such as an X-ray, skin rash, or prescription) for evaluation. The AI processes these inputs and returns both a textual diagnostic response and an automated out-loud voice stream reading the doctor's prognosis natively on your computer.

It utilizes modern Large Language Models (LLMs) and Voice engines via **Groq LPU Acceleration Framework**, **Google Text-to-Speech (gTTS)**, and supports high-fidelity audio pipelines.

---

##  Key Features

* **Voice Transcription (STT):** Uses Groq's high-speed LPU framework executing the `whisper-large-v3` model to immediately transcribe patient audio queries.
* **Multi-Modal Diagnostics (Vision):** Leverages advanced flagship vision models (`meta-llama/llama-4-scout-17b-16e-instruct`) to review visual medical indicators alongside patient statements.
* **Autoplay Voice Pipeline (TTS):** Generates medical advice via Google Text-to-Speech (`gTTS`) or ElevenLabs.
* **Native Media Playback System:** Features a custom background cross-platform audio worker routing through Windows Native Media Subsystem (`wmplayer`) or macOS (`afplay`), eliminating caching and `.wav` alignment bugs.
* **State Caching Reset:** Explicitly isolates memory allocations per event submission to completely prevent old uploaded images from lingering on subsequent submissions.

---

##  Project Architecture

The application is modularized across specialized processing files to ensure maintainability:

1. **`gradio_app.py`**: The central application controller executing the reactive web server layout, managing input guardrails, and clearing cached memory frames dynamically.
2. **`brain_of_the_doctor.py`**: Handles on-the-spot base64 file binary encodings and communicates with Groq's multimodal vision endpoints.
3. **`voice_of_the_patient.py`**: Coordinates microphone capture frameworks and routes files through Groq's transcription subsystem.
4. **`voice_of_the_doctor.py`**: Manages the text-to-speech engines (gTTS/ElevenLabs) and houses the cross-platform command-line media players.

---
