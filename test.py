import json
import socket
import sys

import time
import pymodbus
import logging
from pymodbus.exceptions import ConnectionException
from pymodbus.version import version
from pymodbus.server.asynchronous import StartTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.diag_message import *
from pymodbus.file_message import *
from pymodbus.other_message import *
from pymodbus.mei_message import *
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian

UNIT = 0x1

FORMAT = ('%(asctime)-15s %(threadName)-15s '
          '%(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')

logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.DEBUG)

RS485_DEVICE = '/dev/ttyUSB0'
client = ModbusClient(method='rtu', port=RS485_DEVICE, timeout=1, baudrate=19200, stopbits=1, bytesize=8, parity='E',
                      strict=False)
client.connect()

# rr = client.read_holding_registers(40001, 1, unit=1)
for i in range(1000):
    read = client.read_holding_registers(i, unit=UNIT)

    if read.isError():
        print('Error from inverter')
        time.sleep(1)
        continue

    else:
        decoder = BinaryPayloadDecoder.fromRegisters(read.registers, byteorder=Endian.Big)
        result = decoder.decode_16bit_uint()

# close client connection
client.close()
