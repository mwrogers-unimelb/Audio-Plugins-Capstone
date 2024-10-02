from gpiozero import LED
from time import sleep

# The onboard LED is typically connected to GPIO pin 47 (this may vary with models)
onboard_led = LED(17)
t = 0

try:
    while t < 10:
        # Turn the LED on
        print("LED on")
        onboard_led.on()
        sleep(1)  # Wait for 1 second

        # Turn the LED off
        print("LED off")
        onboard_led.off()
        sleep(1)  # Wait for 1 second
        t += 1

except KeyboardInterrupt:
    # Clean exit when user interrupts the program
    print("Exiting program")
finally:
    onboard_led.off()  # Ensure LED is turned off on exit