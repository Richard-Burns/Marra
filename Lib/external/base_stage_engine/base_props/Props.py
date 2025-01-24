from TDStoreTools import StorageManager
import TDFunctions as TDF
import uuid
import time

p = parent()
pp = p.par
propTemplate = op('geo_template')

class Props:

	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		
	def Create(self):
		# generate id for screen
		propID = str(uuid.uuid1())
		propID = propID.replace('-','_')
		numProps = parent().GetInfoTable().numRows-1
		createdTime = int(time.time())

		newProp = p.copy(propTemplate)
		newProp.name = "prop_"+propID
		newProp.par.Id = propID
		newProp.par.Created = createdTime

		op.UTILS.LayoutCOMPs(p, "prop", 200)
		op.UTILS.SetStatus("info","Created new prop")
		return
		
	def Delete(self, propid):
		op('prop_'+propid).destroy()
		op.UTILS.SetStatus("info","Deleted Prop: " + propid)
		op.UTILS.LayoutCOMPs(p, "prop", 200)
		return
		
	def GetInfoTable(self):
		return op('null_get_props')
		
	def GetNumberOfProps(self):
		return p.GetInfoTable().numRows-1