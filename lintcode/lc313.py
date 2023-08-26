a = b'\x12\x34\x56'

print('0x' + ''.join(hex(x)[2:] for x in a))
