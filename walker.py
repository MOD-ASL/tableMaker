from TableMaker import *
from math import pi
class Walker:

	def __init__(self):
		self.names = {'center-front':0,
		    'center-back':7,
		    'front-left-hip':1,
		    'front-left-knee':2,
		    'front-left-ankle':3,
		    'front-right-hip':4,
		    'front-right-knee':5,
		    'front-right-ankle':6,
		    'back-left-hip':8,
		    'back-left-knee':9,
		    'back-left-ankle':10,
		    'back-right-hip':11,
		    'back-right-knee':12,
		    'back-right-ankle':13,
		}

	def stand_up(self):
		''' Makes walker assume a neutral standing position '''
		hipRot = pi/3
		moveHipsOut = parallel([ self.sms('front-left-hip',{'center':hipRot}),
								self.sms('front-right-hip',{'center':-hipRot}),
								self.sms('back-left-hip',{'center':-hipRot}),
								self.sms('back-right-hip',{'center':hipRot}),
			])
		rotateLegs = parallel([ self.sms('front-left-hip',{'front':pi/2}),
								self.sms('front-right-knee',{'front':pi/2}),
								self.sms('back-left-hip',{'front':pi/2}),
								self.sms('back-right-knee',{'front':pi/2}),
			])
		pushBodyUp = parallel([ self.sms(knee, {'center':-pi/3}) for knee in
			['front-left-knee', 'front-right-knee', 'back-left-knee', 'back-right-knee'] ])
		return series([ moveHipsOut, rotateLegs, pushBodyUp ])

	def walk_cycle(self, num_steps):
		''' Runs a walk cycle for num_steps steps. '''
		#return series([ self.step_back_left(),
		#	])
		return self.step_back_left()
		
	def step_back_left(self):
		''' Takes a step forward with the back-left leg '''	
		liftOff = self.sms('back-left-knee',{'center': 0})
		pause = 'Module_0 p0 p0 p0 [1000]'
		swing = self.sms('back-left-hip',{'center': 0})
		touchdown = self.sms('back-left-knee',{'center': -pi/3})
		return series([ liftOff , pause, swing, touchdown ])#, rotateHip, touchDown ])

	def walk(self):
		''' Makes the walker walk. '''
		c = CommandBlock()
		#c.stitch( series([ self.stand_up(), self.walk_cycle(1) ]) )
		relativeBlock = series([ self.stand_up(), 'Module_0 p0 p0 p0 p0 [1000]', self.walk_cycle(1) ])
		c.stitch( relativeBlock )
		print c
		c.write('walker_auto.gait')

	def sms(self, module_name, positions):
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
	    out += 'Module_' + str(self.names[module_name])
	    for i in xrange(0,4):
	        if p[i] is 'i':
	            out += ' i'
	        else:
	            out += ' p' + str(p[i])
	    #out += ' p' + str(p[0]) + ' p' + str(p[1]) + ' p' + str(p[2]) + ' p' + str(p[3])
	    return out

if __name__=='__main__':
	w = Walker()
	w.walk()