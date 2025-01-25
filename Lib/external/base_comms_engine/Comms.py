from TDStoreTools import StorageManager
import TDFunctions as TDF
p = parent()
pp = p.par

mappingsetTemplate = op('base_template')

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

		op.UTILS.LayoutCOMPs(p, "mappingset", 200)
		op.UTILS.SetStatus("info","Created new screen")
		return
		
	def GetInfoTable(self):
		return op('null_get_mappingsets')
	
	def Delete(self, mappingsetid):
		op('mappingset_'+mappingsetid).destroy()
		op.UTILS.SetStatus("info","Deleted Mapping Set: " + mappingsetid)
		op.UTILS.LayoutCOMPs(p, "mappingset", 200)
		return
		
	def GetMIDIInput(self):
		return op('base_midi_input/out1')