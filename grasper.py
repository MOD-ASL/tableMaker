from TableMaker import *
from math import pi
class Grasper:

	def __init__(self):
		self.names = {
		'center':0,
		'left-shoulder':4,
		'right-shoulder':1,
		'left-elbow':5,
		'right-elbow':2,
		'left-wrist':6,
		'right-wrist':3,
		}
		# Note: 'left' is defined by viewing the design from the font,
		# ie the grasper is able to grasp your head.

	def neutral_position(self):
		''' Moves the grasper from its start position to its neutral position,
		ready to move its arms parallel to the ground plane. '''
		return series([
			self.sms('center', {'left':pi/2}),
			self.sms('center', {'right':pi/2}),
			#'Module_1 p0 p0 p0 p0 [1500]',
			self.janky_pause(1500),
		])

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
		return parallel([
			self.sms('left-shoulder', {'center':shoulder_pos}),
			self.sms('right-shoulder', {'center':shoulder_pos}),
			self.sms('right-elbow', {'center':elbow_pos}),
			self.sms('left-elbow', {'center':elbow_pos}),
			self.sms('left-wrist', {'center':wrist_pos}),
			self.sms('right-wrist', {'center':wrist_pos}),
		])

	def janky_pause(self, time):
		''' A janky implementation of pausing for the requested number of milliseconds. '''
		return self.sms('center', {'left':pi/2, 'right':pi/2}) + ' [' + str(time) + ']'	

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
	g = Grasper()
	c = CommandBlock()
	r = series([g.neutral_position(), g.grasp_ready_position(), g.janky_pause(750), g.squeeze_together() ])
	c.stitch(r)
	print c
	c.write('grasper-auto.gait')