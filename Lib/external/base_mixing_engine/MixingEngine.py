from TDStoreTools import StorageManager
import TDFunctions as TDF
activeMatrix = op('table_active_matrix')
colNames = op('table_column_names')

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
	
	# stop playing all clips
	def ZeroOutActiveMatrix(self):
		for r in range(0, activeMatrix.numRows):
			for c in range(0, activeMatrix.numCols):
				activeMatrix[r,c] = 0
		return
		
	# stop playing a layer of clips
	def ZeroOutActiveMatrixRow(self, row):
		for c in range(0, activeMatrix.numCols):
			activeMatrix[row,c] = 0
		return
	
	# swap two clips
	def SwapActiveMatrixVal(self, val1, val2): # provide a [row, col] array for val1 and val2
		aVal1 = 0
		aVal2 = 0
		
		aVal1 = activeMatrix[val1[0], val1[1]].val
		aVal2 = activeMatrix[val2[0], val2[1]].val
			
		activeMatrix[val1[0],val1[1]] = aVal2
		activeMatrix[val2[0],val2[1]] = aVal1
		
		return
		
	# trigger a single clip in a column and stop all other columns clips
	def SetActiveMatrixForLayer(self, layerID, column):
		layersList = op.LAYERS.GetInfoTable()
		
		for r in range(0, layersList.numRows):
			if layersList[r,'Id'] == layerID:
				self.ZeroOutActiveMatrixRow(r-1)
				activeMatrix[r-1,column] = 1
		return
	
	# Trigger an entire column of clips by ID
	def TriggerColumn(self, column):
		colName = colNames[0,column]
		layerList = op.LAYERS.GetInfoTable()
		op.UTILS.SetStatus('info', 'triggering column: ' + colName)

		for r in range(1, layerList.numRows):
			op.LAYERS.op('layer_'+layerList[r,'Id']).TriggerLayerClipByColumn(column)
			
		# update the active matrix
		
		self.ZeroOutActiveMatrix()
		for r in range(0, activeMatrix.numRows):
			activeMatrix[r,column-1] = 1
		
		
		return
	
	def GetActiveMatrix(self):
		return activeMatrix
		
		
	# Called when you change the number of columns in the project.
	def PopulateColumnNames(self):
		op.UTILS.SetStatus('info', 'changed number of columns to '+ str(colNames.numCols))
		for r in range(0, colNames.numCols):
			if colNames[0,r] == "":
				colNames[0,r] = "column " + str(r)
		return