from TDStoreTools import StorageManager
import TDFunctions as TDF

p = parent()
pp = p.par
screenTemplate = op('geo_template')
toxDir = "stage/screens/"

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
		newScreen.tags.add('projectObject')
		externalPath = op.PROJECT.ProjectDir() + toxDir + newScreen.name + ".tox"
		newScreen.par.externaltox = externalPath

		op.UTILS.LayoutCOMPs(p, "screen", 200)
		op.UTILS.SetStatus("info","Created new screen")
		return
		
	def LoadFromProject(self, projectName):
		p.DeleteAll()
		toxFolder = op.PROJECT.ProjectDir() + toxDir
		toxes = op.UTILS.GetFilesFromFolder(toxFolder)
		
		for nTox in toxes:
			try:
				newTox = p.loadTox(toxFolder + nTox)
				newTox.par.enableexternaltox = True
				newTox.par.externaltox = toxFolder + nTox
			except:
				pass
				
		op.UTILS.LayoutCOMPs(p, "screen", 200)
		return
		
	def Delete(self, screenid):
		compOP = op('screen_'+screenid)
		op.UTILS.DeleteExternalTox(compOP.par.externaltox.eval())
		compOP.destroy()
		op.UTILS.SetStatus("info","Deleted Screen: " + screenid)
		op.UTILS.LayoutCOMPs(p, "screen", 200)
		return
		
	def DeleteAll(self):
		op.UTILS.DeleteAllCOMPs(p, "screen")
		return
		
	def GetInfoTable(self):
		return op('null_get_screens')
		
	def GetNumberOfScreens(self):
		return p.GetInfoTable().numRows-1