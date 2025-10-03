from TDStoreTools import StorageManager
import TDFunctions as TDF

p = parent()
pp = p.par
mappingTemplate = op('base_template')
toxDir = op.PROJECT.ProjectDir()+"lib/mappings/camschnappr/"

class CamSchnapprMappings:

	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		
	def Create(self):
		# generate id for screen
		mappingID = op.UTILS.CreateID()
		numMappings = parent().GetInfoTable().numRows-1
		createdTime = op.UTILS.Timestamp()

		newMapping = p.copy(mappingTemplate)
		newMapping.name = "mapping_"+mappingID
		newMapping.par.Id = mappingID
		newMapping.par.Name = "CamSchnappr mapping"
		newMapping.par.Created = createdTime
		newMapping.tags.add('projectObject')
		externalPath = op.PROJECT.ProjectDir() + toxDir + newMapping.name + ".tox"
		newMapping.par.externaltox = externalPath

		op.UTILS.LayoutCOMPs(p, "mapping", 200)
		op.UTILS.SetStatus("info","Created new camschnappr mapping")
		return

	def LoadFromProject(self, projectName):
		p.DeleteAll()
		toxes = op.UTILS.GetFilesFromFolder(toxDir)
		
		for nTox in toxes:
			try:
				newTox = p.loadTox(toxDir + nTox)
				newTox.par.enableexternaltox = True
				newTox.par.externaltox = toxDir + nTox
			except:
				pass
				
		op.UTILS.LayoutCOMPs(p, "mapping", 200)
		return
		
	def Delete(self, mappingid):
		compOP = op('mapping_'+mappingid)
		op.UTILS.DeleteExternalTox(compOP.par.externaltox.eval())
		compOP.destroy()
		op.UTILS.SetStatus("info","Deleted mapping: " + mappingid)
		op.UTILS.LayoutCOMPs(p, "mapping", 200)
		return
		
	def DeleteAll(self):
		op.UTILS.DeleteAllCOMPs(p, "mapping")
		return
	
	def GetInfoTable(self):
		return op('null_get_mappings')