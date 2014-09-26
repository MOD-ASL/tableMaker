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

		self.grasper_names = {
		'center':0,
		'left-shoulder':4,
		'right-shoulder':1,
		'left-elbow':5,
		'right-elbow':2,
		'left-wrist':6,
		'right-wrist':3,
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
		c.write('walker-auto.gait')
#----------------------------------------------------
# Grasping functions
	def become_grasper(self):
		''' Commands the walker to bend down and get its legs into the right position
		to act as a grasper. '''
		sms = lambda module_name, positions: self.sms(module_name, positions, self.grasper_names) 
		bend_down = parallel([ sms(joint, {'center':0}) for joint in ['left-elbow', 'right-elbow', 'left-wrist', 'right-wrist'] ])
		unrotate_legs = parallel([ sms(joint, {'front':0}) for joint in ['right-shoulder', 'left-elbow'] ])
		bend_middle = self.sms('center-back', {'center':pi/3})
		flattening_angle = pi/3
		make_body_flat = parallel([ self.sms('center-back', {'front':(pi/2-flattening_angle)}), self.sms('back-right-hip', {'front':pi/2+flattening_angle}) ])
		bend_back = self.sms('center-back',	 {'center':0})
		#pi/2+pi/3
		
		# note that make_body_flat uses self.sms (not sms), and bends by the same angle as the back knee joints to bring the body flat.

		return series([ bend_down, unrotate_legs, bend_middle])#, make_body_flat, bend_back ])

	def grasp_ready_position(self):
		''' Moves to the grasp-ready position. '''
		shoulder_pos = 1.2
		elbow_pos = 0.5
		wrist_pos = 1.3
		return self.set_arm_state(shoulder_pos,elbow_pos,wrist_pos)

	def squeeze_together(self):
		''' Squeezes together to grasp an object '''
		shoulder_pos = pi/2
		elbow_pos = 0.3 
		wrist_pos = pi/2 - elbow_pos
		return self.set_arm_state(shoulder_pos, elbow_pos, wrist_pos)

	def set_arm_state(self, shoulder_pos, elbow_pos, wrist_pos):
		''' Sets the state of both arms as specified. '''
		sms = lambda module_name, positions: self.sms(module_name, positions, self.grasper_names) 
		return parallel([
			sms('left-shoulder', {'center':-shoulder_pos}),
			sms('right-shoulder', {'center':shoulder_pos}),
			sms('right-elbow', {'center':elbow_pos}),
			sms('left-elbow', {'center':-elbow_pos}),
			sms('left-wrist', {'center':-wrist_pos}),
			sms('right-wrist', {'center':wrist_pos}),
		])

	def janky_pause(self, time):
		''' A janky implementation of pausing for the requested number of milliseconds. '''
		sms = lambda module_name, positions: self.sms(module_name, positions, self.grasper_names) 
		return sms('center', {'left':0, 'right':0}) + ' [' + str(time) + ']'	


#---------------------------------------------------
	def sms(self, module_name, positions, names = None):
	    ''' Sets module state. Positions is a dict or a list. '''
	    if names == None:
	    	names = self.names
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

if __name__=='__main__':
	w = Walker()
	c = CommandBlock()
	#r = series([ w.stand_up(), w.bend_down_in_front(), w.grasp_ready_position(), w.squeeze_together() ])
	#r = series([ w.become_grasper(), w.grasp_ready_position(), w.janky_pause(750), w.squeeze_together() ])
	r = series([ w.stand_up(), w.janky_pause(1000), w.become_grasper(), w.grasp_ready_position(), w.janky_pause(500), w.squeeze_together() ])
	c.stitch(r)
	print c
	c.write('walker-auto.gait')