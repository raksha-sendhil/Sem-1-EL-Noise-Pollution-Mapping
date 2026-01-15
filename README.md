
# Noise Pollution Mapping System using Low Cost MEMS Microphones

## Semester 1 Experiential Learning Project

### Overview

This project aims to measure and map urban noise levels using embedded sensor nodes. It uses a digital MEMS mic (INMP441) connected to an ESP32-S3 microcontroller, which processes sound data and outputs calibrated decibel (dB SPL) values every second. These values are visualized using a Python-based GUI and plotted on a color-coded map using `folium`.

### Features

- Real-time dB level calculation with A-weighting
- Threshold-based alert system for noise violations
- Tkinter GUI for desktop display
- Folium-based static noise map visualization
- Designed for urban noise monitoring (e.g., campus, traffic zones)

### Hardware

- ESP32-S3 DevKitC-1
- INMP441 I2S Digital MEMS Microphone
- USB for power and serial communication

###  Software

- ESP-32 code for dB SPL calculation (based on [ikostoski](https://github.com/ikostoski/esp32-i2s-slm))
- Python (3.8+) for GUI and visualization
  - `pyserial`, `tkinter`, `folium`

### Getting Started

### 1. Flash ESP32
Connect ESP32 to USB. Upload the firmware from the file `decibel_calculation.ino`  using ArduinoIDE.

### 2. Run the GUI
Then run:
```bash
python displaying_dB.py
