import pyvisa
from pyvisa.constants import StopBits, Parity

# Load NI-VISA device USB ID
# Query *IDN? to all USB devices connected


def scanDevice():
    '''
    Scan NI-VISA usb devices and print device ID to console
    Query *IDN? to all possible devices and print return.
    Must have NI-VISA driver and pyvisa installed.
    '''
    rm = pyvisa.ResourceManager("@py")
    rml = rm.list_resources()

    return rml


if __name__ == "__main__":
    devs = scanDevice()
    print(devs)

pass
