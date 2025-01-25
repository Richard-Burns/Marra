from TDStoreTools import StorageManager
import TDFunctions as TDF

mappingsTbl = op('table_mappings')
p = parent()
pp = p.par

class MappingSet:

	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp

	def AddMapping(self, ID, type, address, path, parameter):
		mappingsTbl.appendRow([ID, type, address, path, parameter])
		return
	
	def RemoveMapping(self, ID):
		mappingsTbl.deleteRow(ID)
		return
	
	def MapMIDIToParameter(self,channel):
		opToArm = op.COMMS.par.Armedpath
		if opToArm != "":
			txtLearn = op(opToArm).op('text_learn')
			p.AddMapping(op.UTILS.CreateID(), "MIDI", channel.name, opToArm, txtLearn.par.Parametertooverride)
		op.COMMS.par.Armedpath = ""
		return
	
	def GetMappings(self):
		return op('null_get_mappings')
		
	def RemoveMappingByPath(self, path):
		for r in range(0, mappingsTbl.numRows):
			
			if mappingsTbl[r,'OP Path'] == path:
				mappingsTbl.deleteRow(r)
		
		
		return