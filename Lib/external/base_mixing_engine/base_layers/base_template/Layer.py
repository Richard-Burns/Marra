from TDStoreTools import StorageManager
import TDFunctions as TDF

p = parent()
pp = p.par
tc = op('table_columns')

class Layer:

	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		
	def GetColumnByClipID(self, id):
		# this function ensures that no matter where we run TriggerLayer from
		# the active matrix gets updated correctly
		
		retCol = -1
		
		for c in range(0, tc.numCols):
			if id == tc[0,c]:
				retCol = c
		return retCol

	def TriggerLayer(self, clipID):
		if pp.Currentblend:
			pp.Clipa = clipID
		else:
			pp.Clipb = clipID
		
		pp.Currentblend = 1-pp.Currentblend
		
		# update active matrix
		clipCol = self.GetColumnByClipID(clipID)
		op.MIXER.SetActiveMatrixForLayer(parent().par.Id, clipCol) 
		return
	
	def TriggerLayerClipByColumn(self, column):
		clipID = p.FindClipIDByColumn(column-1)
		p.TriggerLayer(clipID)
		return

	def LoadClip(self, column, id):
		tc[0, column] = id
		return
		
	def CheckForMissingClips(self):
		for c in range(0, tc.numCols):
			if not op.CLIPS.op('clip_'+tc[0,c]):
				tc[0,c] = ''
		return
		
	def FindClipIDByColumn(self, column):
		return tc[0,column]
		
	def ReplaceClip(self, oldClipID, newClipID):
		for c in range(0, tc.numCols):
			if tc[0,c] == oldClipID:
				tc[0,c] = newClipID
		return
		
	def GetClips(self):
		return op('table_columns').row(0)