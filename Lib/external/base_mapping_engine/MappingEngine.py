from TDStoreTools import StorageManager
import TDFunctions as TDF

class MappingEngine:
	
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp

	def GetInfoTable(self):
		return op('null_get_mappings')
		
	def GetMappingByID(self, ID):
		
		warpaMappings = op.WARPA.GetInfoTable()
		camschnapprMappings = op.CAMSCHNAPPR.GetInfoTable()
		
		for r in range(0, warpaMappings.numRows):
			if warpaMappings[r,'Id'] == ID:
				return op.WARPA.op('mapping_'+ID)
				
		for r in range(0, camschnapprMappings.numRows):
			if camschnapprMappings[r,'Id'] == ID:
				return op.CAMSCHNAPPR.op('mapping_'+ID)
		
		return None