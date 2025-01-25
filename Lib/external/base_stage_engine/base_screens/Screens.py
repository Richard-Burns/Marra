from TDStoreTools import StorageManager
import TDFunctions as TDF

p = parent()
pp = p.par
screenTemplate = op('geo_template')

class Screens:

	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		
	def Create(self):
		# generate id for screen
		screenID = op.UTILS.CreateID()
		numScreens = parent().GetInfoTable().numRows-1
		createdTime = op.UTILS.Timestamp()

		newScreen = p.copy(screenTemplate)
		newScreen.name = "screen_"+screenID
		newScreen.par.Id = screenID
		newScreen.par.Created = createdTime

		op.UTILS.LayoutCOMPs(p, "screen", 200)
		op.UTILS.SetStatus("info","Created new screen")
		return
		
	def Delete(self, screenid):
		op('screen_'+screenid).destroy()
		op.UTILS.SetStatus("info","Deleted Screen: " + screenid)
		op.UTILS.LayoutCOMPs(p, "screen", 200)
		return
		
	def GetInfoTable(self):
		return op('null_get_screens')
		
	def GetNumberOfScreens(self):
		return p.GetInfoTable().numRows-1