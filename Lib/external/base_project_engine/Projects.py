from TDStoreTools import StorageManager
import TDFunctions as TDF
import os

p = parent()
pp = p.par

projectsDir = pp.Projectsdirectory

class Projects:

	# This class manages all project related logic
	# Projects are loaded and saved into the projectsDir folder which is set by the custom parameter Projectsdirectory

	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
	
	# returns the current project directory root
	def ProjectDir(self):
		fullPath = projectsDir + pp.Currentproject +"/"
		return fullPath
	
	# deletes all non-template objects from the project. 
	# It basically sets everything back to a clean new project.
	def ClearWorkspace(self):
		
		pp.Currentproject = ''
		
		# If you create a new engine functionality you can add it into the paths here
		# It needs a DeleteAll() function in it's extension to clear back to default
		opPaths = [
		op.COMMS,
		op.CLIPS,
		op.LAYERS,
		op.COMPOSITIONS,
		op.SCREENS,
		op.PROPS,
		op.CAMERAS,
		op.WARPA,
		op.CAMSCHNAPPR,
		op.FEEDS
		]
		
		for clearOP in opPaths:
			clearOP.DeleteAll()
			
		return
	
	# loads a project by name into the workspace
	def LoadProject(self, name):
		
		# clear the workspace
		p.ClearWorkspace()
		pp.Currentproject = name
		
		# first we get a list of comps with the MARRAENGINE tag
		# These are components with a template object that can be instanced
		engines = op.MARRA.findChildren(tags=["MARRAENGINE"])
		for engine in engines:
			try:
				engine.LoadFromProject(name)
			except:
				pass
		return

	# a helper function for making a single folder
	def MakeFolder(self, path, projectSuccess=True, projectIssue=""):
		try:
			# directory created
			os.mkdir(path)
		except FileExistsError:
			projectSuccess = False
			projectIssue = "Folder already exists"
		except PermissionError:
			projectSuccess = False
			projectIssue = "There's a permissions issue"
		except Exception as e:
			projectSuccess = False
			projectIssue = e

		return [projectSuccess, projectIssue]


	# a helper function for making a bunch of folders at once
	def MakeFoldersFromArray(self, path, directories, returnInfo):
		for subDir in directories:
			subDirPath = path + subDir

			returnInfo = p.MakeFolder(subDirPath, returnInfo[0], returnInfo[1])

		return returnInfo

	def Create(self, projectName):
		
		projectDir = projectsDir + projectName
		# Check whether the project exists or not
		returnInfo = p.MakeFolder(projectDir)

		# make first subdirectory
		subDirs = ["comms", "feeds", "mixing", "mappings", "stage", "settings"]
		subDirPath = projectsDir + projectName + "/"
		returnInfo = p.MakeFoldersFromArray(subDirPath, subDirs, returnInfo)
		
		# make mixing subdirectories
		stageDirs = ["compositions", "clips", "layers"]
		subDirPath = projectsDir + projectName + "/mixing/"
		returnInfo = p.MakeFoldersFromArray(subDirPath, stageDirs, returnInfo)

		# make stage subdirectories
		stageDirs = ["cameras", "props", "screens"]
		subDirPath = projectsDir + projectName + "/stage/"
		returnInfo = p.MakeFoldersFromArray(subDirPath, stageDirs, returnInfo)

		# make mapping subdirectories
		mappingDirs = ["camschnappr", "warpa"]
		subDirPath = projectsDir + projectName + "/mappings/"
		returnInfo = p.MakeFoldersFromArray(subDirPath, mappingDirs, returnInfo)

		projectSuccess = returnInfo[0]
		projectIssue = returnInfo[1]

		# check if everything went well
		if projectSuccess:
			op.UTILS.SetStatus("info", "Project Created: "+ projectName)
		else:
			op.UTILS.SetStatus("error", "Project creation failed: " + str(projectIssue))

		return
		
	# saves all COMPs in a project to the projects subdirectories
	def Save(self):
		projectCOMPS = op.MARRA.findChildren(type=COMP, tags=['projectObject'])
		
		for c in projectCOMPS:
			c.saveExternalTox(recurse=False)
		return