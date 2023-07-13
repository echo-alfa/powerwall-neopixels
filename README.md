# Powerwall LED Status Indicator
This project is a Python application designed to interact with a Tesla Powerwall and provide real-time visual feedback about the power system's status using ws281x addressible LEDs or NeoPixels. The program communicates with the Powerwall over the local network and uses the returned data to illuminate different sections of the LED strip based on current solar power output, house load, and Powerwall charge level.

# Features
Real-time Powerwall status monitoring: The Python application continuously polls the Powerwall's local API to retrieve the latest data about solar power production, house power consumption, and the Powerwall's charge level.

NeoPixel LED indicators: The application controls NeoPixels connected to a Raspberry Pi and updates the illumination of different sections of the strip to reflect the current Powerwall status. Three sections of the strip are used to represent solar power output, house power consumption, and Powerwall charge level.

Color-coded feedback: The color of the LEDs in each section varies based on the intensity of each power source or load. This color-coded feedback helps the user quickly identify whether the power levels are within the expected ranges or wheather consumption is high or low.

# Requirements
Hardware: A Raspberry Pi (any model with GPIO pins), ws281x LED strip compatible with the NeoPixel library (with at least 30 LEDs), and a Tesla Powerwall (with local network connectivity).
Software: Python 3, the requests library for Python (to handle HTTP requests), the NeoPixel library for Python (to control the LED strip), and the Tesla Powerwall's local API (for retrieving power and charge data).
Limitations
Please note that this application relies on the local API of the Tesla Powerwall, which is officially undocumented by Tesla. Therefore, the functionality of the application could be affected by changes made by Tesla to the Powerwall software or local API.

This project is a fun and practical way to monitor your Tesla Powerwall status and visualize your home's power usage and solar power production in real-time. It's also a great starting point for building more complex home automation and monitoring systems based on the Powerwall and Raspberry Pi.
