

'''
[0-3] - length in bytes. [l0 l1 l2]
'''

def steno_data_length(length_value):

    length2 = length_value & 0xFF
    length1 = (length_value >> 8) & 0xFF
    length0 = (length_value >> 16) & 0xFF

    return (length0, length1, length2)

def unsteno_data_length(medium):
    length = 0

    length |= medium[0]
    length = length << 8
    length |= medium[1]
    length = length << 8
    length |= medium[2]

    return length


def steno_byte_array(medium, data):

    if len(medium) < 3 + len(data)*3:
        raise Exception("Medium size too small")

    (m0,m1,m2) = steno_data_length(len(data))

    medium[0] = m0
    medium[1] = m1
    medium[2] = m2

    # steno data
    i = 3
    for d in data:
        (m0,m1,m2) = steno(medium[i], medium[i+1], medium[i+2], d)
        medium[i] = m0
        medium[i+1] = m1
        medium[i+2] = m2

        i += 3

    return medium


def unsteno_byte_array(medium):
    
    length = unsteno_data_length(medium)
    data = bytearray(length)

    d = 0
    for i in range(3, 3*(length+1), 3):
        m0 = medium[i]
        m1 = medium[i+1]
        m2 = medium[i+2]

        data[d] = unsteno(m0, m1, m2)
        d += 1
    
    return data

def steno(b, g, r, value):
    b = (b & 0xF8) | (value & 7) # 3 bit 11111000
    g = (g & 0xFC) | ((value>>3) & 3) # 2 bit 11111100
    r = (r & 0xF8) | ((value>>5) & 7) # 3 bit 11111000

    return (b, g, r)
    
def unsteno(b, g, r):
    v = (r & 7) << 5
    v = v | ((g & 3) << 3)
    v = v | (b & 7)
    
    return v
