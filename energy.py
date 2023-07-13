import time
import requests
import board
import neopixel
import urllib3

# Powerwall settings
powerwall_ip = 'POWERWALL IP ADDRESS' # Replace with te IP address of your Powerwall
username = 'customer' # Required to always be 'customer'
username = 'EMAIL ADDRESS' # Replace with your Tesla Account Email Address
password = 'TESLA GATEWAY PASSWORD' # Replace with the last 5 digits of your Gateway Password

# LED settings
LED_COUNT = 30  # Total number of LEDs
LED_PIN = board.D18  # GPIO pin 18
LED_BRIGHTNESS = 0.5  # Range: 0.0 to 1.0

# Define sections for different meters
SOLAR_SECTION = range(0, 10)
BATTERY_SECTION = range(10, 20)
LOAD_SECTION = range(20, 30)

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Get the power output of the solar array
def get_solar_power(ip):
    login_url = f"https://{ip}/api/login/Basic"
    meter_url = f"https://{ip}/api/meters/aggregates"

    session = requests.Session()
    session.verify = False
    session.post(login_url, headers={'Content-Type': 'application/json'}, json={'username': username, 'email': email, 'password': password, 'force_sm_off': False})

    response = session.get(meter_url)
    power = response.json()['solar']['instant_power']
    print(f'Solar power output: {power / 1000:.2f} kW')  # Print the current solar power with 2 decimal places
    return power

# Same as get_solar_power but for load and battery
def get_load_power(ip):
    # same as in get_solar_power until...
    response = session.get(meter_url)
    power = response.json()['load']['instant_power']
    print(f'House load: {power / 1000:.2f} kW')  # Print the current house load with 2 decimal places
    return power

def get_charge_state(ip):
    # same as in get_solar_power until...
    response = session.get(meter_url)
    charge = response.json()['percentage']
    print(f'Powerwall charge: {charge:.2f}%')  # Print the current Powerwall charge with 2 decimal places
    return charge

# Get the number of LEDs to light up and their color based on the power output
def get_leds_and_color(power, max_power, color_scale):
    num_leds = round((power / max_power) * LED_COUNT / 3)
    color = color_scale[min(int(power / (max_power / 3)), 2)]
    return num_leds, color

def main():
    # Initialize the LED strip
    pixels = neopixel.NeoPixel(LED_PIN, LED_COUNT, brightness=LED_BRIGHTNESS, pixel_order=neopixel.GRB)

    # Define color scales for different meters
    solar_scale = [(0, 255, 0), (165, 255, 0), (255, 0, 0)]
    battery_scale = [(255, 0, 0), (165, 255, 0), (255, 0, 0)]
    load_scale = [(255, 0, 0), (165, 255, 0), (0, 255, 0)]

    while True:
        # Fetch data
        solar_power = get_solar_power(powerwall_ip)
        battery_charge = get_charge_state(powerwall_ip)
        load_power = get_load_power(powerwall_ip)

        # Calculate LEDs and colors
        solar_leds, solar_color = get_leds_and_color(solar_power, 6800, solar_scale)
        battery_leds, battery_color = get_leds_and_color(battery_charge, 100, battery_scale)
        load_leds, load_color = get_leds_and_color(load_power, 10000, load_scale)

        # Update LEDs
        for i in range(LED_COUNT):
            if i in SOLAR_SECTION and i - SOLAR_SECTION.start < solar_leds:
                pixels[i] = solar_color
            elif i in BATTERY_SECTION and i - BATTERY_SECTION.start < battery_leds:
                pixels[i] = battery_color
            elif i in LOAD_SECTION and i - LOAD_SECTION.start < load_leds:
                pixels[i] = load_color
            else:
                pixels[i] = (0, 0, 0)  # Off

        time.sleep(60)  # Update every minute

# Run the script
if __name__ == '__main__':
    main()
