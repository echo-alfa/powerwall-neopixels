import time
import requests
import board
import neopixel

# Powerwall settings
powerwall_ip = 'POWERWALL IP ADDRESS' # Replace with te IP address of your Powerwall
username = 'EMAIL ADDRESS' # Replace with your Tesla Account Email Address
password = 'TESLA GATEWAY PASSWORD' # Replace with the last 5 digits of your Gateway Password

# LED settings
LED_COUNT = 10
LED_PIN = board.D18  # GPIO pin 18
LED_BRIGHTNESS = 0.5  # Range: 0.0 to 1.0

# Get the power output of the solar array
def get_solar_power(powerwall_ip):
    response = requests.get(f'http://{powerwall_ip}/api/meters/aggregates', auth=(username, password))
    return response.json()['solar']['instant_power']

# Get the number of LEDs to light up and their color based on the power output
def get_leds_and_color(power):
    num_leds = round((power / 6.8) * LED_COUNT)
    if power < 2.3:
        color = (255, 0, 0)  # Red
    elif power < 4.6:
        color = (255, 165, 0)  # Orange
    else:
        color = (0, 255, 0)  # Green
    return num_leds, color

def main():
    # Initialize the LED strip
    pixels = neopixel.NeoPixel(LED_PIN, LED_COUNT, brightness=LED_BRIGHTNESS)

    while True:
        power = get_solar_power(powerwall_ip)
        num_leds, color = get_leds_and_color(power)

        # Update LEDs
        for i in range(LED_COUNT):
            if i < num_leds:
                pixels[i] = color
            else:
                pixels[i] = (0, 0, 0)  # Off

        time.sleep(60)  # Update every minute

# Run the script
if __name__ == '__main__':
    main()
