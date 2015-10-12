# Generated by uvusbreplay 0.1
# uvusbreplay copyright 2011 John McMaster <JohnDMcMaster@gmail.com>
# cmd: /home/mcmaster/bin/usbrply bp1410_15_startup_cold.cap --comment --fx2 --device 24 -r 169:264 --sleep
        
from uvscada.usb import usb_wraps
from uvscada.usb import validate_read, validate_readv
from uvscada.bpm.bp1410_fw import load_fx2
from uvscada.bpm import bp1410_fw_sn
from uvscada.util import hexdump, str2hex

import binascii
import struct
from collections import namedtuple

def bulk86(dev, target=None, donef=None, truncate=False):
    bulkRead, _bulkWrite, _controlRead, _controlWrite = usb_wraps(dev)
    
    if donef is None:
        if target is None:
            raise Exception("requires target")
        def donef(buff):
            return len(buff) >= target
    
    def nxt():
        p = bulkRead(0x86, 0x0200)
        #print str2hex(p)
        if ord(p[0]) != 0x08:
            raise Exception("Bad prefix")
        if ord(p[-1]) != 0x00:
            raise Exception("Bad suffix")
        size = ord(p[-2])
        if size != len(p) - 3:
            if truncate and size < len(p) - 3:
                return p[1:1 + size]
            else:
                print 'Truncate: %s' % truncate
                print size, len(p) - 3, len(p)
                hexdump(p)
                raise Exception("Bad length")
        return p[1:-2]

    buff = ''
    while not donef(buff):
        if buff:
            print 'NOTE: split packet'
            hexdump(buff)
        buff += nxt()
    #print 'Done w/ buff len %d' % len(buff)
    if target and len(buff) > target:
        raise Exception('Buffer grew too big')
    return buff

# FIXME: with target set small but not truncate will happily truncate
def bulk2(dev, cmd, target=None, donef=None, truncate=False):
    bulkRead, bulkWrite, _controlRead, _controlWrite = usb_wraps(dev)
    
    bulkWrite(0x02, cmd)
    return bulk86(dev, target=target, donef=donef, truncate=truncate)

def trim(s):
    return s[1:-2]

