import serial
import os
import string
import logging
import sys

log = logging.getLogger(__name__)

class SerialDisplay:
    """Root class for driving serial displays

    Implements stub methods, but can't actually drive any serial display
    itself.

    """
    supported_fonts = {}
    display_limits = {}

    def __init__(self, device=None):
        # Set up the logger
        log.debug('Init')

    def supportedFonts(self):
        # A way to print out what fonts the device supports
        # Base class should print something like 'None'
        return None

    def displayLimits(self):
        # A way to print out what the display row/col limits are.
        # Base class should print something like 'None'
        return None

    def displayPixels(self):
        return None

    def displayInfo(self):
        return 'Base class, no device driver instantiated'
