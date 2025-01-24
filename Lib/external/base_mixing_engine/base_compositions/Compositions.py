from TDStoreTools import StorageManager
import TDFunctions as TDF
import uuid
import time

p = parent()
pp = p.par
compTemplate = op('base_template')

class Compositions:

	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		
	def CreateComposition(self):
		# generate id for scene
		compID = str(uuid.uuid1())
		compID = compID.replace('-','_')
		numCOMPs = parent().GetInfoTable().numRows-1
		nameCOMP = op('table_comp_default_names')
		numNames = nameCOMP.numRows
		nameIncrement = pp.Nameincrement
		createdTime = int(time.time())

		newName = nameCOMP[nameIncrement,0]
		
		if nameIncrement < numNames-1:
			pp.Nameincrement = nameIncrement+1
		else:
			pp.Nameincrement = 0
			
		newColour = op('noise_comp_colours').sample(x=numCOMPs,y=0)

		
		newComp = p.copy(compTemplate)
		newComp.name = "composition_"+compID
		newComp.par.Name = newName
		newComp.par.Id = compID
		newComp.par.Colourr = newColour[0]
		newComp.par.Colourg = newColour[1]
		newComp.par.Colourb = newColour[2]
		newComp.par.Created = createdTime

		p.SetCompPosition(newComp,200)
		op.UTILS.SetStatus("info","Created new composition called " + newName)
		
		# update ui elements
		op.PARAMETERS.SetParameterObject("composition", compID)
		op.OUTPUTVIEWERS.SetLatestToSelected()
		return
		
	def SetCompPosition(self, opToMove, yPos):
		# set pos based on how many clips we have
		compOps = p.findChildren(name="composition_*", type=COMP)
		xPos = len(compOps)*yPos
		opToMove.nodeX = xPos
		opToMove.nodeY = yPos
		return
		
	def DeleteComposition(self, compid):
		op('composition_'+compid).destroy()
		op.UTILS.SetStatus("info","Deleted composition: " + compid)
		
		#update UI
		try:
			op.PARAMETERS.Deselect()
		except:
			pass
		
		return
		
	def DeleteAllCompositions(self):
		opsToDelete = p.findChildren(name="composition_*", type=COMP)
		for delOp in opsToDelete:
			delOp.destroy()
			
		op.PARAMETERS.Deselect()
		return
		
	def GetInfoTable(self):
		return op('null_get_compositions')
		
	def GetNumberOfCompositions(self):
		return p.GetInfoTable().numRows-1
		
	def GetFirstCompositionID(self):
		try:
			firstCOMP = op(p.GetInfoTable()[1,'name'])
			firstCOMPID = firstCOMP.par.Id.eval()
		except:
			firstCOMPID = "none"
			
		return firstCOMPID