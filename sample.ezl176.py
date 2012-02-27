#!/usr/bin/python

import EZL176_Driver

if __name__ == "__main__":
    c = EZL176_Driver()
    if c.display.isOpen():
        print 'Autobaud'
        c.display.write('U')
        c.display.read(1)
        c.CLS()
        c.CLS()
        s = 'Hello'
        c.string(s,1,1,FONT_8x12,0xFF,0xAF)
        print 'Sending ' + s
        c.display.read(1)
        s = 'Dad!'
        print 'Sending ' + s
        c.string(s,1,2,FONT_8x12,0xFF,0xAF)
        c.display.read(1)
        c.rectangle(50,50,70,70,0xAF, 0xAF)
        c.rectangle(71,50,91,70,0x01, 0x0F)
        c.string(line=100, indent=5, str='Hello me')
