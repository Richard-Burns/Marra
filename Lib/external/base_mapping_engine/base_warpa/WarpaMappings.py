from TDStoreTools import StorageManager
import TDFunctions as TDF
import uuid
import time

p = parent()
pp = p.par
mappingTemplate = op('base_template')

class WarpaMappings:

	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		
	def Create(self):
		# generate id for screen
		mappingID = str(uuid.uuid1())
		mappingID = mappingID.replace('-','_')
		numMappings = parent().GetInfoTable().numRows-1
		createdTime = int(time.time())

		newMapping = p.copy(mappingTemplate)
		newMapping.name = "mapping_"+mappingID
		newMapping.par.Id = mappingID
		newMapping.par.Name = "warpa mapping"
		newMapping.par.Created = createdTime

		op.UTILS.LayoutCOMPs(p, "mapping", 200)
		op.UTILS.SetStatus("info","Created new mapping")
		return
		
	def Delete(self, mappingid):
		op('mapping_'+mappingid).destroy()
		op.UTILS.SetStatus("info","Deleted mapping: " + mappingid)
		op.UTILS.LayoutCOMPs(p, "mapping", 200)
		return
	
	def GetInfoTable(self):
		return op('null_get_mappings')
		
	