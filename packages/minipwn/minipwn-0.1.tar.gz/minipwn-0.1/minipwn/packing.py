import struct

def p8(x, endianness='little', sign=False):
    if x >= 2**8:
        raise ValueError('value too big')

    match endianness, sign:
        case 'little', False:
            return struct.pack('<B', x)
        case 'big', False:
            return struct.pack('>B', x)
        case 'little', True:
            return struct.pack('<b', x)
        case 'big', True:
            return struct.pack('>b', x)
        case _:
            raise ValueError('Unknown endianness')
        
def p16(x, endianness='little', sign=False):
    if x >= 2**16:
        raise ValueError('value too big')

    match endianness, sign:
        case 'little', False:
            return struct.pack('<H', x)
        case 'big', False:
            return struct.pack('>H', x)
        case 'little', True:
            return struct.pack('<h', x)
        case 'big', True:
            return struct.pack('>h', x)
        case _:
            raise ValueError('Unknown endianness')
        
def p32(x, endianness='little', sign=False):
    if x >= 2**32:
        raise ValueError('value too big')

    match endianness, sign:
        case 'little', False:
            return struct.pack('<I', x)
        case 'big', False:
            return struct.pack('>I', x)
        case 'little', True:
            return struct.pack('<i', x)
        case 'big', True:
            return struct.pack('>i', x)
        case _:
            raise ValueError('Unknown endianness')
        
def p64(x, endianness='little', sign=False):
    if x >= 2**64:
        raise ValueError('value too big')

    match endianness, sign:
        case 'little', False:
            return struct.pack('<Q', x)
        case 'big', False:
            return struct.pack('>Q', x)
        case 'little', True:
            return struct.pack('<q', x)
        case 'big', True:
            return struct.pack('>q', x)
        case _:
            raise ValueError('Unknown endianness')
        
def u8(x, endianness='little', sign=False):
    match endianness, sign:
        case 'little', False:
            return struct.unpack('<B', x)[0]
        case 'big', False:
            return struct.unpack('>B', x)[0]
        case 'little', True:
            return struct.unpack('<b', x)[0]
        case 'big', True:
            return struct.unpack('>b', x)[0]
        case _:
            raise ValueError('Unknown endianness or sign')

def u16(x, endianness='little', sign=False):
    match endianness, sign:
        case 'little', False:
            return struct.unpack('<H', x)[0]
        case 'big', False:
            return struct.unpack('>H', x)[0]
        case 'little', True:
            return struct.unpack('<h', x)[0]
        case 'big', True:
            return struct.unpack('>h', x)[0]
        case _:
            raise ValueError('Unknown endianness or sign')

def u32(x, endianness='little', sign=False):
    match endianness, sign:
        case 'little', False:
            return struct.unpack('<I', x)[0]
        case 'big', False:
            return struct.unpack('>I', x)[0]
        case 'little', True:
            return struct.unpack('<i', x)[0]
        case 'big', True:
            return struct.unpack('>i', x)[0]
        case _:
            raise ValueError('Unknown endianness or sign')
        
def u64(x, endianness='little', sign=False):
    match endianness, sign:
        case 'little', False:
            return struct.unpack('<Q', x)[0]
        case 'big', False:
            return struct.unpack('>Q', x)[0]
        case 'little', True:
            return struct.unpack('<q', x)[0]
        case 'big', True:
            return struct.unpack('>q', x)[0]
        case _:
            raise ValueError('Unknown endianness or sign')