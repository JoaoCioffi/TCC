"""Library for interacting with DJI Ryze Tello drones.
"""

# coding=utf-8
import logging
import socket
import time
from threading import Thread
from typing import Optional, Union, Type, Dict

from .enforce_types import enforce_types

import av
import numpy as np


threads_initialized = False
drones: Optional[dict] = {}
client_socket: socket.socket


class TelloException(Exception):
    pass


@enforce_types
class Tello:
    """Python wrapper to interact with the Ryze Tello drone using the official Tello api.
    Tello API documentation:
    [1.3](https://dl-cdn.ryzerobotics.com/downloads/tello/20180910/Tello%20SDK%20Documentation%20EN_1.3.pdf),
    [2.0 with EDU-only commands](https://dl-cdn.ryzerobotics.com/downloads/Tello/Tello%20SDK%202.0%20User%20Guide.pdf)
    """
    # Send and receive commands, client socket
    RESPONSE_TIMEOUT = 7.  # in seconds
    TAKEOFF_TIMEOUT = 20.  # in seconds
    FRAME_GRAB_TIMEOUT = 5
    TIME_BTW_COMMANDS = 1.e-1  # in seconds
    TIME_BTW_RC_CONTROL_COMMANDS = 1.e-3  # in seconds
    RETRY_COUNT = 3  # number of retries after a failed command
    TELLO_IP = '192.168.10.1'  # Tello IP address

    # Video stream, server socket
    VS_UDP_IP = '0.0.0.0'
    VS_UDP_PORT = 11111

    CONTROL_UDP_PORT = 8889
    STATE_UDP_PORT = 8890