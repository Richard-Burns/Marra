from TDStoreTools import StorageManager
import TDFunctions as TDF
import datetime
import uuid
import time
from pathlib import Path
import os
from os import listdir
from os.path import isfile, join

p = parent()
pp = p.par

class Utilities:

	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp

	def SetStatus(self, type, status):
		try:
			op(pp.Statuswidget).par.Value = status
		except:
			pass
		ct = datetime.datetime.now()
		op('fifo1').appendRow([ct, type, status])
		return
	
	def CreateID(self):
		newID = str(uuid.uuid1())
		newID = newID.replace('-','_')
		return newID
	
	def Timestamp(self):
		return int(time.time())
		
	def LayoutCOMPs(self, parentCOMP, name, nodeY):
		comps = parentCOMP.findChildren(type=COMP, name=name+"_*")
		
		nodeX = 400
		
		for c in comps:
			c.nodeX = nodeX
			c.nodeY = nodeY
			nodeX = nodeX+200
		return
	
	def DeleteAllCOMPs(self, parentCOMP, name):
		opsToDelete = parentCOMP.findChildren(name=name+"_*", type=COMP)
		for delOp in opsToDelete:
			delOp.destroy()
			
		op.PARAMETERS.Deselect()
		return
		
	def GetFilesFromFolder(self, folderPath):
		allFiles = [f for f in listdir(folderPath) if isfile(join(folderPath, f))]
		return allFiles
	
	def RemoveDependentCOMPFromParameters(self, currentCOMPID, COMPToCheck, parameterName):
		# this function finds comps that are dependent on others and deletes them
		# for example if a composition is deleted all the connected layers should be too

		checkCOMPs = COMPToCheck.findChildren(type=COMP)
		for c in checkCOMPs:
			if c.par[parameterName] == currentCOMPID:
				checkCOMPs.Delete(c.par.Id)
		return
		
	
	# used to delete projext tox files when a comp is deleted.
	def DeleteExternalTox(self, path):
		try:
			os.remove(path)
		except:
			p.SetStatus("warn","Couldn't delete: " + path + " Perhaps the project wasn't saved before deletion")
		return
		
	def Timecode(self):
		return op('timecode1').timecode