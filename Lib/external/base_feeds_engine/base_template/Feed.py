p = parent()
pp = p.par


class Feed:
	"""
	Main description
	"""
	def __init__(self, ownerComp):
		self.ownerComp = ownerComp
		
	def SetType(self, type):
		if type == 'output':
			pass
		elif type == 'quarter':
			pass
		elif type == 'canvas':
			pass
		else:
			pass
		
		return
		
	def ResetBlends(self):
		pp.Topblendwidth = 100
		pp.Topblendgamma = 0.5
		pp.Bottomblendwidth = 100
		pp.Bottomblendgamma = 0
		pp.Leftblendwidth = 100
		pp.Leftblendgamma = 0.5
		pp.Rightblendwidth = 100
		pp.Rightblendgamma = 0.5
		return
		
	def ResetCornerPin(self):
		pp.Cornerpinbottomleftx = 0
		pp.Cornerpinbottomlefty = 0
		pp.Cornerpinbottomrightx = 1
		pp.Cornerpinbottomrighty = 0
		pp.Cornerpintopleftx = 0
		pp.Cornerpintoplefty = 1
		pp.Cornerpintoprightx = 1
		pp.Cornerpintoprighty = 1
		return
	
	def ResetTransform(self):
		pp.Translatex = 0
		pp.Translatey = 0
		pp.Rotate = 0
		pp.Scalex = 1
		pp.Scaley = 1
		pp.Uniformscale = 1
		pp.Pivotx = 0.5
		pp.Pivoty = 0.5
		
		return