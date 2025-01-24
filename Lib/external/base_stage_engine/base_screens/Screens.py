from TDStoreTools import StorageManager
import TDFunctions as TDF
import uuid
import time

p = parent()
pp = p.par
screenTemplate = op('geo_template')

class Screens:

	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		
	def CreateScreen(self):
		# generate id for screen
		screenID = str(uuid.uuid1())
		screenID = screenID.replace('-','_')
		numScreens = parent().GetInfoTable().numRows-1
		createdTime = int(time.time())

		newScreen = p.copy(screenTemplate)
		newScreen.name = "screen_"+screenID
		newScreen.par.Id = screenID
		newScreen.par.Created = createdTime

		p.SetScreenPosition(newScreen,200)
		op.UTILS.SetStatus("info","Created new screen")
		return
		
	def SetScreenPosition(self, opToMove, yPos):
		# set pos based on how many screens we have
		screenOps = p.findChildren(name="screen_*", type=COMP)
		xPos = len(screenOps)*yPos
		opToMove.nodeX = xPos
		opToMove.nodeY = yPos
		return
		
	def DeleteScreen(self, screenid):
		op('screen_'+screenid).destroy()
		op.UTILS.SetStatus("info","Deleted Screen: " + screenid)
		return
		
	def DeleteAllScreens(self):
		opsToDelete = p.findChildren(name="screen_*", type=COMP)
		for delOp in opsToDelete:
			delOp.destroy()
		return
		
	def GetInfoTable(self):
		return op('null_get_screens')
		
	def GetNumberOfScreens(self):
		return p.GetInfoTable().numRows-1