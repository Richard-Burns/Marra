from TDStoreTools import StorageManager
import TDFunctions as TDF

class SplashScreen:

	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		
	def CreateProject(self):
		projectNameOp = op('container_projects/container_fieldstring1')
		projectName = projectNameOp.par.Value
		op.PROJECT.Create(projectName)
		op.PROJECT.LoadProject(projectName)
		op.SPLASHSCREEN.par.display = 0
		projectNameOp.par.Value = ''
		return
		
	def LoadProject(self):
		op.PROJECT.LoadProject(op('container_projects/container_list_projects').par.Value)
		op.SPLASHSCREEN.par.display = 0
		
	def Show(self):
		op.SPLASHSCREEN.par.display = 1
		return