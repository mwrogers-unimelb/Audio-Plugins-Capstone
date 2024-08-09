## UNTESTED!!! TAKEN DIRECTLY FROM CHATGPT ##

# Starter code to interface Raspberry Pi with ADC chips
# required libraries:
# sudo apt-get install python3-spidev
# pip3 install RPi.GPIO

import spidev
import time
import RPi.GPIO as GPIO

# GPIO setup for Chip Select (CS) pins
CS1_PIN = 22  # GPIO pin for CS of the first MCP3208
CS2_PIN = 27  # GPIO pin for CS of the second MCP3208

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(CS1_PIN, GPIO.OUT)
GPIO.setup(CS2_PIN, GPIO.OUT)

# Initialize SPI
spi = spidev.SpiDev()

def setup_spi(bus=0, device=0):
    spi.open(bus, device)
    spi.max_speed_hz = 1000000  # 1 MHz
    spi.mode = 0b00  # SPI mode 0

def read_adc(cs_pin, channel):
    """Read from the specified ADC channel."""
    if channel < 0 or channel > 7:
        raise ValueError("Channel must be between 0 and 7")

    # Start bit, single/diff bit, and channel selection bits
    start_bit = 0b1
    single_ended = 0b1
    command = (start_bit << 2) | (single_ended << 1) | (channel >> 2)
    high_byte = (channel & 0x03) << 6
    low_byte = 0x0

    GPIO.output(cs_pin, GPIO.LOW)  # Activate the MCP3208
    response = spi.xfer2([command, high_byte, low_byte])
    GPIO.output(cs_pin, GPIO.HIGH)  # Deactivate the MCP3208

    # The response will be a 12-bit value across two bytes
    result = ((response[1] & 0x0F) << 8) | response[2]
    return result

def read_all_channels():
    """Read all channels from both MCP3208 devices."""
    adc_values_1 = []
    adc_values_2 = []

    for channel in range(8):
        adc_values_1.append(read_adc(CS1_PIN, channel))
        adc_values_2.append(read_adc(CS2_PIN, channel))

    return adc_values_1, adc_values_2

def main():
    setup_spi()

    try:
        while True:
            adc_values_1, adc_values_2 = read_all_channels()
            print(f"ADC 1 Values: {adc_values_1}")
            print(f"ADC 2 Values: {adc_values_2}")
            time.sleep(1)

    except KeyboardInterrupt:
        print("Program stopped by User")
    finally:
        spi.close()
        GPIO.cleanup()

if __name__ == "__main__":
    main()