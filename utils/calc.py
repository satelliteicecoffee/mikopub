import os
import struct
import datetime

from functools import reduce

from mikopub.utils import log


class _Calc(object):
    def __init__(self) -> None:
        self.instrName = "_CalcDefault"
        # set logger
        self.loglogger = log.setLogLogger()
        pass

    @classmethod
    def convertToFloat(cls, originData: tuple):
        '''
        **Convert read data to float
            originData: original tuple to be converted
        **{"originData": {"Property": {"Type": "tuple"}}}
        **float
        '''
        temp = []
        temp1 = []
        temp2 = [0] * len(originData) * 2
        if len(originData) % 2 != 0:
            return
        else:
            for item in originData:
                item = hex(item)
                # Note : hex will return a string, which will remove the high 0
                # for example 0x0061 will be 0x61, so we have to convert it back.
                if len(item) % 2 != 0:
                    length = len(item)
                    fill_zero = (6-length)
                    item = item.replace("0x", "0x"+"0"*fill_zero)
                temp.append(item)
            for item in temp:
                if item == "0x0":
                    item = "0x0000"
                item = str(item)
                item = item.replace("0x", '')
                temp1.append(item)
            for index in range(0, len(originData)):
                temp2[index * 2] = temp1[index][0:2]
                temp2[index * 2 + 1] = temp1[index][2:4]
            # temp2.reverse()
            data = "".join(temp2)
            float_value = int(data, base=16)
            if len(originData) <= 2:
                float_value = struct.pack('<I', float_value)
                float_value = struct.unpack('f', float_value)
            elif len(originData) == 4:
                float_value = struct.pack('<Q', float_value)
                float_value = struct.unpack('d', float_value)
            float_value = float_value[0]
            return float_value

    def _convertToFloat(self, _originData: tuple):
        _float_value = _Calc.convertToFloat(originData=_originData)
        self.loglogger.info(f"[{self.instrName}]: Convert {_originData} -> {_float_value}")
        return _float_value

    def _reg2list(self, reg):
        '''
        Convert register to list of 8 digits
        '''
        convert_list = [(reg >> 8) & 0xff, reg & 0xff]
        self.loglogger.info(f"[{self.instrName}]: Convert {reg} -> {convert_list}")
        return convert_list

    def _list2int(self, lst, seg_len=8):
        '''
        Convert a list to segments of input length
        '''
        convert_int = 0b00
        for i in lst:
            convert_int = (convert_int << seg_len) | i
        self.loglogger.info(f"[{self.instrName}]: Convert {lst} -> {convert_int}")
        return convert_int

    def _conv2scom(self, integer, bit_num=8):
        '''
        Convert a decimal integer into is 2's complement decimal integer
        '''
        if integer < 2 ** (bit_num-1):
            complement = integer
        else:
            complement = integer - 2 ** bit_num
        self.loglogger.info(f"[{self.instrName}]: Conv 2s {integer} -> {complement}")
        return complement

    def _str2hexbytes(self, string: str) -> bytes:
        '''
        **Convert string containing both /x bytes and int to /x format bytes
          no log required
        **string: str
        **return: bytes
        '''
        hexbytes = bytes.fromhex("".join(["{:02x}".format(ord(c)) for c in string]))
        return hexbytes

    def _xorChecksum(self, data: bytes, chunk_size=1) -> bytes:
        '''
        Calculate XOR checksum of input data bytes, return bytes
        '''
        if chunk_size <= 0:
            raise ValueError(f"[{self.instrName}]: Negative chunck size")
        chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
        xor_results = [reduce(lambda x, y: x ^ y, chunk + b'\x00' * (chunk_size - len(chunk))) for chunk in chunks]
        final_xor = reduce(lambda x, y: x ^ y, xor_results)
        return final_xor.to_bytes(chunk_size, "big")

    pass


pass