def boot_cold(dev):
    bulkRead, bulkWrite, controlRead, _controlWrite = usb_wraps(dev)
    
    # Generated from packet 70/71
    buff = bulk2(dev,
            "\x43\x19\x00\x00\x00\x3B\x66\x1B\x00\x00\xFE\xFF\x3B\x64\x1B\x00"
            "\x00\xFE\xFF\x00",
            target=2)
    validate_read("\xA4\x06", buff, "packet 72/73")
    
    
    # Generated from packet 74/75
    buff = bulk2(dev, '\x01', target=(132 - 3))
    validate_read(
              "\x80\xA4\x06\x02\x00\x22\x00\x43\x00\xC0\x03\x00\x08\xF8\x19"
              "\x00\x00\x30\x00\x80\x00\x00\x00\x00\x00\xC0\x00\x00\x00\x09\x00"
              "\x08\x00\xFF\x00\xE0\x14\x00\x00\xE8\x14\x00\x00\x84\x1C\x00\x00"
              "\xEC\x14\x00\x00\xD0\x19\xFF\xFF\xC0\x19\xFF\xFF\x00\x00\xF0\x3C"
              "\xFF\xFF\x00\x00\x00\x00\x02\x00\x80\x01\xD0\x01\x02\x00\x01\x00"
              "\x00\x00\x56\x10\x00\x00\x88\x1B\x00\x00\x6C\x1B\x00\x00\x00\x00"
              "\x00\x00\x64\x1B\x00\x00\x66\x1B\x00\x00\x68\x1B\x00\x00\x44\x1C"
              "\x00\x00\x70\x1B\x00\x00\x30\x11\x00\x00\x34\x11\x00\x00\x74\x1B"
              "\x00\x00", buff, "packet 76/77")
    
    # Generated from packet 78/79
    bulkWrite(0x02, "\x43\x19\x00\x00\x00\x11\xF0\xFF")
    # Generated from packet 80/85
    bulkWrite(0x02, bp1410_fw_sn.p223)
    # Generated from packet 81/86
    bulkWrite(0x02, bp1410_fw_sn.p224)
    # Generated from packet 82/87
    bulkWrite(0x02, bp1410_fw_sn.p225)
    # Generated from packet 83/88
    bulkWrite(0x02, bp1410_fw_sn.p226)
    # Generated from packet 84/89
    bulkWrite(0x02, bp1410_fw_sn.p227)
    
    # Generated from packet 90/91
    buff = bulk2(dev, "\x5A", target=1)
    validate_read("\x80", buff, "packet 92/93")
    
    # Generated from packet 94/95
    bulkWrite(0x02, "\x11\x10\x00")
    
    # Generated from packet 96/97
    bulkWrite(0x02, "\xEA\xCC\x64\x01\x00\x08\x00\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\x3F")
    
    # Generated from packet 98/99
    buff = bulk2(dev, "\xA6", target=1)
    validate_read("\x81", buff, "packet 100/101")
    
    # Generated from packet 102/103
    bulkWrite(0x02, "\x11\x4E\x00")
    
    # Generated from packet 104/105
    bulkWrite(0x02, "\xE8\x00\x00\x00\x00\xFA\x5A\x83\xEA\x05\x81\xEA\x00\x00\x01\x00"
              "\x81\xFA\x00\x00\x01\x00\x74\x1F\xBB\x00\x00\x00\x00\xB9\x00\x00"
              "\x01\x00\x66\x8B\x02\x66\x89\x83\x00\x00\x01\x00\x83\xC2\x02\x83"
              "\xC3\x02\x83\xE9\x02\x75\xEB\x8C\xC8\x50\xB8\xF0\xFF\x01\x00\x50"
              "\x0F\x20\xC0\x0D\x00\x00\x00\x60\x0F\x22\xC0\x0F\x09\xC3")
    
    # Generated from packet 106/107
    buff = bulk2(dev, "\xDB", target=1)
    validate_read("\x82", buff, "packet 108/109")
    
    # Generated from packet 110/111
    buff = bulk2(dev, "\x82", target=1)
    validate_read("\x16", buff, "packet 112/113")
    
    # Generated from packet 114/115
    exp =    ("\x84\xA4\x06\x02\x00\x26\x00\x43\x00\xC0\x03\x00\x08\x10\x24"
              "\x00\x00\x30\x00\x80\x00\x00\x00\x00\x00\xC0\x00\x00\x00\x09\x00"
              "\x08\x00\xFF\x00\xC4\x1E\x00\x00\xCC\x1E\x00\x00\xB4\x46\x00\x00"
              "\xD0\x1E\x00\x00\xC0\x1E\x01\x00\xB0\x1E\x01\x00\x00\x00\x30\x55"
              "\x01\x00\x00\x00\x00\x00\x02\x00\x80\x01\xD0\x01\x02\x00\x01\x00"
              "\x00\x00\x56\x10\x00\x00\xA0\x25\x00\x00\x84\x25\x00\x00\x00\x00"
              "\x01\x00\x7C\x25\x00\x00\x7E\x25\x00\x00\x80\x25\x00\x00\x74\x46"
              "\x00\x00\x38\x11\x00\x00\x3C\x11\x00\x00\x40\x11\x00\x00\x44\x11"
              "\x00\x00\xC0\x1E\x00\x00")
    # 133
    buff = bulk2(dev, '\x01', target=len(exp))
    validate_read(exp, buff, "packet 116/117")

def boot_warm(dev):
    # Generated from packet 70/71
    buff = bulk2(dev,
            "\x43\x19\x00\x00\x00\x3B\x7E\x25\x00\x00\xFE\xFF\x3B\x7C\x25\x00"
            "\x00\xFE\xFF\x00",
            target=2)
    validate_read("\xA4\x06", buff, "packet 72/73")
    
    # Generated from packet 74/75
    buff = bulk2(dev, '\x01', target=(136 - 3))
    validate_readv((r01_warm[1:-2], r01_glitch_154[1:-2], r01_glitches[1], r01_ps), buff, "packet 76/77")

