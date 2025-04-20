from TDStoreTools import StorageManager
import TDFunctions as TDF

p = parent()
pp = p.par
camTemplate = op('geo_template')
toxDir = "stage/cameras/"

class Cameras:

	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		
	def Create(self):
		# generate id for screen
		cameraID = op.UTILS.CreateID()
		numCams = parent().GetInfoTable().numRows-1
		createdTime = op.UTILS.Timestamp()

		newCam = p.copy(camTemplate)
		newCam.name = "camera_"+cameraID
		newCam.par.Id = cameraID
		newCam.par.Created = createdTime
		newCam.par.render = True
		newCam.tags.add('projectObject')
		externalPath = op.PROJECT.ProjectDir() + toxDir + newCam.name + ".tox"
		newCam.par.externaltox = externalPath

		op.UTILS.SetStatus("info","Created new camera")
		op.UTILS.LayoutCOMPs(p, "camera", 200)
		return
		
	def LoadFromProject(self, projectName):
		p.DeleteAll()
		toxFolder = op.PROJECT.ProjectDir() + toxDir
		toxes = op.UTILS.GetFilesFromFolder(toxFolder)
		
		for nTox in toxes:
			try:
				newTox = p.loadTox(toxFolder + nTox)
				newTox.par.enableexternaltox = True
				newTox.par.externaltox = toxFolder + nTox
			except:
				pass
				
		op.UTILS.LayoutCOMPs(p, "camera", 200)
		return
		
	def Delete(self, camID):
		compOP = op('camera'+camID)
		op.UTILS.DeleteExternalTox(compOP.par.externaltox.eval())
		compOP.destroy()
		op.UTILS.SetStatus("info","Deleted Camera: " + camID)
		op.UTILS.LayoutCOMPs(p, "camera", 200)
		return
		
	def DeleteAll(self):
		op.UTILS.DeleteAllCOMPs(p, "camera")
		return
		
	def GetInfoTable(self):
		return op('null_get_cameras')
		
	def GetNumberOfCameras(self):
		return p.GetInfoTable().numRows-1
		
	def GetAudienceCamera(self):
		retCam = op.CAMERAS.op('camera_'+parent().par.Audiencecameraid).op('cam1')
		return retCam