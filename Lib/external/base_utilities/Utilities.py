from TDStoreTools import StorageManager
import TDFunctions as TDF
import datetime

p = parent()
pp = p.par

class Utilities:

	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp

	def SetStatus(self, type, status):
		op(pp.Statuswidget).par.Value = status
		ct = datetime.datetime.now()
		op('fifo1').appendRow([ct, type, status])
		return
		
	def LayoutCOMPs(self, parentCOMP, name, nodeY):
		comps = parentCOMP.findChildren(type=COMP, name=name+"_*")
		
		nodeX = 400
		
		for c in comps:
			c.nodeX = nodeX
			c.nodeY = nodeY
			nodeX = nodeX+200
		return
	

	def SaveCOMPsToProject(self, parentCOMP, name, projectName="Default"):

		comps = p.findChildren(name=name+'_*', type=COMP)

		for c in comps:
			c.save("Projects/"+projectName+"/"+name+"s/"+c.name, createFolders=False)
		return
	
	def LoadCOMPsToProject(self, parentCOMP, name, projectName="Default"):
		# WARNING! calling this will wipe out all comps currently in the network

		op.UTILS.DeleteAllCOMPs(parentCOMP,name)
		
		dir_path = "Projects/"+projectName+"/"+name+"s/"

		compFiles = [
    		f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))
		]

		for c in compFiles:
			compPath = dir_path + c
			parentCOMP.loadTox(compPath, unwired=True)

		return
	
	def DeleteAllCOMPs(self, parentCOMP, name):
		opsToDelete = parentCOMP.findChildren(name=name+"_*", type=COMP)
		for delOp in opsToDelete:
			delOp.destroy()
			
		op.PARAMETERS.Deselect()
		return
	
	def RemoveDependentCOMPFromParameters(self, currentCOMPID, COMPToCheck, parameterName):
		# this function finds comps that are dependent on others and deletes them
		# for example if a composition is deleted all the connected layers should be too

		checkCOMPs = COMPToCheck.findChildren(type=COMP)
		for c in checkCOMPs:
			if c.par[parameterName] == currentCOMPID:
				checkCOMPs.Delete(c.par.Id)
		return