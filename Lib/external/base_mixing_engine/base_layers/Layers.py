from TDStoreTools import StorageManager
import TDFunctions as TDF

p = parent()
pp = parent().par
layerTemplate = op('base_template')
layersList = op('null_get_params')
numLayers = layersList.numRows-1
toxDir = op.PROJECT.ProjectDir()+"lib/mixing/layers/"

class Layers:

	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		
	def GetOrderedLayersList(self):
		layerOps = p.findChildren(name="layer_*", type=COMP)
		layerList = []
		for layerOp in layerOps:
			layerObj = {'id': layerOp.par.Id.eval(), 'order': layerOp.par.Order.eval()}
			layerList.append(layerObj)
			
		orderedLayerList = sorted(layerList, key=lambda d: d['order'])
		
		return orderedLayerList
		
	def GetInfoTable(self):
		return op('null_get_params')
		
	def GetIDMatrix(self):
		return op('null_id_matrix')
		
	def PlayClipByLayerAndColumnID(self, layerID, columnID):
		op('layer_'+layerID).PlayLayerClipByColumnID(columnID)
		return
	
	def StopClipByLayerAndColumnID(self, layerID, columnID):
		op('layer_'+layerID).PlayLayer('')
		return
		
	def CheckLayerOrder(self):
		
		orderedLayerList = p.GetOrderedLayersList()
		
		orderNum = 0
		for layerOp in orderedLayerList:
			layer = op('layer_'+layerOp['id'])
			layer.par.Order = orderNum
			layer.nodeX = 200 * orderNum
			
			orderNum = orderNum+1

		op.MIXER.UpdateActiveMatrix()
		return
		
	def FindLayerByOrder(self, order):
		layerOps = p.findChildren(name="layer_*", type=COMP)
		
		for r in layerOps:
			if r.par.Order == order:
				return r
		return
		
	def MoveLayerDown(self, layerId):
		moveLayer = op('layer_'+layerId)
		moveLayerOrder = moveLayer.par.Order.eval()
		layerBelow = p.FindLayerByOrder(moveLayerOrder+1)
		
		if layerBelow and moveLayerOrder < numLayers-1:
			layerBelow.par.Order = moveLayerOrder
			moveLayer.par.Order = moveLayerOrder+1
			op.UTILS.SetStatus('info', 'moved layer down')
			
		p.CheckLayerOrder()
		return
		
	def MoveLayerUp(self, layerId):
		moveLayer = op('layer_'+layerId)
		moveLayerOrder = moveLayer.par.Order.eval()
		layerAbove = p.FindLayerByOrder(moveLayerOrder-1)
		
		if layerAbove and moveLayerOrder > 0:
			layerAbove.par.Order = moveLayerOrder
			moveLayer.par.Order = moveLayerOrder-1
			op.UTILS.SetStatus('info', 'moved layer up')
			
		p.CheckLayerOrder()
		return

	def Create(self):
		
		# we need to check if we have any compositions to add to first
		numComps = op.COMPOSITIONS.GetNumberOfCompositions()
		
		# if not lets abort creating the layer and show the user a modal
		if numComps == 0:
			op.MODALS.ShowByID(3)
			op.UTILS.SetStatus('error', "couldn't create new layer. No Compositions available.")
			return
			
		# now lets check if a composition is selected.
		# if a comp isn't selected we'll just add the layer to the first one we find
		selectionObj = op.PARAMETERS.QuerySelection()
		compID = "none"
		
		if selectionObj['isSelected'] and selectionObj['type'] == "composition":
			compID = selectionObj['ID']
			
		else:
			compID = op.OUTPUTVIEWERS.par.Selectedid

			if compID == "" or compID == "none":
				compID = op.COMPOSITIONS.GetFirstCompositionID()
			
			#if compID == "none":
				#op.MODALS.ShowByID(3)
				#op.UTILS.SetStatus('error', "couldn't create new layer. Cant access selected Composition ID")
		
		# generate id for layer
		layerID = op.UTILS.CreateID()
		
		# generate a name for the layer
		
		nameDAT = op('table_layers_default_names')
		numNames = nameDAT.numRows
		nameIncrement = pp.Nameincrement

		newName = nameDAT[nameIncrement,0]
		
		if nameIncrement < numNames-1:
			pp.Nameincrement = nameIncrement+1
		else:
			pp.Nameincrement = 0
			
		# copy the template and set pars on new layer
		
		newLayer = p.copy(layerTemplate)
		newLayer.name = "layer_"+layerID
		newLayer.par.Name = newName
		newLayer.par.Id = layerID
		newLayer.par.Order = numLayers
		newLayer.par.Compositionid = compID
		newLayer.tags.add('projectObject')
		externalPath = op.PROJECT.ProjectDir() + toxDir + newLayer.name + ".tox"
		newLayer.par.externaltox = externalPath
		
		
		p.CheckLayerOrder()
		op.UTILS.LayoutCOMPs(p, "layer", 200)
		op.UTILS.SetStatus('info', 'created new layer: '+ layerID)
		
		return
		
	def LoadFromProject(self, projectName):
		p.DeleteAll()
		toxes = op.UTILS.GetFilesFromFolder(toxDir)
		
		for nTox in toxes:
			try:
				newTox = p.loadTox(toxDir + nTox)
				newTox.par.enableexternaltox = True
				newTox.par.externaltox = toxDir + nTox
			except:
				pass
				
		op.UTILS.LayoutCOMPs(p, "layer", 200)
		op.MIXER.UpdateActiveMatrix()
		return
		
	def Delete(self, layerID):
		
		layer = op('layer_'+layerID)
		
		clips = layer.GetClips()
		
		for c in clips:
			op.CLIPS.Delete(c)

		op.UTILS.DeleteExternalTox(layer.par.externaltox.eval())
		
		layer.destroy()
		op.UTILS.SetStatus('info', 'deleted layer: '+ layerID)
		op.UTILS.LayoutCOMPs(p, "layer", 200)
		p.CheckLayerOrder()
		return
	
	def DeleteAll(self):
		op.UTILS.DeleteAllCOMPs(p, "layer")
		op.MIXER.UpdateActiveMatrix()
		return
		
	def SetLayerClip(self, layerID, column, clipID):
		op('layer_'+layerID).LoadClip(column, clipID)
		
		op.UTILS.SetStatus('info', 'set layer clip - layer: '+layerID+' column: '+str(column)+' clip: '+clipID)
		return
		
	def SwapClip(self, layerId1, columnId1, layerId2, columnId2):
		columnIdLookup1 = columnId1-1
		columnIdLookup2 = columnId2-1
		
		clip1ID = str(op('layer_'+layerId1).FindClipIDByColumn(columnIdLookup1))
		clip2ID = str(op('layer_'+layerId2).FindClipIDByColumn(columnIdLookup2))
		
		op('layer_'+layerId1).LoadClip(columnIdLookup1,clip2ID)
		op('layer_'+layerId2).LoadClip(columnIdLookup2,clip1ID)
		
		op.MIXER.SwapActiveMatrixVal(op('layer_'+layerId1).par.Order+1, columnId1, op('layer_'+layerId2).par.Order+1, columnId2)
		
		op.UTILS.SetStatus('info', 'swapping clip ' + clip1ID + 'and ' + clip2ID)
		p.CheckLayerOrder()
		return
		
	def StopAllLayers(self):
		opsToStop = p.findChildren(name="layer_*", type=COMP)
		for stopOp in opsToStop:
			stopOp.PlayLayer('')
		
		op.UTILS.SetStatus('info', 'stopped all layers in the project')
		return
	
	def StopLayer(self, layerID):
		op('layer_'+layerID).PlayLayer('')
		return
		
	def GetClipIDByLayerIDAndColumnIndex(self, layerID, column):
		try:
			layerCOMP = op.LAYERS.op('layer_'+layerID)
			clipID = layerCOMP.FindClipIDByColumn(column)
		except:
			return ''
			
		return clipID
		
	def CheckAllLayersForMissingClips(self):
		layers = p.findChildren(type=COMP, name="layer_*")
		
		for l in layers:
			l.CheckForMissingClips()
		return