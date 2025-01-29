from TDStoreTools import StorageManager
import TDFunctions as TDF
import os

p = parent()
pp = p.par

projectsDir = 'Projects/'

class Projects:

	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp

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


	def MakeFoldersFromArray(self, path, directories, returnInfo):
		# make first subdirectory
		subDirs = ["clips", "compositions", "feeds", "layers", "mappings", "stage", "settings"]

		for subDir in directories:
			subDirPath = path + subDir

			returnInfo = p.MakeFolder(subDirPath, returnInfo[0], returnInfo[1])

		return returnInfo

	def Create(self, projectName):
		
		projectDir = projectsDir + projectName

		# Check whether the project exists or not
		
		returnInfo = p.MakeFolder(projectDir)

		# make first subdirectory
		subDirs = ["clips", "comms", "compositions", "feeds", "layers", "mappings", "stage", "settings"]
		subDirPath = projectsDir + projectName + "/"

		returnInfo = p.MakeFoldersFromArray(subDirPath, subDirs, returnInfo)

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

		
		if projectSuccess:
			op.UTILS.SetStatus("info", "Project Created: "+ projectName)
		else:
			op.UTILS.SetStatus("error", "Project creation failed: " + str(projectIssue))

		return