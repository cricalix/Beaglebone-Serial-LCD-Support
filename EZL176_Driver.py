import logging
import sys
import serial
import struct

from collections import namedtuple
from SerialDisplay import SerialDisplay
log = logging.getLogger(__name__)

class EZL176_Driver(SerialDisplay):
    FONT_5x7=0
    FONT_8x8=1
    FONT_8x12=2
    supported_fonts = {FONT_5x7: '5x7', FONT_8x8: '8x8', FONT_8x12: '8x12'}
    display_limits = {
        FONT_5x7: {'lines': 27, 'cols': 29},
        FONT_8x8: {'lines': 27, 'cols': 22},
        FONT_8x12: {'lines': 18, 'cols': 22}
        }
    display_pixels_x = 176
    display_pixels_y = 220
    ACK='\x06'
    NAK='\x15'

    def __init__(self, device='/dev/ttyO1'):
        self.device = device
        self.comm_speed = 19200
        self.comm_timeout = 1 # seconds
        self.mode = 0
        self.rx_flag = 32
        self.rx_mux = 'uart1_rxd'
        self.tx_mux = 'uart1_txd'
        self.mux_path = '/sys/kernel/debug/omap_mux/'
        self.display = None

    def initialise(self):
        log.debug('Initialise')
        self.__init_mux()
        self.display = self.__init_serial()

    def displayPixels(self):
        # download.tigal.com/ezoled/EZL-176_datasheet_1.1.pdf
        return [display_pixels_x, display_pixels_y]

    def deviceInfo(self):
        return 'EZL-176, powered by 4D-Labs GOLDELOX'

    def hardwareInfo(self):
        if self.display:
            self.display.write('V')
            data = self.display.read(4)
            # The 176 returns 5 bytes of data.
            if len(data) == 0:
                raise Exception('Failed to read hardware information')
            dev_type, silicon_rev, pmmc_rev, res1 = struct.unpack('BBBB', data)
            return [dev_type, silicon_rev, pmmc_rev]
        else:
            return None

    def doCommand(self, cmd):
        self.display.write(cmd)
        res = self.display.read(1)
        return res == EZL176_Driver.ACK

    def CLS(self):
        return self.doCommand('E')

    def setSolid(self):
        self.__setPenSize(0)

    def setWireframe(self):
        self.__setPenSize(1)

    def __setPenSize(self, size):
        self.display.write('p%c' % (size))
        self.display.read(1)

    def string(self, str, indent=1, line=0, font=FONT_8x8, colour1=0xFF,
            colour2=0xFF):
        """Write an ASCII string to the display

        str(string) - value to display, limited to 255 characters
        indent(int) - number of columns to indent. width of a column is
                determined by the font size used and the GOLDELOX handles it.
        line(int) - the line number on the display. The maximum line number is
                determined by the font size in use.
        font(int) - One of three system-supplied fonts. Use the FONT_ defines
                for a shortcut.
        colour1, colour2(hex) - The MSB and LSB hex pairs that form a complete
                colour code for the string.
        """
        if len(str) > 255:
            raise "String length too long (255)"
        if display_limits[font]['lines'] < line:
            raise "Line position " + string(line) + " is out of bounds"
        if display_limits[font]['cols'] < indent:
            raise "Column position " + str(indent) + " is out of bounts"
        self.display.write('"s%c%c%c%c%c%s%c' %\
                (indent, line, font, colour1, colour2, str, 0x00))
        self.display.read(1)

    def rectangle(self, tx, ty, bx, by, colour1, colour2):
        self.setSolid()
        self.display.write('r%c%c%c%c%c%c' %
                (tx, ty, bx, by, colour1, colour2))
        self.display.read(1)

    def __init_mux(self):
        try:
            open(self.mux_path + self.rx_mux, 'wb').write("%X" %\
                (self.rx_flag + self.mode))
        except Exception as e:
            print e
            sys.exit(99)
        try:
            open(self.mux_path + self.tx_mux, 'wb').write("%X" %\
                (self.mode))
        except Exception as e:
            print e
            sys.exit(99)

    def __init_serial(self):
        s = None
        try:
            s = serial.Serial(baudrate=self.comm_speed, port=self.device,
                bytesize=8, parity='N', stopbits=1, timeout=self.comm_timeout)
            s.open()
        except Exception as e:
            print e
            sys.exit(88)
        return s
