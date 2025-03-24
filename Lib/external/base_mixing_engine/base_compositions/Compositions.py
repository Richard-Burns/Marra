from TDStoreTools import StorageManager
import TDFunctions as TDF
import uuid
import time
import os
from pathlib import Path

p = parent()
pp = p.par
compTemplate = op('base_template')
toxDir = "mixing/compositions/"

class Compositions:

	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp

		
	def Create(self):
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
		newComp.tags.add('projectObject')
		externalPath = op.PROJECT.ProjectDir() + toxDir + newComp.name + ".tox"
		newComp.par.externaltox = externalPath

		op.UTILS.LayoutCOMPs(p, "composition", 200)
		op.UTILS.SetStatus("info","Created new composition called " + newName)
		
		# update ui elements
		op.PARAMETERS.SetParameterObject("composition", compID)
		op.OUTPUTVIEWERS.SetLatestToSelected()
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
				
		op.UTILS.LayoutCOMPs(p, "composition", 200)
		return
		
	def Delete(self, compid):
		op('composition_'+compid).destroy()
		op.UTILS.RemoveDependentCOMPFromParameters(compid, op.LAYERS, "Compositionid")
		op.UTILS.SetStatus("info","Deleted composition: " + compid)
		
		#update UI
		try:
			op.PARAMETERS.Deselect()
		except:
			pass
		
		op.UTILS.LayoutCOMPs(p, "composition", 200)
		return
		
	def DeleteAll(self):
		op.UTILS.DeleteAllCOMPs(p, "composition")
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