r01_cold = ("\x08\x80\xA4\x06\x02\x00\x22\x00\x43\x00\xC0\x03\x00\x08\xF8\x19"
          "\x00\x00\x30\x00\x80\x00\x00\x00\x00\x00\xC0\x00\x00\x00\x09\x00"
          "\x08\x00\xFF\x00\xE0\x14\x00\x00\xE8\x14\x00\x00\x84\x1C\x00\x00"
          "\xEC\x14\x00\x00\xD0\x19\xFF\xFF\xC0\x19\xFF\xFF\x00\x00\xF0\x3C"
          "\xFF\xFF\x00\x00\x00\x00\x02\x00\x80\x01\xD0\x01\x02\x00\x01\x00"
          "\x00\x00\x56\x10\x00\x00\x88\x1B\x00\x00\x6C\x1B\x00\x00\x00\x00"
          "\x00\x00\x64\x1B\x00\x00\x66\x1B\x00\x00\x68\x1B\x00\x00\x44\x1C"
          "\x00\x00\x70\x1B\x00\x00\x30\x11\x00\x00\x34\x11\x00\x00\x74\x1B"
          "\x00\x00\x81\x00")
r01_warm = ("\x08\x84\xA4\x06\x02\x00\x26\x00\x43\x00\xC0\x03\x00\x08\x10\x24"
          "\x00\x00\x30\x00\x83\x00\x30\x01\x09\x00\xC0\x00\x00\x00\x09\x00"
          "\x08\x00\xFF\x00\xC4\x1E\x00\x00\xCC\x1E\x00\x00\xB4\x46\x00\x00"
          "\xD0\x1E\x00\x00\xC0\x1E\x01\x00\xB0\x1E\x01\x00\x00\x00\x30\x55"
          "\x01\x00\x00\x00\x00\x00\x02\x00\x80\x01\xD0\x01\x02\x00\x01\x00"
          "\x00\x00\x56\x10\x00\x00\xA0\x25\x00\x00\x84\x25\x00\x00\x00\x00"
          "\x01\x00\x7C\x25\x00\x00\x7E\x25\x00\x00\x80\x25\x00\x00\x74\x46"
          "\x00\x00\x38\x11\x00\x00\x3C\x11\x00\x00\x40\x11\x00\x00\x44\x11"
          "\x00\x00\xC0\x1E\x00\x00\x85\x00")
# warm glitched initially on 154/155
# after that stuck on 68/69
# Not sure what it means though
# Otherwise its a warm startup
r01_glitch_154 = (
          "\x08\x84\xA4\x06\x02\x00\x26\x00\x43\x00\xC0\x03\x00\x08\x10\x24"
          # Differences here
          "\x00\x00\x30\x00\x80\x00\x00\x00\x09\x00\xC0\x00\x00\x00\x09\x00"
          "\x08\x00\xFF\x00\xC4\x1E\x00\x00\xCC\x1E\x00\x00\xB4\x46\x00\x00"
          "\xD0\x1E\x00\x00\xC0\x1E\x01\x00\xB0\x1E\x01\x00\x00\x00\x30\x55"
          "\x01\x00\x00\x00\x00\x00\x02\x00\x80\x01\xD0\x01\x02\x00\x01\x00"
          "\x00\x00\x56\x10\x00\x00\xA0\x25\x00\x00\x84\x25\x00\x00\x00\x00"
          "\x01\x00\x7C\x25\x00\x00\x7E\x25\x00\x00\x80\x25\x00\x00\x74\x46"
          "\x00\x00\x38\x11\x00\x00\x3C\x11\x00\x00\x40\x11\x00\x00\x44\x11"
          "\x00\x00\xC0\x1E\x00\x00\x85\x00")

# rarer responses
r01_glitches = [
    binascii.unhexlify("84a406020026004300c0030008102400003000820010010900c000000009000800ff00c41e0000cc1e0000b4460000d01e0000c01e0100b01e01000000305501000000000002008001d00102000100000056100000a025000084250000000001007c2500007e2500008025000074460000381100003c1100004011000044110000c01e0000"),
    binascii.unhexlify('84a406020026004300c0030008102400003000830030010900c000000009000800ff00c41e0000cc1e0000b4460000d01e0000c01e0100b01e01000000305501000000000002008001c00102000100000056100000a025000084250000000001007c2500007e2500008025000074460000381100003c1100004011000044110000c01e0000'),
    ]

