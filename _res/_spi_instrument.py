import os
import datetime

import spidev

from mikopub.utils import log
from mikopub.utils import calc


class _spi_instrument(calc._Calc, object):
    def __init__(self, logFile=os.path.abspath(__file__).replace(r"\instrument", r"\log").replace(".py", ".log")):
        calc._Calc.__init__(self, logFile=logFile)
        # instrument name
        self.instrName = "_SPI_Default"
        # spi config
        self.max_speed_hz = 1000000
        self.mode = 0b00
        # set logger
        self.logFile = logFile
        self.loglogger = log.setLogLogger(logFile=self.logFile, logName=self.instrName + " " + str(datetime.datetime.now()))
        pass

    def connectSpi(
            self,
            bus,
            dev,
            max_speed_hz: int | None = None,
            mode: str | None = None
            ) -> None:
        if max_speed_hz is not None:
            self.max_speed_hz = max_speed_hz
        if mode is not None:
            self.mode = mode
        try:
            self.loglogger.info(f"[{self.instrName}]: SPI connect bus:".ljust(48)+f"{bus} dev:{dev}")
            self.instr = spidev.SpiDev()
            self.instr.open(bus, dev)
            self.instr.max_speed_hz = self.max_speed_hz
            self.instr.mode = self.mode
            self.connectType = "SPI"
            self.loglogger.info(f"[{self.instrName}]: SPI connection OK")
        except BaseException as e:
            raise RuntimeError(f"[{self.instrName}]: SPI connection fail \n{e}")
        pass

    def read(self, readRegister: list) -> list:
        try:
            read = self.instr.xfer2(tuple(readRegister))
        except BaseException as e:
            raise RuntimeError(f"[{self.instrName}]: Read error \n{e}")
        self.loglogger.info(f"[{self.instrName}]: Read:".ljust(48)+f"{tuple(readRegister)}")
        self.loglogger.info(f"[{self.instrName}]: Return:".ljust(48)+f"{read}")
        return read

    def write(self, writeRegister: list) -> None:
        try:
            self.instr.xfer2(tuple(writeRegister))
        except BaseException as e:
            raise RuntimeError(f"[{self.instrName}]: Write error \n{e}")
        self.loglogger.info(f"[{self.instrName}]: Write:".ljust(48)+f"{tuple(writeRegister)}")
        pass

    def _termInfo(self) -> None:  # log device termination info
        self.loglogger.info(f"[{self.instrName}]: Terminated")
        pass

    pass


if __name__ == "__main__":

    print(0b1000111100001011)
    print([0b10001111, 0b00001011])

    reg_ch0 = (
            0b1 << 15 |   # single shot coversion
            0b000 << 12 | # ch0
            0b111 << 9 |  # FSR 0.256 V
            0b1 << 8 |    # single shot mode
            0b000 << 5 |  # 8 SPS
            0b0 << 4 |    # ADC mode
            0b1 << 3 |    # pullup enabled on DOUT
            0b01 << 1 |   # valid data
            0b1           # reserved
            )
    reg_ch1 = (
            0b1 << 15 |   # single shot coversion
            0b011 << 12 | # ch1
            0b111 << 9 |  # FSR 0.256 V
            0b1 << 8 |    # single shot mode
            0b000 << 5 |  # 8 SPS
            0b0 << 4 |    # ADC mode
            0b1 << 3 |    # pullup enabled on DOUT
            0b01 << 1 |   # valid data
            0b1           # reserved
            )
    reg_tem = (
            0b1 << 15 |   # single shot coversion
            0b000 << 12 | #
            0b111 << 9 |  # FSR 0.256 V
            0b1 << 8 |    # single shot mode
            0b000 << 5 |  # 8 SPS
            0b1 << 4 |    # Internal temperature mode
            0b1 << 3 |    # pullup enabled on DOUT
            0b01 << 1 |   # valid data
            0b1           # reserved
            )

    spi = _spi_instrument()
    spi.connectSpi(bus=0, dev=0)
    readreg0 = spi._reg2list(reg_ch0)
    readreg1 = spi._reg2list(reg_ch1)
    readregtem = spi._reg2list(reg_tem)
    ddd = spi._list2int(readreg0)
    spi.read(readreg0)
    spi.read(readreg1)
    spi.read(readregtem)
    pass


pass
