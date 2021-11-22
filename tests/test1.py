# from pathlib import Path
import sys
from time import sleep
# path_root = Path(__file__).parents[2]
# sys.path.append(str(path_root))
#print(sys.path)


from ads124s08.ads124s08 import ads124s08


a =  ads124s08.ads124s08(0,0)

a.open()

a._command([ads124s08.ADS124S08_CMD_NOP,ads124s08.ADS124S08_CMD_WAKEUP])
a._command([ads124s08.ADS124S08_CMD_NOP,ads124s08.ADS124S08_CMD_RESET])


#set registers disables PGA, internal oscillator, single shot, low latency (default) 20SPS (default) internal 2.5V ref
a._writereg(ads124s08.ADS124S08_REG_PGA,[0x08,0x34,0x0A])
#sys 8 samples(default) disable CRC at the end and enable STATUS in preamble (4 words in DATAREAD) 
a._writereg(ads124s08.ADS124S08_REG_SYS,[0x91]) #was 0x11 here
#AIN0 + and AINCOM -
#a._writereg(ads124s08.ADS124S08_REG_INPMUX,[0xC])

print("ID=", hex(a._readDeviceID()))
print("STATUS=",hex(a._readStatus()))
print("GAIN=",hex(a._readGain()))
print("INPMUX=",hex(a._readIMUX()))
print("REFERENCE=",hex(a._readInternalRef()))



sleep(0.3)
a._command([ads124s08.ADS124S08_CMD_START])

sleep(0.3)
v=a._readData()
print ("DATA="," ".join(hex(x) for x in v))
voltage = v[0]<<16 | v[1] <<8 | v[2]
print ("DATAVOLTAGE=",hex(voltage))


#MCP3426_FS = 2^24
MCP3426_REFV = 2.5
if voltage > 0x7FFFFF:
#    print("here",float(voltage-0x800000),2**23,float(voltage-0x800000)/float(2**23))
    voltage = -MCP3426_REFV + float(voltage - 0x800000)*MCP3426_REFV/float(2**23)
else:
    print("done")
    voltage = float(voltage)*MCP3426_REFV/(2**23)

print ("VOLTAGE=",voltage)

a._command([ads124s08.ADS124S08_CMD_STOP])

#set IDAC to 500uA
a._writereg(ads124s08.ADS124S08_REG_IDACMAG,[0x7])
#set IDAC1 to AIN0

channel = int(sys.argv[1])
reg = (0xF << 4) | channel
a._writereg(ads124s08.ADS124S08_REG_IDACMUX,[reg])
#set IMUXP+ to AIN0 and IMUXP- to AINCOM
reg = (channel << 4) | 0xC
a._writereg(ads124s08.ADS124S08_REG_INPMUX,[reg])
#sys 8 samples(default) disable CRC at the end and enable STATUS in preamble (4 words in DATAREAD) 
a._writereg(ads124s08.ADS124S08_REG_SYS,[0x11]) #was 0x11 here


print("ID=", hex(a._readDeviceID()))
print("STATUS=",hex(a._readStatus()))
print("GAIN=",hex(a._readGain()))
print("INPMUX=",hex(a._readIMUX()))
print("REFERENCE=",hex(a._readInternalRef()))

a._command([ads124s08.ADS124S08_CMD_START])
sleep(0.3)
v=a._readData()
print ("DATA="," ".join(hex(x) for x in v))
voltage = v[0]<<16 | v[1] <<8 | v[2]
print ("DATAVOLTAGE=",hex(voltage))


#MCP3426_FS = 2^24
MCP3426_REFV = 2.5
if voltage > 0x7FFFFF:
#    print("here",float(voltage-0x800000),2**23,float(voltage-0x800000)/float(2**23))
    voltage = -MCP3426_REFV + float(voltage - 0x800000)*MCP3426_REFV/float(2**23)
else:
    print("done")
    voltage = float(voltage)*MCP3426_REFV/(2**23)

print ("VOLTAGE=",voltage)
a._command([ads124s08.ADS124S08_CMD_STOP])

for i in range(0,11):
    reg = (i << 4) | 0xC
    a._writereg(ads124s08.ADS124S08_REG_INPMUX,[reg])
    #sys 8 samples(default) disable CRC at the end and enable STATUS in preamble (4 words in DATAREAD) 
    a._writereg(ads124s08.ADS124S08_REG_SYS,[0x11]) #was 0x11 here


    a._command([ads124s08.ADS124S08_CMD_START])
    sleep(0.3)
    v=a._readData()
#    print ("DATA="," ".join(hex(x) for x in v))
    voltage = v[0]<<16 | v[1] <<8 | v[2]
#    print ("DATAVOLTAGE=",hex(voltage))


#MCP3426_FS = 2^24
    MCP3426_REFV = 2.5
    if voltage > 0x7FFFFF:
        #    print("here",float(voltage-0x800000),2**23,float(voltage-0x800000)/float(2**23))
        voltage = -MCP3426_REFV + float(voltage - 0x800000)*MCP3426_REFV/float(2**23)
    else:
        voltage = float(voltage)*MCP3426_REFV/(2**23)

    print ("channel=",i,"VOLTAGE=",voltage)



    a._command([ads124s08.ADS124S08_CMD_STOP])
