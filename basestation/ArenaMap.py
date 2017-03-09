import re

class MazeLayout:

	def __init__(self, sizeX, sizeY, description):
		if (isinstance(sizeX, int) and isinstance(sizeY, int)):
			if (not description):
				raise NameError('Invalid arguments. Description is empty.')
			else:
				self.description = description
				self.sizeX = sizeX
				self.sizeY = sizeY
				self.noTargets = 0
				self.noBlockers = 0
				self.targets = dict()
				self.blockers = dict()
				self.valid = self.isValid()
		else:
			# invalid constructor
			raise NameError('Invalid arguments. should be ints')
			
	def isValid(self):
		preIndex = self.description.find('*#*#*#*#')
		if (preIndex > -1):
			# Preamblr valid
			# Find next '*' to determine number of targets
			targetStart = self.description.find('*#',8)
			
			# 0         1         2         3         4         5         6         7
			# 012345678901234567890123456789012345678901234567890123456789012345678901234
			# *#*#*#*#A0000B0000C0000D0000A0000B0000C0000*0000*0000*0000*0000*0000*0000*#
			
			self.noTargets = (targetStart - 8)/5
			# Should be integer
			if round(self.noTargets) != self.noTargets:
				raise NameError('Invalid target length')
		
			count = 0
			result = 0
			pos = 0
			# Find targets
			while result == re.match('([A-D])([0-9]{2})([0-9]{2})^$', self.description, pos):
				# Create empty dictionary
				cTarget = dict()
				cTarget['dir'] = result[0]
				cTarget['x'] = int(result[1])
				cTarget['y'] = int(result[2])
				self.targets[count] = cTarget
				count = count +1
				pos = pos + 5
				
			# Find blockers
			while result == re.match('\*([0-9]{2})([0-9]{2})^%', self.description, pos):
				cBlocker = dict()
				cBlocker['x'] = int(result[0])
				cBlocker['y'] = int(result[1])
				# Should come in pairs
				res2 = re.match('\*([0-9]{2})([0-9]{2})^%')
				if (res2 == None):
					raise NameError('Blockers should come in pairs.')
					
				# Calculate size
				cBlocker['dx'] = int(res2[0]) - cBlocker['x']
				cBlocker['dy'] = int(res2[1]) - cBlocker['y']
				self.blockers[count] = cBlocker;
				count = count +1
				pos = pos + 5
				
			if (self.description.find('*#', 8)):
				return True
			else:
				raise NameError('Invalid arena specification, missing post-amble.')			
			
		else:
			raise NameError('Invalid preamble.')
		
	def getNumberOfTargets(self):
		return self.targets.count()
		
	def getTargetX(self, idx):
		return self.targets[idx]['x']
		
	def getTargetY(self, idx):
		return self.targets[idx]['y']
		
	def getTargetDirection(self, idx):
		return self.targets[idx]['dir']
		
	def blockedAt(self, cx, cy):
		# Loop through targets
		for cBlock in self.blockers:
			x = cBlock['x']
			y = cBlock['y']
			xFin = cBlock['dx'] + x
			yFin = cBlock['dy'] + y
			if (cx >= x and cx <= xFin):
				if (cy >= y and cy <= yFin):
					return True
		# Not Blocked, return false
		return False
