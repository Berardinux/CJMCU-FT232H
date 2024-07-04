import time
import sys
from ctypes import *

# Constants
GPIO_DIRECTION_OUT = 0x01  # Output direction
GPIO_DIRECTION_IN = 0x00   # Input direction

# Define GPIO pins (adjust pin numbers based on your setup)
PIN_LED = 0  # Assuming AD0 corresponds to GPIO pin 0

# Load the libftdi1 library
try:
    if sys.platform.startswith('win32'):
        ftdi = cdll.ftdi1
    else:
        ftdi = cdll.LoadLibrary("/usr/lib/x86_64-linux-gnu/libftdi1.so.2")  # Adjust for your specific version
except OSError:
    print("Error loading libftdi1 library. Make sure it is installed and in the appropriate path.")
    sys.exit(1)

# Function to initialize FTDI device
def initialize_ftdi():
    context = ftdi.ftdi_new()

    if not context:
        print("Failed to initialize FTDI context.")
        return None

    if ftdi.ftdi_usb_open(context, 0x0403, 0x6014) < 0:
        print("Failed to open FTDI device.")
        ftdi.ftdi_free(context)
        return None

    ftdi.ftdi_write_data_set_chunksize(context, 4096)
    ftdi.ftdi_read_data_set_chunksize(context, 4096)

    if ftdi.ftdi_set_bitmode(context, 0xFF, GPIO_DIRECTION_OUT) < 0:
        print("Failed to set FTDI bitmode.")
        ftdi.ftdi_usb_close(context)
        ftdi.ftdi_free(context)
        return None

    return context

# Function to set GPIO pin state
def set_gpio(context, pin, state):
    mask = 1 << pin
    if state:
        ftdi.ftdi_write_data(context, bytes([mask]), 1)
    else:
        ftdi.ftdi_write_data(context, bytes([0]), 1)

# Main program loop
if __name__ == "__main__":
    # Initialize FTDI context
    context = initialize_ftdi()

    if context:
        try:
            while True:
                set_gpio(context, PIN_LED, True)  # Turn LED on (assuming AD0 is GPIO 0)
                time.sleep(1)
                set_gpio(context, PIN_LED, False)  # Turn LED off
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nExiting...")
        finally:
            ftdi.ftdi_usb_close(context)
            ftdi.ftdi_free(context)
    else:
        print("Failed to initialize FTDI context. Exiting...")
