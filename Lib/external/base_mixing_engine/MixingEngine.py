from TDStoreTools import StorageManager
import TDFunctions as TDF
activeMatrix = op('table_active_matrix')

p = parent()
pp = p.par

class MixingEngine:

	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
	
	# called when you drop something from the Asset Browser onto the Grid Laucher
	# It uses the layer ID and column ID to determine where you dropped.
	def LoadClip(self, layerId, column, filePath=None):
		
		if filePath:
			droppedOP = op(filePath)
		
			if droppedOP.parent(2).name == "container_toxs":
				toxPath = droppedOP.par.Filename.eval()
				clipId = op.CLIPS.Create("tox", layerId, filePath=toxPath)
				op.LAYERS.SetLayerClip(layerId, column, clipId)
				
			if droppedOP.parent(2).name == "container_movies":
				moviePath = droppedOP.par.Filename.eval()
				clipId = op.CLIPS.Create("movie", layerId, filePath=moviePath)
				op.LAYERS.SetLayerClip(layerId, column, clipId)
		else:
			clipId = op.CLIPS.Create("tox", layerId)
			op.LAYERS.SetLayerClip(layerId, column, clipId)
			
		return
		
	# matrix helper functions for dealing with the grid launcher
	# we set the matrix table to 1 or 0 to indicate playing or not
	# a DAT execute picks up on the table changes and then does the triggering
	# this means that the active table matrix and the ID matrix are the single sources of truth
	
	# Get the active matrix OP
	def GetActiveMatrix(self):
		return activeMatrix
	
	# update the layer IDs and column IDs in the active matrix
	def UpdateActiveMatrix(self):
		# set the size of the matrix table first
		layerList = op.LAYERS.op('null_get_params')
		activeMatrix.par.rows = layerList.numRows
		activeMatrix.par.cols = op.MIXER.par.Columnnumber+1
		
		# set the first column to be ids
		for r in range(0, activeMatrix.numRows):
			activeMatrix[r,0] = layerList[r,'Id']
			
		# set the first row to be column numbers
		for c in range(1, op.MIXER.par.Columnnumber+1):
			activeMatrix[0,c] = c
		return
	
	# stop playing all clips
	def StopAllClips(self):
		for r in range(1, activeMatrix.numRows):
			for c in range(1, activeMatrix.numCols):
				activeMatrix[r,c] = 0
		return
		
	# stop only a single layer from playing, this is useful for switching to a new clip in a layer
	def StopLayer(self, layerID):
		for c in range(1, activeMatrix.numCols):
			activeMatrix[layerID,c] = 0
		return
	
	# trigger a clip on a specific layer
	def PlayClipByLayerAndColumnID(self, layerID, columnID):
		p.StopLayer(layerID)
		activeMatrix[layerID, columnID] = 1
		return

	# trigger all clips in a specific column
	def PlayColumn(self, columnID):
		p.StopAllClips()
		
		for r in range(1, activeMatrix.numRows):
			layer = op.LAYERS.FindLayerByOrder(r-1)
			clipID = layer.FindClipIDByColumn(columnID-1)
			if clipID != "":
				activeMatrix[r,columnID] = 1
		return
	
	def CheckLayerForPlayingClips(self, activeRow):
		checkRow = activeMatrix.row(activeRow)
		foundPlayingClip = False

		for c in checkRow:
			if c.col > 0 and c > 0:
				foundPlayingClip = True
		
		return foundPlayingClip
	
	def SwapActiveMatrixVal(self, row1, col1, row2, col2):
		val1 = 0
		val2 = 0

		val1 = activeMatrix[row1,col1].val
		val2 = activeMatrix[row2,col2].val

		activeMatrix[row1, col1] = val2
		activeMatrix[row2, col2] = val1
		
		return
		