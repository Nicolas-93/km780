import usb.core
import usb.util as util
from usb.legacy import REQ_SET_CONFIGURATION
from usb.core import Device
from sys import exit
from enum import Enum, IntEnum
from dataclasses import dataclass
from keys import Key
from typing import List

KM_START_PACKET = 0x07

"""class CommandMethod(IntEnum):
    CurrentProfile     = 1 << 0
    ProfileInformation = 1 << 1
    UNKNOWN1           = 1 << 2
    LEDEffectDatabase  = 1 << 3
    LEDMatrixDatabase  = CommandMethod.LEDEffectDatabase | CommandMethod.CurrentProfile
    UNKNOWN2           = 1 << 4
    UNKNOWN3           = 1 << 5
    UNKNOWN4           = 1 << 6"""

class KMCommand(IntEnum):
    SetCurrentProfile     = 0x01
    GetCurrentProfile     = 0x81

    SetProfileInformation = 0x02
    GetProfileInformation = 0x82
    
    SetLEDEffectDatabase  = 0x08
    GetLEDEffectDatabase  = 0x88
    
    SetLEDMatrixDatabase  = 0x09
    GetLEDMatrixDatabase  = 0x89

class Color(Enum):
    RED   = 0x01
    GREEN = 0x02
    BLUE  = 0x03

class ColorMask(list):
    def __init__(self, color: Color):
        self.color = color
        super().__init__([0] * Key.LEN)

class ColorMap:

    red: ColorMask
    green: ColorMask
    blue: ColorMask

    def __init__(self):
        self.red   = ColorMask(Color.RED)
        self.green = ColorMask(Color.GREEN)
        self.blue  = ColorMask(Color.BLUE)

    def set_color(self, key: Key, red: int, green: int, blue: int):
        if not all(0 <= col <= 255 for col in (red, green, blue)):
            raise ValueError(f"Colors must be between 0 and 255, got {(red, green, blue)}")

        key = key.value
        self.red[key]   = red
        self.green[key] = green
        self.blue[key]  = blue

class Keyboard:
    VENDOR_ID     = 0x28da
    PRODUCT_ID    = 0x1101
    PACKET_LENGTH = 264
    IN_ENDPOINT   = 0x83 # Third endpoint, Direction : IN

    dev: Device
    
    def __init__(self):
        self.mode = 2
        self.in_interface = None
        self.color_map = ColorMap()

    def attach(self):
        # Find the keyboard
        self.dev = usb.core.find(idVendor=self.VENDOR_ID, idProduct=self.PRODUCT_ID)

        if self.dev is None:
            raise ValueError('Device not found')

        print(f"Found: {usb.util.get_string(self.dev, self.dev.iProduct)}")
        print(self.dev)
        print("Detaching kernel driver...")

        # self.dev.detach_kernel_driver(2)
        # self.dev.detach_kernel_driver(1)
        usb.util.claim_interface(self.dev, 2) # In interface (endpoint=0x83)
        # usb.util.claim_interface(self.dev, 1) # Out interface ()

        self.in_endpoint = util.find_descriptor(
            self.dev[0][2,0],
            custom_match=lambda e: e.bEndpointAddress == Keyboard.IN_ENDPOINT
        )
        assert self.in_endpoint is not None

    def close(self):
        print('bye')
        usb.util.release_interface(self.dev, 2)
        # usb.util.release_interface(self.dev, 1)
        # self.dev.attach_kernel_driver(2)
        # self.dev.attach_kernel_driver(1)
    
        # usb.util.dispose_resources(self.dev)
        self.dev.reset()

    def send_packet(self, packet):
        assert len(packet) == Keyboard.PACKET_LENGTH
        bmRequestType = util.build_request_type(
            util.ENDPOINT_OUT,
            util.CTRL_TYPE_CLASS,
            util.CTRL_RECIPIENT_INTERFACE
        )
        bRequest = REQ_SET_CONFIGURATION
        wValue = 0x0307
        wIndex = 1
        print(f"Packet : {packet}")
        r = self.dev.ctrl_transfer(
            bmRequestType=bmRequestType,
            bRequest=bRequest,
            wValue=wValue,
            wIndex=wIndex,
            data_or_wLength=packet
        )
        print("r", r)
        resp = self.in_endpoint.read(1024) # 64
        print("Response :", resp)

    def set_mode(self, num):
        if not 1 <= num <= 3:
            raise ValueError("KM780 only provide 3 modes (M1, M2, M3)")
        self.mode = num

    def _create_color_packet(self, mask: ColorMask):
        packet = [KM_START_PACKET, KMCommand.SetLEDMatrixDatabase.value, self.mode, mask.color.value] + 4 * [0x0]
        packet.extend(mask)
        return self._pad_packet(packet)

    @staticmethod
    def _pad_packet(packet):
        packet.extend([0] * (Keyboard.PACKET_LENGTH - len(packet)))
        return packet
    
    def set_color(self, key: Key, red: int, green: int, blue: int):
        self.color_map.set_color(key, red, green, blue)

    def apply_colors(self):
        self._begin()
        self.send_packet(self._create_color_packet(self.color_map.red))
        self.send_packet(self._create_color_packet(self.color_map.green))
        self.send_packet(self._create_color_packet(self.color_map.blue))
    
    def _begin(self):
        self.send_packet(self._pad_packet([KM_START_PACKET, 0x0d, 0x00]))

    def commit(self):
        packet = [KM_START_PACKET, 0x0d, 0x01]

if __name__ == "__main__":
    from keys import Key
    kb = Keyboard()
    # kb.attach()

    kb.set_color(Key.A, 0xff, 0xff, 0xff)
    kb.set_color(Key.Z, 0xff, 0xff, 0xff)
    kb.set_color(Key.E, 0xff, 0xff, 0xff)
    kb.set_color(Key.R, 0xff, 0xff, 0xff)

    kb.apply_colors()
    # kb.commit()
    # kb.close()
