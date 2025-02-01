import re
import time

import pyvisa
from pyvisa.constants import StopBits, Parity

from mikopub.utils import calc
from mikopub.utils import log
from mikopub._res._visa_otherResources import OtherResourceManager


class _visa_instrument(calc._Calc, object):
    def __init__(self):
        calc._Calc.__init__(self)
        # instrument name
        self.instrName = "_VISA_Default"
        # usb config
        self.usbID = "USB::0x0000::0x0000::"
        # tcp/ip config
        self.tcpIP = "192.168.0.255"
        self.tcpPort = "8900"
        # udp/ip config
        self.udpIP = "192.168.0.255"
        self.udpPort = "8000"
        # serial config
        self.comPort = 0
        self.baudrate = 9600
        self.bytesize = 8
        self.parity = Parity.none
        self.stopbits = StopBits.one
        # IO config
        self.write_termination = "\n"
        self.read_termination = "\n"
        self.timeout = 2200
        # set logger
        self.loglogger = log.setLogLogger()
        pass

    def connectUSB(self, usbID: None | str = None) -> None:
        '''Connect instrument via usb'''
        rm = pyvisa.ResourceManager("@py")
        if usbID is not None:
            self.usbID = usbID
        for item in rm.list_resources():
            if re.search(self.usbID, item) and (len(self.usbID) > 0):
                self.loglogger.info(f"[{self.instrName}]: USB connect id:".ljust(48)+f"{self.usbID}")
                self.instr = rm.open_resource(item)
                break
        else:
            raise RuntimeError(f"[{self.instrName}]: USB connection not found")
        self.instr.write_termination = self.write_termination
        self.instr.read_termination = self.read_termination
        self.instr.timeout = self.timeout
        self.connectType = "USB"
        self.loglogger.info(f"[{self.instrName}]: USB connection OK")
        pass

    def connectSerial(
            self,
            comPort: str | int,
            baudrate: None | int = None,
            bytesize: None | int = None,
            parity: None | int = None,
            stopbits: None | int = None,
            ) -> None:
        '''Connect instrument via serial control'''
        rm = pyvisa.ResourceManager("@py")
        self.comPort = comPort
        if baudrate is not None:
            self.baudrate = baudrate
        if bytesize is not None:
            self.bytesize = bytesize
        if parity is not None:
            self.parity = parity
        if stopbits is not None:
            self.stopbits = stopbits
        for item in rm.list_resources():
            if re.search(f"ASRL{comPort}::INSTR", item):
                self.loglogger.info(f"[{self.instrName}]: Serial connect port:".ljust(48)+f"{self.comPort}")
                self.loglogger.info(f"[{self.instrName}]:                baudrate:".ljust(48)+f"{self.baudrate}")
                self.instr = rm.open_resource(f"ASRL{comPort}::INSTR")
                break
        else:
            raise RuntimeError(f"[{self.instrName}]: Serial connection not found")
        self.instr.baud_rate = self.baudrate
        self.instr.data_bits = self.bytesize
        self.instr.parity = self.parity
        self.instr.stop_bits = self.stopbits
        self.instr.write_termination = self.write_termination
        self.instr.read_termination = self.read_termination
        self.instr.timeout = self.timeout
        self.connectType = "Serial"
        self.loglogger.info(f"[{self.instrName}]: Serial connection OK")
        pass

    def connectTcp(self, tcpIP: str) -> None:
        rm = pyvisa.ResourceManager("@py")
        self.tcpIP = tcpIP
        try:
            self.loglogger.info(f"[{self.instrName}]: TCPIP connect ip:".ljust(48)+f"{self.tcpIP}")
            self.instr = rm.open_resource("TCPIP::"+tcpIP+"::INSTR")
        except BaseException as e:
            raise RuntimeError(f"[{self.instrName}]: TCPIP VXI11 connection fail \n{e}")
        self.instr.write_termination = self.write_termination
        self.instr.read_termination = self.read_termination
        self.instr.timeout = self.timeout
        self.connectType = "TCPIPVXI11"
        self.loglogger.info(f"[{self.instrName}]: TCPIP VXI11 connection OK")
        pass

    def connectTcpRaw(self, tcpIP: str, tcpPort: str | int) -> None:
        rm = pyvisa.ResourceManager("@py")
        self.tcpIP = tcpIP
        self.tcpPort = tcpPort
        try:
            self.loglogger.info(f"[{self.instrName}]: TCPIP connect ip:".ljust(48)+f"{self.tcpIP}")
            self.loglogger.info(f"[{self.instrName}]:               port:".ljust(48)+f"{self.tcpPort}")
            self.instr = rm.open_resource("TCPIP::"+tcpIP+"::"+str(tcpPort)+"::SOCKET")
        except BaseException as e:
            raise RuntimeError(f"[{self.instrName}]: TCPIP connection fail \n{e}")
        self.instr.write_termination = self.write_termination
        self.instr.read_termination = self.read_termination
        self.instr.timeout = self.timeout
        self.connectType = "TCPIPRaw"
        self.loglogger.info(f"[{self.instrName}]: TCPIP connection OK")
        pass

    def connectUDP(self, udpIP: str, udpPort: str | int) -> None:
        orm = OtherResourceManager()
        self.udpIP = udpIP
        self.udport = udpPort
        try:
            self.loglogger.info(f"[{self.instrName}]: UDP set socket ip:".ljust(48)+f"{self.udpIP}")
            self.loglogger.info(f"[{self.instrName}]:                port:".ljust(48)+f"{self.udpPort}")
            self.instr = orm.open_resource("UDPIP::"+udpIP+"::"+str(udpPort)+"::SOCKET")
        except BaseException as e:
            raise RuntimeError(f"[{self.instrName}]: UDP socket set fail \n{e}")
        self.instr.write_termination = self.write_termination
        self.instr.read_termination = self.read_termination
        self.instr.timeout = self.timeout
        self.connectType = "UDP"
        self.loglogger.info(f"[{self.instrName}]: UDP socket set OK")
        pass

    def query(self, cmd: str, wait=0, encoding="ascii") -> str:
        try:
            self.instr.write(cmd, encoding=encoding)
            time.sleep(wait)
            resp = self.instr.read(encoding=encoding).replace('\n', '').replace('\r', '')
        except BaseException as e:
            raise RuntimeError(f"[{self.instrName}]: Query error \n{e}")
        self.loglogger.info(f"[{self.instrName}]: Query ({encoding}):".ljust(48)+f"{cmd}")
        self.loglogger.info(f"[{self.instrName}]: Return ({encoding}):".ljust(48)+f"{resp}")
        return resp

    def queryBytes(self, cmd: bytes, wait=0) -> bytes:
        try:
            self.instr.write_raw(cmd)
            time.sleep(wait)
            resp = self.instr.read_raw()
        except BaseException as e:
            raise RuntimeError(f"[{self.instrName}]: Query error \n{e}")
        self.loglogger.info(f"[{self.instrName}]: Query bytes:".ljust(48)+f"{cmd}")
        self.loglogger.info(f"[{self.instrName}]: Return bytes:".ljust(48)+f"{resp}")
        return resp

    def write(self, cmd: str, encoding="ascii") -> None:
        try:
            self.instr.write(cmd, encoding=encoding)
        except BaseException as e:
            raise RuntimeError(f"[{self.instrName}]: Write error \n{e}")
        self.loglogger.info(f"[{self.instrName}]: Write ({encoding}):".ljust(48)+f"{cmd}")
        pass

    def writeBytes(self, cmd: bytes) -> None:
        try:
            self.instr.write_raw(cmd)
        except BaseException as e:
            raise RuntimeError(f"[{self.instrName}]: Write error \n{e}")
        self.loglogger.info(f"[{self.instrName}]: Write bytes:".ljust(48)+f"{cmd}")
        pass

    def read(self, encoding="ascii") -> str:
        try:
            resp = self.instr.read(encoding=encoding).replace('\n', '').replace('\r', '')
        except BaseException as e:
            raise RuntimeError(f"[{self.instrName}]: Read error \n{e}")
        self.loglogger.info(f"[{self.instrName}]: Read ({encoding}):".ljust(48)+f"{resp}")
        return resp

    def readBytes(self) -> bytes:
        try:
            resp = self.instr.read_raw()
        except BaseException as e:
            raise RuntimeError(f"[{self.instrName}]: Read error \n{e}")
        self.loglogger.info(f"[{self.instrName}]: Read bytes:".ljust(48)+f"{resp}")
        return resp

    def readBytesNum(self, bytenum=8) -> bytes:
        try:
            resp = self.instr.read_bytes(bytenum)
        except BaseException as e:
            raise RuntimeError(f"[{self.instrName}]: Read error \n{e}")
        self.loglogger.info(f"[{self.instrName}]: Read {bytenum} bytes:".ljust(48)+f"{resp}")
        return resp

    def _termError(self) -> None:
        self.instr.close()
        self.loglogger.error(f"[{self.instrName}]: Terminated on error")
        pass

    def terminateErrorInstr(self) -> None:
        '''
        **Terminate device on error for visa instrument placeholder
        **None
        **None
        '''
        # function to terminate device on error
        self._termError()
        pass

    def _termInfo(self) -> None:  # log device termination info
        self.instr.close()
        self.loglogger.info(f"[{self.instrName}]: Terminated")
        pass

    def terminateInstr(self) -> None:
        '''
        **Terminate device for visa instrument placeholder
        **None
        **None
        '''
        # function to terminate device normally
        self._termInfo()
        pass

    pass


pass
