import SerialDisplay

class EZL176_Driver(SerialDisplay):
    supported_fonts = {FONT_5x7: 0, FONT_8x8: 1, FONT_8x12: 2}
    display_limits = {FONT_5x7: {'lines': 27, 'cols': 29},
        FONT_8x8: {'lines': 27, 'cols': 22},
        FONT_8x12: {'lines': 18, 'cols': 22}}

    def __init__(self, device='/dev/ttyO1'):
        self.device = device
        self.mode = 0
        self.rx_flag = 32
        self.rx_mux = 'uart1_rxd'
        self.tx_mux = 'uart1_txd'
        self.mux_path = '/sys/kernel/debug/omap_mux/'
        self.__init_mux()
        self.display = self.__init_serial()

    def CLS(self):
        self.display.write('E')
        self.display.read(1)

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
        try:
            s = serial.Serial()
            s.baudrate = 19200
            s.port = self.device
            s.bytesize = 8
            s.parity = 'N'
            s.stopbits = 1
            s.timeout = 1
            s.open()
        except Exception as e:
            print e
            sys.exit(88)
        return s