r01_ps = \
     "\x84\xA4\x06\x02\x00\x26\x00\x43\x00\xC0\x03\x00\x08\x10\x24\x00" \
    "\x00\x30\x00\x84\x00\x50\x01\x09\x00\xC0\x00\x00\x00\x09\x00\x08" \
    "\x00\xFF\x00\xC4\x1E\x00\x00\xCC\x1E\x00\x00\xB4\x46\x00\x00\xD0" \
    "\x1E\x00\x00\xC0\x1E\x01\x00\xB0\x1E\x01\x00\x00\x00\x30\x55\x01" \
    "\x00\x00\x00\x00\x00\x02\x00\x80\x01\xD0\x01\x02\x00\x01\x00\x00" \
    "\x00\x56\x10\x00\x00\xA0\x25\x00\x00\x84\x25\x00\x00\x00\x00\x01" \
    "\x00\x7C\x25\x00\x00\x7E\x25\x00\x00\x80\x25\x00\x00\x74\x46\x00" \
    "\x00\x38\x11\x00\x00\x3C\x11\x00\x00\x40\x11\x00\x00\x44\x11\x00" \
    "\x00\xC0\x1E\x00\x00"

r01_sm = \
    "\x80\xA4\x06\x02\x00\x22\x00\x43\x00\xC0\x03\x00\x08\xF8\x19\x00" \
    "\x00\x30\x00\x80\x00\x00\x00\x00\x00\xC0\x00\x00\x00\x09\x00\x08" \
    "\x00\xFF\x00\xE0\x14\x00\x00\xE8\x14\x00\x00\x84\x1C\x00\x00\xEC" \
    "\x14\x00\x00\xD0\x19\xFF\xFF\xC0\x19\xFF\xFF\x00\x00\xF0\x3C\xFF" \
    "\xFF\x00\x00\x00\x00\x02\x00\x80\x01\xE0\x01\x02\x00\x01\x00\x00" \
    "\x00\x56\x10\x00\x00\x88\x1B\x00\x00\x6C\x1B\x00\x00\x00\x00\x00" \
    "\x00\x64\x1B\x00\x00\x66\x1B\x00\x00\x68\x1B\x00\x00\x44\x1C\x00" \
    "\x00\x70\x1B\x00\x00\x30\x11\x00\x00\x34\x11\x00\x00\x74\x1B\x00" \
    "\x00"


GPIO_SM = 0x0001
# Not sure if this actually is GPIO
# but seems like a good guess given that it detects socket module insertion
def gpio_read(dev):
    buff = bulk2(dev, "\x03", target=2, truncate=True)
    validate_readv((
            "\x31\x00",
            "\x71\x04",
            "\x71\x00",
            
            # SM
            "\x30\x00",
            "\x30\x04",
            ),
            buff, "packet 128/129")
    return struct.unpack('<H', buff)[0]

