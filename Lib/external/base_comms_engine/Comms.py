from TDStoreTools import StorageManager
import TDFunctions as TDF
p = parent()
pp = p.par

mappingsetTemplate = op('base_template')
toxDir = "comms/"

class Comms:

	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp

	def Create(self):
		mapID = op.UTILS.CreateID()
		numMappingSets = parent().GetInfoTable().numRows-1
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
				p.loadTox(toxFolder + nTox)
			except:
				pass
				
		op.UTILS.LayoutCOMPs(p, "mappingset", 200)
		return
		
		
	def GetInfoTable(self):
		return op('null_get_mappingsets')
	
	def Delete(self, mappingsetid):
		if not op('mappingset_'+mappingsetid).par.Locked:
			op('mappingset_'+mappingsetid).destroy()
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