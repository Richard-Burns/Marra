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
		
	def CreateProp(self):
		# generate id for screen
		propID = str(uuid.uuid1())
		propID = propID.replace('-','_')
		numProps = parent().GetInfoTable().numRows-1
		createdTime = int(time.time())

		newProp = p.copy(propTemplate)
		newProp.name = "prop_"+propID
		newProp.par.Id = propID
		newProp.par.Created = createdTime

		p.SetPropPosition(newProp,200)
		op.UTILS.SetStatus("info","Created new prop")
		return
		
	def SetPropPosition(self, opToMove, yPos):
		# set pos based on how many screens we have
		propOps = p.findChildren(name="prop_*", type=COMP)
		xPos = len(propOps)*yPos
		opToMove.nodeX = xPos
		opToMove.nodeY = yPos
		return
		
	def DeleteProp(self, propid):
		op('prop_'+propid).destroy()
		op.UTILS.SetStatus("info","Deleted Prop: " + propid)
		return
		
	def DeleteAllProps(self):
		opsToDelete = p.findChildren(name="prop_*", type=COMP)
		for delOp in opsToDelete:
			delOp.destroy()
		return
		
	def GetInfoTable(self):
		return op('null_get_props')
		
	def GetNumberOfProps(self):
		return p.GetInfoTable().numRows-1