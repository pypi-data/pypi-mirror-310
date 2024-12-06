''' Crow/AAP Alarm IP / Serial Module Base Connection'''
import asyncio
import datetime
import logging
import re
import threading
import time 
import serial_asyncio

from pycrowmodule import StatusState
from pycrowmodule.crow_defs import *

_LOGGER = logging.getLogger(__name__)

from asyncio import ensure_future

class CrowModuleClient(asyncio.Protocol):

    """Abstract base class for the Crow/AAP IP / Serial Module"""
    def __init__(self, panel, loop):
        self._connected = False
        self._alarmPanel = panel

        if loop is None:
            _LOGGER.info("Creating own event loop...")
            self._eventLoop = asyncio.new_event_loop()
            self._ownLoop = True
        else:
            _LOGGER.info("Latching onto existing event loop...")
            self._eventLoop = loop
            self._ownLoop = False

        self._transport = None
        self._shutdown = False
        self._cachedCode = None
        self._buffer = b''  

    def start(self):
        """Public method for initiating connectivity with the Module"""
        self._shutdown = False
        ensure_future(self.connect(), loop=self._eventLoop)
        ensure_future(self.keep_alive(), loop=self._eventLoop)

        if self._ownLoop:
            _LOGGER.info("Starting up our own event loop...")
            self._eventLoop.run_forever()
            self._eventLoop.close()
            _LOGGER.info("Connection shut down!")

    def stop(self):
        """Public method for shutting down connectivity with the Crow IP / Serial Module."""
        self._connected = False
        self._shutdown = True

        if self._ownLoop:
            _LOGGER.info("Shutting down Crow IP / Serial Module client connection...")
            self._eventLoop.call_soon_threadsafe(self._eventLoop.stop)
        else:
            _LOGGER.info("An event loop was given to us- we will shutdown when that event loop shuts down.")

    # async def connect(self):
    #     """Internal method for making the physical connection."""
    #     _LOGGER.info(str.format("Starting connection to Crow IP Module... at {0}:{1}", self._alarmPanel.host, self._alarmPanel.port))
    #     coro = self._eventLoop.create_connection(lambda: self, self._alarmPanel.host, self._alarmPanel.port)
    #     try:
    #         await asyncio.wait_for(coro, timeout=self._alarmPanel.connection_timeout)
    #         """Changed in version 3.7: When aw is cancelled due to a timeout, wait_for waits for aw to be cancelled. Previously, it raised asyncio.TimeoutError immediately."""
    #     except:
    #         _LOGGER.debug('Timeout connecting to Crow IP module...')
    #         self.handle_connect_failure()
    #     """        
    #     try:
    #         async with async_timeout.timeout(self._alarmPanel.connection_timeout, loop=self._eventLoop):
    #             coro = self._eventLoop.create_connection(lambda: self, self._alarmPanel.host, self._alarmPanel.port)
    #             await coro
    #     except:
    #         self.handle_connect_failure()
    #     """

    # CHANGES MADE TO ADD IP and SERIAL support
    
    async def connect(self):
        """Internal method for making the physical connection."""
        if self._alarmPanel.connection_type == 'ip':
            await self._connect_ip()
        elif self._alarmPanel.connection_type == 'serial':
            await self._connect_serial()
        else:
            raise ValueError("Invalid connection type specified")

    async def _connect_ip(self):
        """Internal method for making the IP connection."""
        _LOGGER.info(f"Starting connection to Crow IP Module... at {self._alarmPanel.host}:{self._alarmPanel.port}")
        coro = self._eventLoop.create_connection(lambda: self, self._alarmPanel.host, int(self._alarmPanel.port))
        try:
            await asyncio.wait_for(coro, timeout=self._alarmPanel.connection_timeout)
        except asyncio.TimeoutError:
            _LOGGER.debug('Timeout connecting to Crow IP module...')
            self.handle_connect_failure()

    async def _connect_serial(self):
        """Internal method for making the serial connection."""
        _LOGGER.info(f"Starting connection to Crow Serial Module... at {self._alarmPanel.port}")
        coro = serial_asyncio.create_serial_connection(self._eventLoop, lambda: self, self._alarmPanel.port, baudrate=9600)
        try:
            await asyncio.wait_for(coro, timeout=self._alarmPanel.connection_timeout)
        except asyncio.TimeoutError:
            _LOGGER.debug('Timeout connecting to Crow Serial module...')
            self.handle_connect_failure()

    # END OF CHANGES

    def connection_made(self, transport):
        """asyncio callback for a successful connection."""
        _LOGGER.info("Connection Successful!")
        self._transport = transport
        self._connected = True
        self._alarmPanel.callback_connected(self._connected)
        if self._connected:
            if self._alarmPanel.connection_type == 'ip':
                self.send_command('status','')
            elif self._alarmPanel.connection_type == 'serial':
                self.send_command('?', '')
        
    def connection_lost(self, exc):
        """asyncio callback for connection lost."""
        self._connected = False
        if not self._shutdown:
            _LOGGER.error('The server closed the connection. Reconnecting...')
            ensure_future(self.reconnect(self._alarmPanel.connection_timeout), loop=self._eventLoop)

    async def reconnect(self, delay):
        """Internal method for reconnecting."""
        self.disconnect()
        await asyncio.sleep(delay)
        await self.connect()
           
    def disconnect(self):
        """Internal method for forcing connection closure if hung."""
        _LOGGER.debug('Disconnecting server...')
        if self._transport:
            self._transport.close()
            
    def send_data(self, data):
        """Raw data send- just make sure it's encoded properly and logged."""
        _LOGGER.debug(str.format('Sent: {0}', (data + '\r\n').encode('ascii')))
        try:
            self._transport.write((data + '\r\n').encode('ascii'))
        except RuntimeError as err:
            _LOGGER.error(str.format('Failed to send. Reconnecting. ({0}) ', err))
            self._connected = False
            if not self._shutdown:
                ensure_future(self.reconnect(self._alarmPanel.connection_timeout), loop=self._eventLoop)

    def send_command(self, code, data):
        """Send a command in the proper format."""
        if data == '':
            to_send = COMMANDS[code] + ' '
        else:
            if COMMANDS[code]=='OO':
                to_send = COMMANDS[code] + data
            else:
                to_send = COMMANDS[code] + ' ' + data
        self.send_data(to_send)

    def data_received(self, data):
        """asyncio callback for any data received from the Module."""
        _LOGGER.debug(data)
        self._buffer += data
        
        if self._alarmPanel.connection_type == 'serial':
            if b'\n\r' in self._buffer:
                line, self._buffer = self._buffer.split(b'\n\r', 1)
                self.process_line(line.decode('ascii').strip())
                _LOGGER.debug(self._buffer)
                self._buffer = b''
                
        else:
            fullData = data.decode('ascii').strip()
            lines = str.split(fullData, '\n\r')
            for line in lines:
                self.process_line(line)

    def process_line(self, line):
        """Process a complete line of data."""
        if line:
            try:
                _LOGGER.debug('----------------------------------------')
                _LOGGER.debug(f'Received: {line}')
                parsed = self.parseHandler(line)
                _LOGGER.debug(f'Parsed: {parsed}')
                
                try:
                    _LOGGER.debug(f'Calling handler: {parsed["handler"]} for message: {parsed["name"]} with data: {parsed["data"]}')
                    handlerFunc = getattr(self, parsed['handler'])
                    result = handlerFunc(parsed)
                except (AttributeError, TypeError, KeyError) as err:
                    _LOGGER.debug("No handler configured for message.")
                    _LOGGER.debug(f"Error: {err}")

                try:
                    _LOGGER.debug(f'Invoking callback: {parsed["callback"]}')
                    callbackFunc = getattr(self._alarmPanel, parsed['callback'])
                    callbackFunc(result)
                except (AttributeError, TypeError, KeyError) as err:
                    _LOGGER.debug("No callback configured for the command.")
                    _LOGGER.debug(f"Error: {err}")

                _LOGGER.debug('----------------------------------------')
            except Exception as e:
                _LOGGER.error(f'Error processing received data: {e}')


    def parseHandler(self, rawInput):
        """When the Module contacts us- parse out message and data."""
        _LOGGER.debug(str.format('Parsing response line: {0}', rawInput))
        result = {}
        if rawInput != '':
            for attribute, format in RESPONSE_FORMATS.items():
                match = re.match(attribute, rawInput)
                if match:
                    _LOGGER.debug(str.format('Match found for {0}', attribute))
                    result['attribute'] = format['attr']
                    result['name'] = format['name']
                    result['status'] = format['status']
                    result['handler'] = "handle_%s" % format['handler']
                    result['callback'] = "callback_%s" % format['handler']
                    if format['handler'] == 'area_state_change':
                        result['area'] = format['area']
                    if match.groups():
                        result['data'] = match.group('data')
                    else:
                        result['data'] = ''
                    break
                else:
