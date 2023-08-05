# Copyright (c) 2020 embyt GmbH. See LICENSE for further details.
# Author: Roman Morawek <roman.morawek@embyt.com>
"""this class handles the enocean and mqtt interfaces"""
import logging
import queue
import numbers
import json
import platform

from enocean.communicators.serialcommunicator import SerialCommunicator
from enocean.protocol.packet import RadioPacket
from enocean.protocol.constants import PACKET, RETURN_CODE
import enocean.utils
import paho.mqtt.client as mqtt


class Communicator:
    """the main working class providing the MQTT interface to the enocean packet classes"""
    mqtt = None
    enocean = None

    CONNECTION_RETURN_CODE = [
        "connection successful",
        "incorrect protocol version",
        "invalid client identifier",
        "server unavailable",
        "bad username or password",
        "not authorised",
    ]

    def __init__(self, config, sensors):
        self.conf = config
        self.sensors = sensors

        # check for mandatory configuration
        if 'mqtt_host' not in self.conf or 'enocean_port' not in self.conf:
            raise Exception("Mandatory configuration not found: mqtt_host/enocean_port")
        mqtt_port = int(self.conf['mqtt_port']) if 'mqtt_port' in self.conf else 1883
        mqtt_keepalive = int(self.conf['mqtt_keepalive']) if 'mqtt_keepalive' in self.conf else 60

        # setup mqtt connection
        client_id = self.conf['mqtt_client_id'] if 'mqtt_client_id' in self.conf else ''
        self.mqtt = mqtt.Client(client_id=client_id)
        self.mqtt.on_connect = self._on_connect
        self.mqtt.on_disconnect = self._on_disconnect
        self.mqtt.on_message = self._on_mqtt_message
        self.mqtt.on_publish = self._on_mqtt_publish
        if 'mqtt_user' in self.conf:
            logging.info("Authenticating: %s", self.conf['mqtt_user'])
            self.mqtt.username_pw_set(self.conf['mqtt_user'], self.conf['mqtt_pwd'])
        if str(self.conf.get('mqtt_ssl')) in ("True", "true", "1"):
            logging.info("Enabling SSL")
            ca_certs = self.conf['mqtt_ssl_ca_certs'] if 'mqtt_ssl_ca_certs' in self.conf else None
            certfile = self.conf['mqtt_ssl_certfile'] if 'mqtt_ssl_certfile' in self.conf else None
            keyfile = self.conf['mqtt_ssl_keyfile'] if 'mqtt_ssl_keyfile' in self.conf else None
            self.mqtt.tls_set(ca_certs=ca_certs, certfile=certfile, keyfile=keyfile)
            if str(self.conf.get('mqtt_ssl_insecure')) in ("True", "true", "1"):
                logging.warning("Disabling SSL certificate verification")
                self.mqtt.tls_insecure_set(True)
        if str(self.conf.get('mqtt_debug')) in ("True", "true", "1"):
            self.mqtt.enable_logger()
        logging.debug("Connecting to host %s, port %s, keepalive %s",
                      self.conf['mqtt_host'], mqtt_port, mqtt_keepalive)
        self.mqtt.connect_async(self.conf['mqtt_host'], port=mqtt_port, keepalive=mqtt_keepalive)
        self.mqtt.loop_start()

        # setup enocean communication
        self.enocean = SerialCommunicator(self.conf['enocean_port'])
        self.enocean.start()
        # sender will be automatically determined
        self.enocean_sender = None

    def __del__(self):
        if self.enocean is not None and self.enocean.is_alive():
            self.enocean.stop()

    def _on_connect(self, mqtt_client, _userdata, _flags, return_code):
        '''callback for when the client receives a CONNACK response from the MQTT server.'''
        if return_code == 0:
            logging.info("Succesfully connected to MQTT broker.")
            # listen to enocean send requests
            for cur_sensor in self.sensors:
                # logging.debug("MQTT subscribing: %s", cur_sensor['name']+'/req/#')
                mqtt_client.subscribe(cur_sensor['name']+'/req/#')
        else:
            logging.error("Error connecting to MQTT broker: %s",
                          self.CONNECTION_RETURN_CODE[return_code]
                          if return_code < len(self.CONNECTION_RETURN_CODE) else return_code)

    def _on_disconnect(self, _mqtt_client, _userdata, return_code):
        '''callback for when the client disconnects from the MQTT server.'''
        if return_code == 0:
            logging.warning("Successfully disconnected from MQTT broker")
        else:
            logging.warning("Unexpectedly disconnected from MQTT broker: %s",
                            self.CONNECTION_RETURN_CODE[return_code]
                            if return_code < len(self.CONNECTION_RETURN_CODE) else return_code)

    def _on_mqtt_message(self, _mqtt_client, _userdata, msg):
        '''the callback for when a PUBLISH message is received from the MQTT server.'''
        # search for sensor
        found_topic = False
        logging.debug("Got MQTT message: %s", msg.topic)
        for cur_sensor in self.sensors:
            if cur_sensor['name'] in msg.topic:
                # get message topic
                prop = msg.topic[len(cur_sensor['name']+"/req/"):]
                # do we face a send request?
                if prop == "send":
                    found_topic = True
                    logging.debug("Trigger message to: %s", cur_sensor['name'])
                    destination = [(cur_sensor['address'] >> i*8) &
                                   0xff for i in reversed(range(4))]

                    # Retrieve command from MQTT message and pass it to _send_packet()
                    command = None
                    command_shortcut = cur_sensor.get('command')

                    if command_shortcut:
                        # Check MQTT message has valid data
                        if 'data' not in cur_sensor:
                            logging.warning('No data to send from MQTT message!')
                            return
                        # Check MQTT message sets the command field
                        if command_shortcut not in cur_sensor['data']:
                            logging.warning(
                                'Command field %s must be set in MQTT message!', command_shortcut)
                            return
                        # Retrieve command id from MQTT message
                        command = cur_sensor['data'][command_shortcut]
                        logging.debug('Retrieved command id from MQTT message: %s', hex(command))

                    self._send_packet(cur_sensor, destination, command)

                    # Clear sent data, if requested by the send message
                    # MQTT payload is binary data, thus we need to decode it
                    if msg.payload.decode('UTF-8') == "clear":
                        logging.debug('Clearing data buffer.')
                        del cur_sensor['data']

                else:
                    found_topic = True
                    # parse message content
                    value = None
                    try:
                        value = int(msg.payload)
                    except ValueError:
                        logging.warning("Cannot parse int value for %s: %s", msg.topic, msg.payload)
                    # store received data
                    logging.debug("%s: %s=%s", cur_sensor['name'], prop, value)
                    if 'data' not in cur_sensor:
                        cur_sensor['data'] = {}
                    cur_sensor['data'][prop] = value
        if not found_topic:
            logging.warning("Unexpected MQTT message: %s", msg.topic)

    def _on_mqtt_publish(self, _mqtt_client, _userdata, _mid):
        '''the callback for when a PUBLISH message is successfully sent to the MQTT server.'''
        #logging.debug("Published MQTT message "+str(mid))

    def _get_command_id(self, packet, cur_sensor):
        '''interpret packet to retrieve command id from VLD packets'''
        # Retrieve the first defined EEP profile matching sensor RORG-FUNC-TYPE
        # As we take the first defined profile, this suppose that command is
        # ALWAYS at the same offset and ALWAYS has the same size.
        profile = packet.eep.find_profile(
            packet._bit_data, cur_sensor['rorg'], cur_sensor['func'], cur_sensor['type'])

        # Loop over profile contents
        for source in profile.contents:
            if not source.name:
                continue
            # Check the current shortcut matches the command shortcut
            if source['shortcut'] == cur_sensor.get('command'):
                return packet.eep._get_raw(source, packet._bit_data)

        # If not found, return None for default handling of the packet
        return None

    def _read_packet(self, packet):
        '''interpret packet, read properties and publish to MQTT'''
        mqtt_publish_json = 'mqtt_publish_json' in self.conf and \
            self.conf['mqtt_publish_json'] in ("True", "true", "1")
        mqtt_json = {}
        # loop through all configured devices
        for cur_sensor in self.sensors:
            # does this sensor match?
            if enocean.utils.combine_hex(packet.sender) == cur_sensor['address']:
                # found sensor configured in config file
                if str(cur_sensor.get('publish_rssi')) in ("True", "true", "1"):
                    if mqtt_publish_json:
                        mqtt_json['RSSI'] = packet.dBm
                    else:
                        self.mqtt.publish(cur_sensor['name']+"/RSSI", packet.dBm)
                if not packet.learn or str(cur_sensor.get('log_learn')) in ("True", "true", "1"):
                    retain = str(cur_sensor.get('persistent')) in ("True", "true", "1")
                    found_property = self._handle_data_packet(
                        packet, cur_sensor,
                        mqtt_json if mqtt_publish_json else None, retain
                    )
                    if not found_property:
                        logging.warning("message not interpretable: %s", cur_sensor['name'])
                    elif mqtt_publish_json:
                        name = cur_sensor['name']
                        value = json.dumps(mqtt_json)
                        logging.debug("%s: Sent MQTT: %s", name, value)
                        self.mqtt.publish(name, value, retain=retain)
                else:
                    # learn request received
                    logging.info("learn request not emitted to mqtt")

    def _handle_data_packet(self, packet, sensor, mqtt_json, retain: bool):
        # data packet received
        found_property = False
        if packet.packet_type == PACKET.RADIO and packet.rorg == sensor['rorg']:
            # radio packet of proper rorg type received; parse EEP
            direction = sensor.get('direction')

            # Retrieve command from the received packet and pass it to parse_eep()
            command = None
            if sensor.get('command'):
                command = self._get_command_id(packet, sensor)
                logging.debug('Retrieved command id from packet: %s', hex(command))

            # Retrieve properties from EEP
            properties = packet.parse_eep(
                sensor['func'], sensor['type'], direction, command)

            # loop through all EEP properties
            for prop_name in properties:
                found_property = True
                cur_prop = packet.parsed[prop_name]
                # we only extract numeric values, either the scaled ones
                # or the raw values for enums
                if isinstance(cur_prop['value'], numbers.Number):
                    value = cur_prop['value']
                else:
                    value = cur_prop['raw_value']
                # publish extracted information
                logging.debug("%s: %s (%s)=%s %s", sensor['name'], prop_name,
                              cur_prop['description'], cur_prop['value'], cur_prop['unit'])
                retain = str(sensor.get('persistent')) in ("True", "true", "1")
                if mqtt_json is not None:
                    mqtt_json[prop_name] = value
                else:
                    self.mqtt.publish(f"{sensor['name']}/{prop_name}", value, retain=retain)
        return found_property

    def _reply_packet(self, in_packet, sensor):
        '''send enocean message as a reply to an incoming message'''
        # prepare addresses
        destination = in_packet.sender

        self._send_packet(sensor, destination, None, True,
                          in_packet.data if in_packet.learn else None)

    def _send_packet(self, sensor, destination, command=None,
                     negate_direction=False, learn_data=None):
        '''triggers sending of an enocean packet'''
        # determine direction indicator
        if 'direction' in sensor:
            direction = sensor['direction']
            if negate_direction:
                # we invert the direction in this reply
                direction = 1 if direction == 2 else 2
        else:
            direction = None
        # is this a response to a learn packet?
        is_learn = learn_data is not None

        # Add possibility for the user to indicate a specific sender address
        # in sensor configuration using added 'sender' field.
        # So use specified sender address if any
        if 'sender' in sensor:
            sender = [(sensor['sender'] >> i*8) & 0xff for i in reversed(range(4))]
        else:
            sender = self.enocean_sender

        try:
            # Now pass command to RadioPacket.create()
            packet = RadioPacket.create(sensor['rorg'], sensor['func'], sensor['type'],
                                        direction=direction, command=command, sender=sender,
                                        destination=destination, learn=is_learn)
        except ValueError as err:
            logging.error("Cannot create RF packet: %s", err)
            return

        # assemble data based on packet type (learn / data)
        if not is_learn:
            # data packet received
            # start with default data

            # Initialize packet with default_data if specified
            if 'default_data' in sensor:
                packet.data[1:5] = [(sensor['default_data'] >> i*8) &
                                    0xff for i in reversed(range(4))]

            # do we have specific data to send?
            if 'data' in sensor:
                # override with specific data settings
                logging.debug("sensor data: %s", sensor['data'])
                packet.set_eep(sensor['data'])
                packet.parse_eep()  # ensure that the logging output of packet is updated
            else:
                # what to do if we have no data to send yet?
                logging.warning('sending only default data as answer to %s', sensor['name'])

        else:
            # learn request received
            # copy EEP and manufacturer ID
            packet.data[1:5] = learn_data[1:5]
            # update flags to acknowledge learn request
            packet.data[4] = 0xf0

        # send it
        logging.info("sending: %s", packet)
        self.enocean.send(packet)

    def _process_radio_packet(self, packet):
        # first, look whether we have this sensor configured
        found_sensor = False
        for cur_sensor in self.sensors:
            if 'address' in cur_sensor and \
                    enocean.utils.combine_hex(packet.sender) == cur_sensor['address']:
                found_sensor = cur_sensor

        # skip ignored sensors
        if found_sensor and 'ignore' in found_sensor and found_sensor['ignore']:
            return

        # log packet, if not disabled
        if str(self.conf.get('log_packets')) in ("True", "true", "1"):
            logging.info("received: %s", packet)

        # abort loop if sensor not found
        if not found_sensor:
            logging.info("unknown sensor: %s", enocean.utils.to_hex_string(packet.sender))
            return

        # interpret packet, read properties and publish to MQTT
        self._read_packet(packet)

        # check for neccessary reply
        if str(found_sensor.get('answer')) in ("True", "true", "1"):
            self._reply_packet(packet, found_sensor)

    def run(self):
        """the main loop with blocking enocean packet receive handler"""
        # start endless loop for listening
        while self.enocean.is_alive():
            # Request transmitter ID, if needed
            if self.enocean_sender is None:
                self.enocean_sender = self.enocean.base_id

            # Loop to empty the queue...
            try:
                # get next packet
                if platform.system() == 'Windows':
                    # only timeout on Windows for KeyboardInterrupt checking
                    packet = self.enocean.receive.get(block=True, timeout=1)
                else:
                    packet = self.enocean.receive.get(block=True)

                # check packet type
                if packet.packet_type == PACKET.RADIO:
                    self._process_radio_packet(packet)
                elif packet.packet_type == PACKET.RESPONSE:
                    response_code = RETURN_CODE(packet.data[0])
                    logging.info("got response packet: %s", response_code.name)
                else:
                    logging.info("got non-RF packet: %s", packet)
                    continue
            except queue.Empty:
                continue
            except KeyboardInterrupt:
                logging.debug("Exception: KeyboardInterrupt")
                break

        # Run finished, close MQTT client and stop Enocean thread
        logging.debug("Cleaning up")
        self.mqtt.loop_stop()
        self.mqtt.disconnect()
        self.mqtt.loop_forever()  # will block until disconnect complete
        self.enocean.stop()
