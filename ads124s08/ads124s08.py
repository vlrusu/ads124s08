"""Main module."""

import spidev


ADS124S08_CMD_RREG               = 1
ADS124S08_CMD_WREG               = 2

ADS124S08_CMD_NOP = 0x0
ADS124S08_CMD_WAKEUP = 0x2
ADS124S08_CMD_POWERDOWN = 0x4
ADS124S08_CMD_RESET = 0x6
ADS124S08_CMD_START = 0x8
ADS124S08_CMD_STOP  = 0xA
ADS124S08_CMD_SYOCAL = 0x16
ADS124S08_CMD_SYGCAL = 0x17
ADS124S08_CMD_SFOCAL = 0x18
ADS124S08_CMD_RDATA = 0x12

ADS124S08_REG_ID = 0x0
ADS124S08_REG_STATUS = 0x1
ADS124S08_REG_INPMUX = 0x2
ADS124S08_REG_PGA = 0x3
ADS124S08_REG_DATARATE = 0x4
ADS124S08_REG_REF = 0x5
ADS124S08_REG_IDACMAG = 0x6
ADS124S08_REG_IDACMUX = 0x7
ADS124S08_REG_VBIAS = 0x8
ADS124S08_REG_SYS = 0x9
ADS124S08_REG_OFCAL0 = 0xA
ADS124S08_REG_OFCAL1 = 0xB
ADS124S08_REG_OFCAL2 = 0xC
ADS124S08_REG_FSCAL0 = 0xD
ADS124S08_REG_FSCAL1 = 0xE
ADS124S08_REG_FSCAL2 = 0xF
ADS124S08_REG_GPIODAT = 0x10
ADS124S08_REG_GPIOCON = 0x11

class ads124s08(object):

    def __init__(self, bus=0, cs = 0, max_speed_hz = 1000000):
        """Initialize an SPI device using the SPIdev interface.  Port and device
        identify the device, for example the device /dev/spidev1.0 would be port
        1 and device 0.
        """

        self.isInitialized = False
        self._bus = bus
        self._cs = cs
        self._max_speed_hz = max_speed_hz

    def open(self):

        if self.isInitialized:
            return

        self._spi = spidev.SpiDev()

        self._spi.open(self._bus, self._cs)
        self._spi.max_speed_hz=self._max_speed_hz
        self._spi.mode = 1
        self.isInitialized = True



    def _writereg(self, startaddress=0, val=0):

        firstbyte = (ADS124S08_CMD_WREG << 5) | startaddress
        secondbyte = len(val) - 1
        commandlist = [firstbyte,secondbyte] + val
#        print(" ".join(hex(x) for x in commandlist))
        self._spi.xfer2(commandlist)


    def _readreg(self, startaddress=0, nreg = 1):

        firstbyte = (ADS124S08_CMD_RREG << 5) | startaddress
        secondbyte = nreg - 1
        commandlist = [firstbyte,secondbyte] + nreg*[0]
#        print(" ".join(hex(x) for x in commandlist))        
        retval = self._spi.xfer2(commandlist)
#        print(" ".join(hex(x) for x in retval))        
        return retval[2:]

    def _command(self, command=[ADS124S08_CMD_NOP]):
#        print(" ".join(hex(x) for x in command))        
        self._spi.xfer2(command)

    def _readDeviceID(self):
        return self._readreg(ADS124S08_REG_ID,1)[0] & 0x7
    def _readStatus(self):
        return self._readreg(ADS124S08_REG_STATUS,1)[0]

    def _writeGain(self,gain = 1):
        self._writereg(ADS124S08_REG_PGA,gain,1)

    def _readGain(self):
        return self._readreg(ADS124S08_REG_PGA)[0]
    def _readIMUX(self):
        return self._readreg(ADS124S08_REG_INPMUX)[0]

    def _readInternalRef(self):
        return self._readreg(ADS124S08_REG_REF)[0]
    
    def _readData(self):
        commandlist = [ADS124S08_CMD_RDATA] + 4*[0]
#        print(" ".join(hex(x) for x in commandlist))        
        retval = self._spi.xfer2(commandlist)
#        print(" ".join(hex(x) for x in retval))        
        return retval[2:]
