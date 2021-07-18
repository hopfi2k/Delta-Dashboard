# Python script to server dashboard data for DELTA Inverters
# written and (c) 2021 by Andreas Hopfenblatt

import functools
import json
from pymodbus.constants import Endian
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.payload import BinaryPayloadDecoder
from twisted.internet.defer import Deferred
import os
import logging
import time
import threading
import sunspec.sunspeclib
from http.server import BaseHTTPRequestHandler, HTTPServer
import asyncio
import websockets
import random

# define constants
HTTP_HOST = os.getenv('HOST', '0.0.0.0')
HTTP_PORT = int(os.getenv('PORT', 8080))  # http port the dashboard will bind to
INVERTER_ADDR = '192.168.1.1'  # address of the inverter to collct data from
INVERTER_PORT = '3500'

# --------------------------------------------------------------------------- #
# Logging
# --------------------------------------------------------------------------- #
_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)
logging.basicConfig()


#
# Class that handles reading data from the DELTA Inverter
#
class DeltaDataClass(threading.Thread):
    data = {"Volt": 240, "Amps": 30, "Hz": 50.0}  # dictionary with the inverter data
    new_data = False  # true if new data is available
    timestamp = None  # timestamp of last data update

    def __init__(self, delta_ip, delta_port):
        threading.Thread.__init__(self)  # call parent constructor
        self.delta_ip = delta_ip
        self.delta_port = delta_port
        print('Delta Inverter Data Reader Server started. Polling data via RS-485!')
        time.sleep(1)

    # private methode reading data from the inverter
    def __readdata(self):
        pass

    # private method updating the data
    def __update(self):
        self.data['Volt'] = random.randrange(100, 250, 1)
        self.data['Amps'] = random.randrange(1, 32, 1)
        self.data['Hz'] = round(random.random() * 50, 2)
        self.new_data = True
        self.timestamp = time.time()

    def run(self):
        while True:
            self.__update()
            time.sleep(1)

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
class WebServer(threading.Thread):

    def __init__(self, host, port):
        threading.Thread.__init__(self)  # call parent constructor
        self.host = host
        self.port = port
        print('HTTP Server started! ' + 'http://' + self.host + ':' + str(self.port) + '/')
        time.sleep(1)

    def run(self):
        server_class = HTTPServer
        httpd = server_class((self.host, self.port), RequestHandler)
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
            asyncio.run_coroutine_threadsafe(response, loop)

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
        print('ModBus Server started!')
        time.sleep(1)


#
# ------------------------------------------------------------------
# main
# ------------------------------------------------------------------
#
# create objects from classes
inverterdata = DeltaDataClass(INVERTER_ADDR, INVERTER_PORT)
webpage = WebServer(HTTP_HOST, HTTP_PORT)
websock = WS(inverterdata)
modbus = ModBusServer(inverterdata)

# start threads and websockets server
try:
    inverterdata.start()    # start the data polling thread
    webpage.start()         # start the webserver thread
    websock.start()         # start the websocket pusher thread
    modbus.start()          # start the modbus server

    ws_server = websockets.serve(websock.handler, '0.0.0.0', 8000)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(ws_server)
    loop.run_forever()
except KeyboardInterrupt:
    stopFlag = True
    print('Exiting program...')
