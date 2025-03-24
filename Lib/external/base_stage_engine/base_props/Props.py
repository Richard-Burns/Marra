from TDStoreTools import StorageManager
import TDFunctions as TDF

p = parent()
pp = p.par
propTemplate = op('geo_template')
toxDir = "stage/props/"

class Props:

	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		
	def Create(self):
		# generate id for screen
		propID = op.UTILS.CreateID()
		numProps = parent().GetInfoTable().numRows-1
		createdTime = op.UTILS.Timestamp()

		newProp = p.copy(propTemplate)
		newProp.name = "prop_"+propID
		newProp.par.Id = propID
		newProp.par.Created = createdTime
		newProp.tags.add('projectObject')
		externalPath = op.PROJECT.ProjectDir() + toxDir + newProp.name + ".tox"
		newProp.par.externaltox = externalPath

		op.UTILS.LayoutCOMPs(p, "prop", 200)
		op.UTILS.SetStatus("info","Created new prop")
		return
		
	def LoadFromProject(self, projectName):
		p.DeleteAll()
		toxFolder = op.PROJECT.ProjectDir() + toxDir
		toxes = op.UTILS.GetFilesFromFolder(toxFolder)
		
		for nTox in toxes:
			try:
				p.loadTox(toxFolder + nTox)
			except:
				pass
				
		op.UTILS.LayoutCOMPs(p, "prop", 200)
		return
		
	def Delete(self, propid):
		op('prop_'+propid).destroy()
		op.UTILS.SetStatus("info","Deleted Prop: " + propid)
		op.UTILS.LayoutCOMPs(p, "prop", 200)
		return
		
	def DeleteAll(self):
		op.UTILS.DeleteAllCOMPs(p, "prop")
		return
		
	def GetInfoTable(self):
		return op('null_get_props')
		
	def GetNumberOfProps(self):
		return p.GetInfoTable().numRows-1