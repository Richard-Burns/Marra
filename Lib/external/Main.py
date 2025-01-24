import os
from TDStoreTools import StorageManager
TDF = op.TDModules.mod.TDFunctions

class Main:

	def __init__(self, ownerComp):
		self.ownerComp = ownerComp
		return
		
	def Save(self):
		if ui.performMode == False:
			#project.save(saveExternalToxs=True)
			
			allCOMPS = parent().findChildren(type=COMP, parName='externaltox', onlyNonDefaults=True)
			
			for c in allCOMPS:
				if c.dirty:
					c.saveExternalTox(recurse=False)
		return