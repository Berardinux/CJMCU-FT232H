locate libftdi1.so


python3 -m venv env
source env/bin/activate

deactivate

Example rule (/etc/udev/rules.d/99-ftdi.rules):
SUBSYSTEM=="usb", ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6014", MODE="0666"
sudo udevadm control --reload-rules
sudo udevadm trigger

