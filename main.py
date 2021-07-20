# Python script to server dashboard data for DELTA Inverters
# written and (c) 2021 by Andreas Hopfenblatt

import json
import socket

from pymodbus.version import version
from pymodbus.server.asynchronous import StartTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.transaction import ModbusRtuFramer, ModbusAsciiFramer
import asyncio
import os
import logging
import time
import threading
import sunspec.sunspeclib
import sunspec.delta_data_structure
from http.server import BaseHTTPRequestHandler, HTTPServer
import websockets
import random


# define constants
HTTP_HOST_IP = socket.gethostbyname_ex(socket.gethostname())[-1][0]               # retreive the host name

HTTP_PORT = int(os.getenv('PORT', 8080))    # http port the dashboard will bind to
RS485_PORT = '/dev/ttyUSB0'                      # USB device of the RS-485 adapter (inverter)
RS485_READ_INTERVAL = 1                     # read values every second
UNIT = 0x00                                 # unit ID of the Sunspec slave, default

# --------------------------------------------------------------------------- #
# Logging
# --------------------------------------------------------------------------- #
FORMAT = ('%(asctime)-15s %(threadName)-15s'
          ' %(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.DEBUG)             # set to .INFO for production


#
# Class that handles reading data from the DELTA Inverter
#
class RS485ReaderClass(threading.Thread, sunspec.delta_data_structure.DeltaDataStructure):
    new_data = False  # true if new data is available
    timestamp = None  # timestamp of last data update

    def __init__(self, rs485_port):
        threading.Thread.__init__(self)  # call parent constructor
        self.rs485port = rs485_port
        print('Delta Inverter Data Reader Server started. Polling data via RS-485!')
        time.sleep(1)

    # private methode reading data from the inverter
    def __readdata(self):
        pass

    # private method updating the data
    def __update(self):
        self.data['Phase1_Output_Voltage'] = float(random.randrange(2250, 2450, 1)/10)
        self.data['Phase1_Output_Current'] = float(random.randrange(10, 320, 1)/10)
        self.data['Phase1_Output_Frequency'] = float(round(random.random() * 50, 2))
        self.data['Phase2_Output_Voltage'] = float(random.randrange(2200, 2460, 1)/10)
        self.data['Phase2_Output_Current'] = float(random.randrange(1, 32, 1))
        self.data['Phase2_Output_Frequency'] = float(round(random.random() * 50, 2))
        self.data['Phase3_Output_Voltage'] = float(random.randrange(2250, 2450, 1)/10)
        self.data['Phase3_Output_Current'] = float(random.randrange(1, 32, 1))
        self.data['Phase3_Output_Frequency'] = float(round(random.random() * 50, 2))
        self.new_data = True
        self.timestamp = time.time()

    def run(self):
        while True:
            self.__update()                     # read values via RS485
            time.sleep(RS485_READ_INTERVAL)     # wait N seconds until next read

    # public method that returns the data as a JSON-Object
    def asJSON(self):
        self.new_data = False
        return json.dumps(self.data)


#
# RequestHandler for our WebServer that serves just one static
# file (index.html)
#
class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            filename = os.getcwd() + '/html/index.html'
            self.send_response_only(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open(filename, 'rb') as htmlfile:
                html = htmlfile.read()
                self.wfile.write(html)
                print('Served index.html to the browser')


#
# Class as for a simple webserver to serve the static webpage
# for the dashboard
#
class WebServerClass(threading.Thread):

    def __init__(self, host, port):
        threading.Thread.__init__(self)  # call parent constructor
        self.host = host
        self.port = port
        print('HTTP Server started. Please open http:' + '//' + self.host + ':' + str(self.port) + ' in your browser.')
        time.sleep(1)

    def run(self):
        server_class = HTTPServer
        httpd = server_class(('0.0.0.0', self.port), RequestHandler)
        httpd.serve_forever()


#
# Class to provide as WebSocket service that streams new data
# from the inverter to the dashboard web page
#
class WS(threading.Thread):

    def __init__(self, deltadata):
        threading.Thread.__init__(self)  # call parent constructor
        self.connected = set()
        self.data = deltadata
        print('WebSocket-Server v' + str(websockets.__version__) + ' started!')
        time.sleep(1)

    def run(self):
        while True:
            data = self.data.asJSON()
            if data:
                self.pushData(data)     # push data via websocket to client (browser)
                time.sleep(0.5)         # wait half second before pushing new data

    def pushData(self, data):
        for websocket in self.connected.copy():         # loop through all registered clients
            response = websocket.send(data)
            asyncio.run_coroutine_threadsafe(response, ws_loop)

    async def handler(self, websocket, path):
        self.connected.add(websocket)                   # register client connection
        try:
            await websocket.recv()                      # receive incoming message
        except websockets.ConnectionClosed:
            print('Client closed the connection, can not push data!')
        finally:
            self.connected.remove(websocket)            # remove client connection if done


#
# Class to provide a ModBus server that serves the data from the
# Delta Inverter via ModBusTCP to other clients
#
class ModBusServer(threading.Thread):

    def __init__(self, deltadata):
        threading.Thread.__init__(self)  # call parent constructor
        self.data = deltadata

        # ModBus slave context
        self.store = ModbusSlaveContext(
            di=ModbusSequentialDataBlock(0, [17]*100),
            co=ModbusSequentialDataBlock(0, [17]*100),
            hr=ModbusSequentialDataBlock(0, [17]*100),
            ir=ModbusSequentialDataBlock(0, [17]*100)
        )

        self.context = ModbusServerContext(slaves=self.store, single=True)

        # ModBus server identification
        self.identity = ModbusDeviceIdentification()
        self.identity.VendorName = 'DeltaModBus'
        self.identity.ProductCode = 'DMB'
        self.identity.VendorUrl = 'https://hopfenblatt.com'
        self.identity.ProductName = 'DELTA Inverter Modbus Server'
        self.identity.ModelName = 'Modbus Server'
        self.identity.MajorMinorRevision = version.short()

    def update(self, a):
        log.debug('updating modbus values')
        context = a[0]
        register = 3
        slave_id = 0x00
        address = 0x10
        values = context[slave_id].getValues(register, address, count=5)
        values = [v + 1 for v in values]
        log.debug('new values: ' + str(values))
        context[slave_id].setValues(register, address, values)

    def run(self):
        # start TCP ModBus-Server
        StartTcpServer(self.context, identity=self.identity, address=("", 5020))


#
# ------------------------------------------------------------------
# main
# ------------------------------------------------------------------
#
# create objects from classes
inverterdata = RS485ReaderClass(RS485_PORT)
webpage = WebServerClass(HTTP_HOST_IP, HTTP_PORT)
websock = WS(inverterdata)
modbus = ModBusServer(inverterdata)

# start threads and websockets server
try:
    inverterdata.start()    # start the data polling thread
    webpage.start()         # start the webserver thread
    websock.start()         # start the websocket pusher thread
    modbus.start()          # start the modbus server

    ws_server = websockets.serve(websock.handler, HTTP_HOST_IP, 8000)
    ws_loop = asyncio.get_event_loop()
    ws_loop.run_until_complete(ws_server)
    ws_loop.run_forever()

except KeyboardInterrupt:
    stopFlag = True
    print('Exiting program...')
