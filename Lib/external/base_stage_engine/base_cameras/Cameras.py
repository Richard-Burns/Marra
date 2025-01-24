from TDStoreTools import StorageManager
import TDFunctions as TDF
import uuid
import time

p = parent()
pp = p.par
camTemplate = op('geo_template')

class Cameras:

	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		
	def CreateCamera(self):
		# generate id for screen
		cameraID = str(uuid.uuid1())
		cameraID = cameraID.replace('-','_')
		numCams = parent().GetInfoTable().numRows-1
		createdTime = int(time.time())

		newCam = p.copy(camTemplate)
		newCam.name = "camera_"+cameraID
		newCam.par.Id = cameraID
		newCam.par.Created = createdTime
		newCam.par.render = True

		p.SetCameraPosition(newCam,200)
		op.UTILS.SetStatus("info","Created new camera")
		return
		
	def SetCameraPosition(self, opToMove, yPos):
		# set pos based on how many screens we have
		camOps = p.findChildren(name="camera_*", type=COMP)
		xPos = len(camOps)*yPos
		opToMove.nodeX = xPos
		opToMove.nodeY = yPos
		return
		
	def DeleteCamera(self, camID):
		op('camera_'+camID).destroy()
		op.UTILS.SetStatus("info","Deleted Camera: " + camID)
		return
		
	def DeleteAllCameras(self):
		opsToDelete = p.findChildren(name="camera_*", type=COMP)
		for delOp in opsToDelete:
			delOp.destroy()
		return
		
	def GetInfoTable(self):
		return op('null_get_cameras')
		
	def GetNumberOfCameras(self):
		return p.GetInfoTable().numRows-1
		
	def GetAudienceCamera(self):
		retCam = op.CAMERAS.op('camera_'+parent().par.Audiencecameraid).op('cam1')
		return retCam