# v.0.27 Commented out for shorter debug log
#                    _LOGGER.debug(str.format('No Match found for {0}', attribute))
                  pass
        return result

    async def keep_alive(self):
        """Send a STATUS keepalive command to reset it's watchdog timer and latest status."""
        while not self._shutdown:
            if self._connected:
                if self._alarmPanel.connection_type == 'ip':
                    self.send_command('status','')
                elif self._alarmPanel.connection_type == 'serial':
                    self.send_command('?', '')
            await asyncio.sleep(self._alarmPanel.keepalive_interval)

    def arm_stay(self):
        """Public method to arm/stay a partition."""
        self.send_command('stay', '')

    def arm_away(self):
        """Public method to arm/away a partition."""
        self.send_command('arm', '')

    def disarm(self, code):
        """Public method to disarm a partition."""
        self._cachedCode = code
        self.send_command('disarm', str(code)+'E')
#        await asyncio.sleep(1)
        self.send_command('status', '')

    def send_keys(self, keys):
        """Public method to disarm a partition."""
        self.send_command('keys', str(keys)+'E')    

    def panic_alarm(self, panicType):
        """Public method to raise a panic alarm."""
        self.send_command('panic', '')

    def toggle_output(self, outputNumber):
        """Used to toggle the selected command output"""
        self.send_command('toogle_output_x', str(outputNumber))	

    def handle_connect_failure(self):
        """Handler for if we fail to connect to the Module."""
        self._connected = False
        if not self._shutdown:
            _LOGGER.error('Unable to connect to IP Module. Reconnecting...')
            self._alarmPanel._loginTimeoutCallback(False)
            ensure_future(self.reconnect(self._alarmPanel.connection_timeout), loop=self._eventLoop)
		
    def handle_system_state_change(self,msg):
        _LOGGER.debug('Setting System State %s to %s', msg['name'], str(msg['status']))
        self._alarmPanel.system_state['status'][msg['attribute']] = msg['status']
        return msg['attribute']

    def handle_output_state_change(self,msg):
        _LOGGER.debug('Setting Output State %s to %s', msg['name'], str(msg['data']))
        outputNumber = msg['data']
        self._alarmPanel.output_state[int(msg['data'])]['status'][msg['attribute']] = msg['status']
        return outputNumber

    def handle_area_state_change(self,msg):
        _LOGGER.debug('Setting %s to %s', msg['name'], str(msg['status']))
        if msg['area'] == '1':
            areaNumber = 'A'
        else:
            areaNumber = 'B'
        
        # Reset Area Status
        self._alarmPanel.area_state[int(msg['area'])]['status']['armed'] = False
        self._alarmPanel.area_state[int(msg['area'])]['status']['stay_armed'] = False
        self._alarmPanel.area_state[int(msg['area'])]['status']['disarmed'] = False
        self._alarmPanel.area_state[int(msg['area'])]['status']['exit_delay'] = False
        self._alarmPanel.area_state[int(msg['area'])]['status']['stay_exit_delay'] = False
        
        self._alarmPanel.area_state[int(msg['area'])]['status'][msg['attribute']] = msg['status']
        if self._alarmPanel.area_state[int(msg['area'])]['status']['disarmed']:
            self._alarmPanel.area_state[int(msg['area'])]['status']['alarm'] = False
            self._alarmPanel.area_state[int(msg['area'])]['status']['alarm_zone'] = ''

        return areaNumber
 
    def handle_zone_state_change(self,msg):
        _LOGGER.debug('Setting %s of %s', msg['name'], msg['data'])
        zoneNumber = msg['data']
        self._alarmPanel.zone_state[int(zoneNumber)]['status'][msg['attribute']] = msg['status']
        if msg['attribute'] == 'alarm':
            if msg['status']:
                _LOGGER.error('ALARM RAISED !!!')                
                self._alarmPanel.area_state[1]['status']['alarm_zone']=zoneNumber
                self._alarmPanel.area_state[2]['status']['alarm_zone']=zoneNumber
                self._alarmPanel.area_state[1]['status']['alarm']=True
                self._alarmPanel.area_state[2]['status']['alarm']=True
            else:
                _LOGGER.error('ALARM RESTORED...') 
                self._alarmPanel.area_state[1]['status']['alarm_zone']=''
                self._alarmPanel.area_state[2]['status']['alarm_zone']=''
                self._alarmPanel.area_state[1]['status']['alarm']=False
                self._alarmPanel.area_state[2]['status']['alarm']=False
            try:
                _LOGGER.debug('Invoking callback within zone state change...')                
                self._alarmPanel.callback_area_state_change('A')
                self._alarmPanel.callback_area_state_change('B')
            except (AttributeError, TypeError, KeyError) as err:
                    _LOGGER.debug("No callback configured for the command."+str(err))

        return zoneNumber
