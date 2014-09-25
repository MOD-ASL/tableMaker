from TableMaker import *

# module name map:
names = {'center':0,
    'front-center':1,
    'front-left':2,
    'front-right':3,
    'back-center':4,
    'back-right':5,
    'back-left':6
}

# define module groups:
wheel_group = ['front-center', 'front-left', 'front-right', 'back-center', 'back-left', 'back-right']

#ss = set_module_state # for convenience

def stand_up():
    ''' Assume neutral standing position. '''
    return parallel( [
        sms( 'front-left',   [0, 0, 0, 0.7]  ),
        sms( 'front-right',  [0, 0, 0, 0.7]  ),
        sms( 'front-center', [0, 0, 0, 0.5]  ),
        sms( 'center',       [0, 0, 0, -0.5] ),
        sms( 'back-center',  [0, 0, 0, 0.7]  ),
        sms( 'back-right',  [0, 0, 0, 0.7]  ),
        sms( 'back-left',    [0, 0, 0, 0.7]  ),
    ])

def drive_forward(angle):
    ''' Drives the wheels forward, to the specified angle. '''
    return parallel([ sms( module, {'left':angle,'right':angle} ) for module in wheel_group ])

def turn(angle):
    ''' Makes the center joints turn by specified angle. '''
    return parallel([ sms( 'back-center', {'front':angle} ),
                      sms( 'center', {'front':-angle} ),
     ])

def sms(module_name, positions):
    ''' Sets module state. Positions is a dict or a list. '''
    if isinstance(positions, dict):
        p = ['i', 'i', 'i', 'i']
        for i,key in enumerate(['front', 'left', 'right', 'center']):
            # map specified joints into table command; leave as 'i' (no change) if not used.
            if positions.has_key(key):
                p[i] = positions[key]
            #p = [ positions['front'], positions['left'], positions['right'], positions['center'] ]
    elif isinstance(positions, list):
        # for conciseness, you can also specify as a list.
        p = positions
    else:
        assert(False)
    out = ''
    out += 'Module_' + str(names[module_name])
    for i in xrange(0,4):
        if p[i] is 'i':
            out += ' i'
        else:
            out += ' p' + str(p[i])
    #out += ' p' + str(p[0]) + ' p' + str(p[1]) + ' p' + str(p[2]) + ' p' + str(p[3])
    return out

c = CommandBlock()
r = series([ stand_up(),
        drive_forward(3),
        turn(.3),
        drive_forward(12),
        turn(-0.3),
        drive_forward(21),
        turn(0),
        drive_forward(30)
    ])
c.stitch( r )
print c
c.write('car_auto.gait')