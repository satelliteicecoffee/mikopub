'''
mikopub.instrument.example_instrument
An example instrument class template for mikopub
'''

from typing import Literal

from pyvisa.constants import StopBits, Parity

from mikopub.utils import log
from mikopub._res._visa_instrument import _visa_instrument


class example_instrument(_visa_instrument):
    def __init__(self):
        super(example_instrument, self).__init__()
        self.instrName = "Example_Instrument"
        # serial config
        self.comPort = 0
        self.baudrate = 38400
        self.bytesize = 8
        self.parity = Parity.none
        self.stopbits = StopBits.one
        # IO config
        self.write_termination = "\r"
        self.read_termination = "\r"
        self.timeout = 1200
        # set logger
        self.loglogger = log.setLogLogger()
        pass

    def switchRemote(self, toStatus: Literal["on", "off"]) -> None:
        '''
        **Request to start/end terminal mode
        **toStatus: str = on, off
        **return: none
        '''
        if toStatus.lower() == "on":
            # self.write("SWITCH,1")
            # You may remove the following logging part once you have the real command
            self.loglogger.info(f"[{self.instrName}]: switch remote control on")
        elif toStatus.lower() == "off":
            # self.write("SWITCH,0")
            # You may remove the following logging part once you have the real command
            self.loglogger.info(f"[{self.instrName}]: switch remote control off")
        else:
            raise RuntimeError(f"[{self.instrName}]: input status incorrect")
        pass

    def exampleFunc1(self, x: int) -> int:
        '''
        **Example function 1, return double the x value
        **x: int
        **return: int
        '''
        if not isinstance(x, int):
            raise RuntimeError(f"[{self.instrName}]: input x type incorrect")
        y = x * 2
        return y

    def exampleFunc2(self) -> None:
        '''
        **Example function 2, a function that only pops a message
        **None
        **None
        '''
        self.loglogger.info(f"[{self.instrName}]: example function 2 executed")
        pass

    def terminateInstr(self) -> None:
        '''
        **Terminate device, turn off output
        **None
        **None
        '''
        self.switchRemote(toStatus="off")
        self._termInfo()
        pass

    pass


if __name__ == '__main__':
    '''
    Example debugging procedures
    '''
    vg = example_instrument()
    vg.connectSerial(comPort=6)
    # vg.connectUDP(udpIP="192.168.1.11", udpPort=8000)

    vg.switchRemote(toStatus="on")

    vg.switchRemote(toStatus="off")
    vg.instr.close()
    pass

pass
