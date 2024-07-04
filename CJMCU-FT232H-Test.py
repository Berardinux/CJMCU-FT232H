import time
import sys
from ctypes import *

# Constants
GPIO_DIRECTION_OUT = 0x01  # Output direction
GPIO_DIRECTION_IN = 0x00   # Input direction

# Define GPIO pins (adjust pin numbers based on your setup)
PIN_LED = 0  # Example: LED connected to GPIO 0

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
    # Initialize context
    context = ftdi.ftdi_new()

    if not context:
        print("Failed to initialize FTDI context.")
        return None

    # Open device
    if ftdi.ftdi_usb_open(context, 0x0403, 0x6014) < 0:
        print("Failed to open FTDI device.")
        ftdi.ftdi_free(context)
        return None

    # Set USB transfer sizes
    ftdi.ftdi_write_data_set_chunksize(context, 4096)
    ftdi.ftdi_read_data_set_chunksize(context, 4096)

    # Set bitmode (GPIO mode)
    if ftdi.ftdi_set_bitmode(context, 0xFF, GPIO_DIRECTION_OUT) < 0:
        print("Failed to set FTDI bitmode.")
        ftdi.ftdi_usb_close(context)
        ftdi.ftdi_free(context)
        return None

    return context

# Functio
