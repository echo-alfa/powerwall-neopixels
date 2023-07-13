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
LED_COUNT = 10  # Number of LEDs per section
LED_PIN = board.D18  # GPIO pin 18
LED_BRIGHTNESS = 0.5  # Range: 0.0 to 1.0

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Get the powerwall data
def get_powerwall_data(ip):
    login_url = f"https://{ip}/api/login/Basic"
    meter_url = f"https://{ip}/api/meters/aggregates"
    soe_url = f"https://{ip}/api/system_status/soe"

    session = requests.Session()
    session.verify = False
    session.post(login_url, headers={'Content-Type': 'application/json'}, json={'username': username, 'email': email, 'password': password, 'force_sm_off': False})

    response = session.get(meter_url)
    solar_power = response.json()['solar']['instant_power']
    load_power = response.json()['load']['instant_power']
    response = session.get(soe_url)
    charge_percent = response.json()['percentage']

    print(f'Solar power output: {solar_power / 1000} kW')  # Print the current solar power
    print(f'House load: {load_power / 1000} kW')  # Print the current house load
    print(f'Powerwall charge: {charge_percent}%')  # Print the current Powerwall charge

    return solar_power, load_power, charge_percent

# Get the number of LEDs to light up and their color based on the power output
def get_leds_and_color(power, is_load=False):
    # Convert power to kilowatts
    power = power / 1000

    num_leds = round((power / (10 if is_load else 6.8)) * LED_COUNT)

    if is_load:
        if power > 5:
            color = (0, 255, 0)  # Red in GRB
        else:
            color = (255, 0, 0)  # Green in GRB
    else:
        if power < 2.5:
            color = (0, 255, 0)  # Red in GRB
        elif power < 5:
            color = (165, 255, 0)  # Orange in GRB
        else:
            color = (255, 0, 0)  # Green in GRB

    return num_leds, color

def main():
    # Initialize the LED strip
    pixels = neopixel.NeoPixel(LED_PIN, LED_COUNT * 3, brightness=LED_BRIGHTNESS, pixel_order=neopixel.GRB)

    while True:
        solar_power, load_power, charge_percent = get_powerwall_data(powerwall_ip)
        num_solar_leds, solar_color = get_leds_and_color(solar_power)
        num_load_leds, load_color = get_leds_and_color(load_power, True)
        num_charge_leds, charge_color = get_leds_and_color(charge_percent * 10)  # Convert percentage to a 0 to 10 scale

        # Update LEDs
        for i in range(LED_COUNT * 3):
            if i < num_solar_leds:
                pixels[i] = solar_color
            elif i < LED_COUNT + num_charge_leds:
                pixels[i] = charge_color
            elif i < LED_COUNT * 2 + num_load_leds:
                pixels[i] = load_color
            else:
                pixels[i] = (0, 0, 0)  # Off

        time.sleep(60)  # Update every minute

# Run the script
if __name__ == '__main__':
    main()