def replay(dev):
    bulkRead, bulkWrite, controlRead, controlWrite = usb_wraps(dev)

    # Generated from packet 169/170
    # ...
    # Generated from packet 179/180
    load_fx2(dev)
    
    # Generated from packet 50/51
    # None (0xB0)
    buff = controlRead(0xC0, 0xB0, 0x0000, 0x0000, 4096)
    # NOTE:: req max 4096 but got 3
    validate_read("\x00\x00\x00", buff, "packet 50/51")
    # Generated from packet 55/56
    # None (0xB0)
    buff = controlRead(0xC0, 0xB0, 0x0000, 0x0000, 4096)
    # NOTE:: req max 4096 but got 3
    validate_read("\x00\x00\x00", buff, "packet 55/56")
    # Generated from packet 57/58
    buff = bulkRead(0x86, 0x0200)
    # NOTE:: req max 512 but got 4
    validate_read("\x08\x16\x01\x00", buff, "packet 57/58")
    # Generated from packet 62/63
    # None (0xB0)
    buff = controlRead(0xC0, 0xB0, 0x0000, 0x0000, 4096)
    # NOTE:: req max 4096 but got 3
    validate_read("\x00\x00\x00", buff, "packet 62/63")
    # Generated from packet 64/65
    buff = bulkRead(0x86, 0x0200)
    # NOTE:: req max 512 but got 4
    validate_read("\x08\x16\x01\x00", buff, "packet 64/65")

    # Generated from packet 66/67
    # FIXME: len(cold) != len(warm)
    # not perfect but should catch most errors
    # how does BP handle this?
    # am I supposed to be decoding this data structure as I go to determine the length?
    def donef(buff):
        return len(buff) == 129 or len(buff) == 133
    buff = bulk2(dev, '\x01', donef=donef)
    
    validate_readv([trim(r01_cold), trim(r01_warm), trim(r01_glitch_154), r01_ps, r01_sm] + r01_glitches, buff, "packet 68/69 (warm/cold)")
    # Seems to be okay if we always do this although its only sometimes needed
    glitch_154 = True
    if buff == trim(r01_cold):
        print 'Cold boot'
        # 70-117
        boot_cold(dev)
    elif buff in (trim(r01_warm), r01_ps, r01_sm) or buff in r01_glitches:
        print 'Warm boot'
        # 70-76
        boot_warm(dev)
    elif buff == trim(r01_glitch_154):
        print 'Warm boot (glitch)'
        glitch_154 = True
        # 70-76
        boot_warm(dev)
    else:
        raise Exception("Bad warm/cold response")

    # Packets going forward are from cold boot since its more canonical / clean
    # warm -40 packet (ie 120 cold => 80 warm)

    # Generated from packet 118/119
    buff = bulk2(dev, "\x0E\x00", target=0x20)
    validate_read(
            "\x3A\x00\x90\x32\xA7\x02\x2A\x86\x01\x95\x3C\x36\x90\x00\x1F"
            "\x00\x01\x00\xD6\x05\x01\x00\x72\x24\x22\x39\x00\x00\x00\x00\x27"
            "\x1F",
            buff, "packet 120/121")
    sn = buff[6:8]
    print 'S/N: %s' % binascii.hexlify(sn)
    
    # Generated from packet 122/123
    buff = bulk2(dev, "\x14\x38\x25\x00\x00\x04\x00\x90\x32\x90\x00\xA7\x02\x1F\x00\x14"
              "\x40\x25\x00\x00\x01\x00\x3C\x36\x0E\x01", target=0x20)
    validate_read("\x14\x00\x54\x41\x38\x34\x56\x4C\x56\x5F\x46\x58\x34\x00\x00"
              "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x3E"
              "\x2C", buff, "packet 124/125")
    
    # Generated from packet 126/127
    gpio_read(dev)
    
    # Generated from packet 130/131
    gpio_read(dev)
    
    # Generated from packet 134/135
    sm_read(dev)
    
    # Generated from packet 138/139
    buff = bulk2(dev, "\x01", target=0x85)
    # NOTE:: req max 512 but got 136
    validate_readv((
              "\x84\xA4\x06\x02\x00\x26\x00\x43\x00\xC0\x03\x00\x08\x10\x24"
              "\x00\x00\x30\x00\x80\x00\x00\x00\x00\x00\xC0\x00\x00\x00\x09\x00"
              "\x08\x00\xFF\x00\xC4\x1E\x00\x00\xCC\x1E\x00\x00\xB4\x46\x00\x00"
              "\xD0\x1E\x00\x00\xC0\x1E\x01\x00\xB0\x1E\x01\x00\x00\x00\x30\x55"
              "\x01\x00\x00\x00\x00\x00\x02\x00\x80\x01\xD0\x01\x02\x00\x01\x00"
              "\x00\x00\x56\x10\x00\x00\xA0\x25\x00\x00\x84\x25\x00\x00\x00\x00"
              "\x01\x00\x7C\x25\x00\x00\x7E\x25\x00\x00\x80\x25\x00\x00\x74\x46"
              "\x00\x00\x38\x11\x00\x00\x3C\x11\x00\x00\x40\x11\x00\x00\x44\x11"
              "\x00\x00\xC0\x1E\x00\x00",
              
              # warm
              "\x84\xA4\x06\x02\x00\x26\x00\x43\x00\xC0\x03\x00\x08\x10\x24"
              "\x00\x00\x30\x00\x83\x00\x30\x01\x09\x00\xC0\x00\x00\x00\x09\x00"
              "\x08\x00\xFF\x00\xC4\x1E\x00\x00\xCC\x1E\x00\x00\xB4\x46\x00\x00"
              "\xD0\x1E\x00\x00\xC0\x1E\x01\x00\xB0\x1E\x01\x00\x00\x00\x30\x55"
              "\x01\x00\x00\x00\x00\x00\x02\x00\x80\x01\xD0\x01\x02\x00\x01\x00"
              "\x00\x00\x56\x10\x00\x00\xA0\x25\x00\x00\x84\x25\x00\x00\x00\x00"
              "\x01\x00\x7C\x25\x00\x00\x7E\x25\x00\x00\x80\x25\x00\x00\x74\x46"
              "\x00\x00\x38\x11\x00\x00\x3C\x11\x00\x00\x40\x11\x00\x00\x44\x11"
              "\x00\x00\xC0\x1E\x00\x00",
              
              # glitch recover
              "\x84\xA4\x06\x02\x00\x26\x00\x43\x00\xC0\x03\x00\x08\x10\x24"
              "\x00\x00\x30\x00\x83\x00\x30\x01\x09\x00\xC0\x00\x00\x00\x09\x00"
              "\x08\x00\xFF\x00\xC4\x1E\x00\x00\xCC\x1E\x00\x00\xB4\x46\x00\x00"
              "\xD0\x1E\x00\x00\xC0\x1E\x01\x00\xB0\x1E\x01\x00\x00\x00\x30\x55"
              "\x01\x00\x00\x00\x00\x00\x02\x00\x80\x01\xD0\x01\x02\x00\x01\x00"
              "\x00\x00\x56\x10\x00\x00\xA0\x25\x00\x00\x84\x25\x00\x00\x00\x00"
              "\x01\x00\x7C\x25\x00\x00\x7E\x25\x00\x00\x80\x25\x00\x00\x74\x46"
              "\x00\x00\x38\x11\x00\x00\x3C\x11\x00\x00\x40\x11\x00\x00\x44\x11"
              "\x00\x00\xC0\x1E\x00\x00",
              
              # after ps
            "\x84\xA4\x06\x02\x00\x26\x00\x43\x00\xC0\x03\x00\x08\x10\x24\x00" \
            "\x00\x30\x00\x84\x00\x50\x01\x09\x00\xC0\x00\x00\x00\x09\x00\x08" \
            "\x00\xFF\x00\xC4\x1E\x00\x00\xCC\x1E\x00\x00\xB4\x46\x00\x00\xD0" \
            "\x1E\x00\x00\xC0\x1E\x01\x00\xB0\x1E\x01\x00\x00\x00\x30\x55\x01" \
            "\x00\x00\x00\x00\x00\x02\x00\x80\x01\xD0\x01\x02\x00\x01\x00\x00" \
            "\x00\x56\x10\x00\x00\xA0\x25\x00\x00\x84\x25\x00\x00\x00\x00\x01" \
            "\x00\x7C\x25\x00\x00\x7E\x25\x00\x00\x80\x25\x00\x00\x74\x46\x00" \
            "\x00\x38\x11\x00\x00\x3C\x11\x00\x00\x40\x11\x00\x00\x44\x11\x00" \
            "\x00\xC0\x1E\x00\x00",

              r01_glitches[1],
              ), buff, "packet 140/141")
    # Generated from packet 142/143
    bulkWrite(0x02, "\x43\x19\x00\x00\x00")

    # Generated from packet 144/145
    bulkWrite(0x02, "\x20\x01\x00\x0C\x04")

    # Generated from packet 146/147
    bulkWrite(0x02, "\x41\x00\x00")

    # Generated from packet 148/149
    buff = bulk2(dev, "\x10\x80\x02", target=6)
    validate_read("\x80\x00\x00\x00\x09\x00", buff, "packet 150/151")

    # Generated from packet 152/153
    buff = bulk2(dev, "\x45\x01\x00\x00\x31\x00\x06", target=0x64)
    validate_read("\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
              "\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
              "\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
              "\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
              "\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
              "\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
              "\xFF\xFF\xFF\xFF\xFF", buff, "packet 154/155")

    # Generated from packet 156/157
    buff = bulk2(dev, "\x49", target=2)
    validate_read("\x0F\x00", buff, "packet 158/159")

    # Generated from packet 160/161
    gpio_read(dev)


    # Generated from packet 164/165
    gpio_read(dev)


    # Generated from packet 168/169
    sm_read(dev)

    # Generated from packet 172/173
    bulkWrite(0x02, "\x3B\x0C\x22\x00\xC0\x30\x00\x3B\x0E\x22\x00\xC0\x00\x00\x3B\x1A"
              "\x22\x00\xC0\x18\x00")

    # Generated from packet 174/175
    buff = bulk2(dev, "\x4A\x03\x00\x00\x00", target=2)
    validate_read("\x03\x00", buff, "packet 176/177")

    # Generated from packet 178/179
    bulkWrite(0x02, "\x4C\x00\x02")

    # Generated from packet 180/181
    # None (0xB2)
    controlWrite(0x40, 0xB2, 0x0000, 0x0000, "")

    # Generated from packet 182/183
    bulkWrite(0x02, "\x50\x45\x00\x00\x00")

    # Generated from packet 184/185
    # FIXME: size field unexpected
    buff = bulk2(dev, "\xE9\x03\x00\x00\x00\x90\x00\x00\xE9\x03\x00\x00\x00\x90\x01\x10"
              "\xE9\x03\x00\x00\x00\x90\x00\x00\xE9\x03\x00\x00\x00\x90\x01\x80"
              "\xE9\x02\x00\x00\x00\x90\x00\xE9\x04\x00\x00\x00\x00\x00\x00\x00"
              "\xE9\x03\x00\x00\x00\x90\x00\x00\x66\xB9\x00\x00\xB2\x00\xFB\xFF"
              "\x25\x44\x11\x00\x00",
              target=2, truncate=True)
    validate_read("\x80\x00", buff, "packet 186/187")

    # Generated from packet 188/189
    buff = bulk2(dev, "\x02", target=6, truncate=True)
    validate_read("\x81\x00\x50\x00\x09\x00", buff, "packet 190/191")

    # Generated from packet 192/193
    bulkWrite(0x02, "\x50\xC0\x00\x00\x00")
    
    # Generated from packet 194/195
    # FIXME: size field unexpected
    buff = bulk2(dev, "\x66\xB8\x01\x2D\x81\xE3\xFF\xFF\x00\x00\x66\xBB\x18\x00\x66\xC7"
              "\x05\x30\x40\x00\xC0\xF0\xFF\x89\xD9\xC1\xE1\x02\x66\xC7\x81\x02"
              "\x00\x00\x00\xF0\xFF\x66\x03\x05\xE4\x46\x00\x00\x66\x89\x05\x90"
              "\x40\x00\xC0\x89\xDA\x81\xCA\x00\x80\x00\x00\x66\x89\x15\x50\x40"
              "\x00\xC0\xC6\x05\x14\x22\x00\xC0\x7B\x81\xCA\x00\x40\x00\x00\x66"
              "\x89\x15\x50\x40\x00\xC0\x89\xD9\x66\xC1\xE1\x02\x66\x89\x81\x00"
              "\x00\x00\x00\x66\x2B\x05\xE4\x46\x00\x00\xC6\x05\x14\x22\x00\xC0"
              "\xBB\x81\xCB\x00\x80\x00\x00\x66\x89\x1D\x50\x40\x00\xC0\x89\xC2"
              "\x81\xE2\x07\x00\x00\x00\x03\xD2\x81\xCA\x01\x00\x00\x00\x89\xD9"
              "\x81\xE1\x03\x00\x00\x00\xD3\xE2\xD3\xE2\xD3\xE2\xD3\xE2\xD3\xE2"
              "\xC1\xE2\x0A\x89\xD9\x81\xE1\xFC\x03\x00\x00\x09\xCA\x88\x82\x00"
              "\x00\x00\x40\x66\xB9\x00\x00\xB2\x00\xFB\xFF\x25\x44\x11\x00\x00",
              target=2, truncate=True)
    validate_read("\x81\x00", buff, "packet 196/197")

    # Generated from packet 198/199
    buff = bulk2(dev, "\x02", target=6, truncate=True)
    validate_read("\x82\x00\x10\x01\x09\x00", buff, "packet 200/201")

    if glitch_154:
        buff = bulk2(dev, "\x08\x20\x09\x20\x0A\x20\x0B\x20\x57\x81\x00\x0C\x04\x30",
                    target=2, truncate=True)
        validate_read("\x04\x00", buff, "packet 204/205")
    else:
        # Think this clears the red light
        # Generated from packet 202/203
        buff = bulk2(dev,
                  "\x04\x72\x05\x73\x06\x2E\x07\x70\x08\x75\x09\x73\x0A\x68\x0B\x28"
                  "\x57\x81\x00\x0C\x04\x30",
                  target=2, truncate=True)
        validate_read("\x04\x00", buff, "packet 204/205")
    
    # Generated from packet 206/207
    buff = bulk2(dev,
              "\x3B\x0C\x22\x00\xC0\x30\x00\x3B\x0E\x22\x00\xC0\x00\x00\x3B\x1A"
              "\x22\x00\xC0\x18\x00\x0E\x01",
              target=0x20, truncate=True)
    validate_read(
              "\x14\x00\x54\x41\x38\x34\x56\x4C\x56\x5F\x46\x58\x34\x00\x00"
              "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x3E"
              "\x2C", buff, "packet 208/209")

    # Generated from packet 210/211
    gpio_read(dev)


    # Generated from packet 214/215
    gpio_read(dev)


    # Generated from packet 218/219
    sm_read(dev)
    
    # Generated from packet 222/223
    bulkWrite(0x02, "\x48\x00\x20\x00\x00\x50\x12\x00\x00\x00")
    
    # Generated from packet 224/225
    buff = bulk2(dev, "\x00\x00\x00\x00\x04\x00\x08\x00\x0C\x00\x10\x00\x14\x00\x18\x00"
              "\x1C\x00", target=2, truncate=True)
    validate_read("\x82\x00", buff, "packet 226/227")

    # Generated from packet 228/229
    buff = bulk2(dev, "\x02", target=6, truncate=True)
    validate_read("\x83\x00\x30\x01\x09\x00", buff, "packet 230/231")

    # Generated from packet 232/233
    buff = bulk2(dev,
              "\x1D\x10\x01\x09\x00\x00\x00\x15\x60\x00\x00\x00\x00\x00\x00\x00"
              "\x00\x00\x00\x00\x00\x00\x1C\x00\x00\x48\x00\x12\xAA",
              target=1, truncate=True)
    validate_read("\xAB", buff, "packet 234/235")

    # Generated from packet 236/237
    gpio_read(dev)

