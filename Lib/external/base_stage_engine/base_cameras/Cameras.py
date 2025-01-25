from TDStoreTools import StorageManager
import TDFunctions as TDF

p = parent()
pp = p.par
camTemplate = op('geo_template')

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

		p.SetCameraPosition(newCam,200)
		op.UTILS.SetStatus("info","Created new camera")
		op.UTILS.LayoutCOMPs(p, "camera", 200)
		return
		
	def Delete(self, camID):
		op('camera_'+camID).destroy()
		op.UTILS.SetStatus("info","Deleted Camera: " + camID)
		op.UTILS.LayoutCOMPs(p, "camera", 200)
		return
		
	def GetInfoTable(self):
		return op('null_get_cameras')
		
	def GetNumberOfCameras(self):
		return p.GetInfoTable().numRows-1
		
	def GetAudienceCamera(self):
		retCam = op.CAMERAS.op('camera_'+parent().par.Audiencecameraid).op('cam1')
		return retCam