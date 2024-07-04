from pyftdi.gpio import GpioAsyncController
import time

try:
    # Initialize GPIO controller
    gpio = GpioAsyncController()
    gpio.configure('ftdi:///1', direction=0x76)  # Example direction configuration

    # Example: Toggle output on BD1 (assuming BD1 is configured as output)
    while True:
        gpio.write(0x02)  # Set BD1 high
        time.sleep(1)
        gpio.write(0x00)  # Set BD1 low
        time.sleep(1)

except Exception as e:
    print(f"Error: {e}")

finally:
    if gpio:
        gpio.close()