SM_FMT = '<H12s18s'
SM = namedtuple('sm', ('unk0', 'name', 'unk12'))

def sm_read(dev):
    buff = bulk2(dev, "\x0E\x02", target=0x20, truncate=True)
    validate_readv((
              "\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
              "\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
              "\xFF",
              
              # Socket module
              # 00000000  11 00 53 4D 34 38 44 00  00 00 00 00 00 00 5D F4  |..SM48D.......].|
              # 00000010  39 FF 00 00 00 00 00 00  00 00 00 00 00 00 62 6C  |9.............bl|
              "\x11\x00\x53\x4D\x34\x38\x44\x00\x00\x00\x00\x00\x00\x00\x5D\xF4" \
              "\x39\xFF\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x62\x6C",
              ),
              buff, "packet 136/137")
    # Don't throw exception on no SM for now?)
    # since it will break other code
    if buff == '\xFF' * 32:
        return None
    
    return SM(*struct.unpack(SM_FMT, buff))

def sm_info(dev):
    # Generated from packet 3/4
    gpio_read(dev)
    
    # Generated from packet 7/8
    gpio_read(dev)

    # Generated from packet 11/12
    buff = bulk2(dev, "\x22\x02\x22\x00\x23\x00\x06", target=4, truncate=True)
    validate_read("\xAA\x55\x33\xA2", buff, "packet 13/14")
    
    # Generated from packet 15/16
    buff = bulk2(dev, "\x22\x02\x24\x00\x25\x00\x06", target=4, truncate=True)
    validate_read("\x01\x00\x00\x00", buff, "packet 17/18")
    
    # Generated from packet 19/20
    sm_read(dev)
    
    # Generated from packet 23/24
    buff = bulk2(dev, "\x49", target=2, truncate=True)
    validate_read("\x0F\x00", buff, "packet 25/26")
    
    # Generated from packet 27/28
    sm = sm_read(dev)
    print 'Name: %s' % sm.name
    
    # Generated from packet 31/32
    buff = bulk2(dev, "\x22\x02\x10\x00\x1F\x00\x06", target=0x20, truncate=True)
    '''
    validate_read("\x32\x01\x00\x00\x93\x00\x00\x00\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
            "\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
            "\xFF", buff, "packet 33/34")
    '''
    ins_all, _unk1, ins_last, _unk2, _res = struct.unpack('<HHHH24s', buff)
    print 'Insertions (all): %d' % ins_all
    print 'Insertions (since last): %d' % ins_last
    
    # Generated from packet 35/36
    buff = bulk2(dev, "\x22\x02\x10\x00\x13\x00\x06", target=8, truncate=True)
    validate_read("\x32\x01\x00\x00\x93\x00\x00\x00", buff, "packet 37/38")
