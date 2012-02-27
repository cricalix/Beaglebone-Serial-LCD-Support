import serial
import os
import string
import logging
import sys

class SerialDisplay:
    """Root class for driving serial displays

    Implements stub methods, but can't actually drive any serial display
    itself.

    """
    supported_fonts = {}
    display_limits = {}

    def __init__(self):
        print __name__
