from TDStoreTools import StorageManager
import TDFunctions as TDF
p = parent()
pp = p.par

mappingsetTemplate = op('base_template') # the template object for a mapping
toxDir = "comms/" # where the mapping is stored in the project folder

class Comms:

	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp

	def Create(self):
		mapID = op.UTILS.CreateID()
		createdTime = op.UTILS.Timestamp()

		newMappingSet = p.copy(mappingsetTemplate)
		newMappingSet.name = "mappingset_"+mapID
		newMappingSet.par.Name = "Mapping Set"
		newMappingSet.par.Id = mapID
		newMappingSet.par.Created = createdTime
		newMappingSet.tags.add('projectObject')
		externalPath = op.PROJECT.ProjectDir() + toxDir + newMappingSet.name + ".tox"
		newMappingSet.par.externaltox = externalPath

		op.UTILS.LayoutCOMPs(p, "mappingset", 200)
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
				
		op.UTILS.LayoutCOMPs(p, "mappingset", 200)
		return
		
		
	def GetInfoTable(self):
		return op('null_get_mappingsets')
	
	def Delete(self, mappingsetid):
		if not op('mappingset_'+mappingsetid).par.Locked:
			compOP = op('mappingset_'+mappingsetid)
			op.UTILS.DeleteExternalTox(compOP.par.externaltox.eval())
			compOP.destroy()
			op.UTILS.SetStatus("info","Deleted Mapping Set: " + mappingsetid)
			op.UTILS.LayoutCOMPs(p, "mappingset", 200)
		return
	
	def DeleteAll(self):
		op.UTILS.DeleteAllCOMPs(p, "mappingset")
		return
		
	def GetMIDIInput(self):
		return op('base_midi_input/out1')
		
	def GetOSCInput(self):
		return op('base_osc_input/out1')