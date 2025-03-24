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
		
	def LoadClip(self, layerId, column, filePath=None):
		
		if filePath:
			droppedOP = op(filePath)
		
			if droppedOP.parent(2).name == "container_toxs":
				toxPath = droppedOP.par.Filename.eval()
				clipId = op.CLIPS.Create("tox", layerId, filePath=toxPath)
				op.LAYERS.SetLayerClip(layerId, column, clipId)
		else:
			clipId = op.CLIPS.Create("tox", layerId)
			op.LAYERS.SetLayerClip(layerId, column, clipId)
			
		return
		
	def ZeroOutActiveMatrix(self):
		for r in range(0, activeMatrix.numRows):
			for c in range(0, activeMatrix.numCols):
				activeMatrix[r,c] = 0
		return
		
	def ZeroOutActiveMatrixRow(self, row):
		for c in range(0, activeMatrix.numCols):
			activeMatrix[row,c] = 0
		return
		
	def SwapActiveMatrixVal(self, val1, val2): # provide a [row, col] array for val1 and val2
	
		print('val1: ' + str(val1[0]) + " " + str(val1[1]))
		print('val2: ' + str(val2[0]) + " " + str(val2[1]))
		aVal1 = 0
		aVal2 = 0
		
		aVal1 = activeMatrix[val1[0], val1[1]].val
		aVal2 = activeMatrix[val2[0], val2[1]].val
			
		activeMatrix[val1[0],val1[1]] = aVal2
		activeMatrix[val2[0],val2[1]] = aVal1
		
		return
		
	def SetActiveMatrixForLayer(self, layerID, column):
		layersList = op.LAYERS.GetInfoTable()
		
		for r in range(0, layersList.numRows):
			if layersList[r,'Id'] == layerID:
				self.ZeroOutActiveMatrixRow(r-1)
				activeMatrix[r-1,column] = 1
		return
	
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
		
	def PopulateColumnNames(self):
		op.UTILS.SetStatus('info', 'changed number of columns to '+ str(colNames.numCols))
		for r in range(0, colNames.numCols):
			if colNames[0,r] == "":
				colNames[0,r] = "column " + str(r)
		return