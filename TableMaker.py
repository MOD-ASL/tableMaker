# TableMaker.py
# Tarik Tosun

from CommandBlock import CommandBlock
from RelativeBlock import RelativeBlock

def series(blocks):
    b = RelativeBlock()
    b.type = 'series'
    b.block_list = blocks
    return b

def parallel(blocks):
    b = RelativeBlock()
    b.type = 'parallel'
    b.block_list = blocks
    return b

# def sms(module_name, positions):
#     ''' Sets module state. Positions is a dict or a list. '''
#     if isinstance(positions, dict):
#         p = ['i', 'i', 'i', 'i']
#         for i,key in enumerate(['front', 'left', 'right', 'center']):
#             # map specified joints into table command; leave as 'i' (no change) if not used.
#             if positions.has_key(key):
#                 p[i] = positions[key]
#             #p = [ positions['front'], positions['left'], positions['right'], positions['center'] ]
#     elif isinstance(positions, list):
#         # for conciseness, you can also specify as a list.
#         p = positions
#     else:
#         assert(False)
#     out = ''
#     out += 'Module_' + str(names[module_name])
#     for i in xrange(0,4):
#         if p[i] is 'i':
#             out += ' i'
#         else:
#             out += ' p' + str(p[i])
#     #out += ' p' + str(p[0]) + ' p' + str(p[1]) + ' p' + str(p[2]) + ' p' + str(p[3])
#     return out