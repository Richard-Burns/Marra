# me - this DAT
# scriptOp - the OP which is cooking
#
# press 'Setup Parameters' in the OP to call this function to re-create the parameters.
def onSetupParameters(scriptOp):
	return

# called whenever custom pulse parameter is pushed
def onPulse(par):
	return

def onCook(scriptOp):
	scriptOp.clear()
	layersList = op.LAYERS.GetOrderedLayersList()
	layerNum = 0
	
	clipRow = []
	
	for r in range(0, parent().par.Columnnumber):
		clipRow.append("Column" + str(r+1))
		
	scriptOp.appendRow(clipRow)
	
	
	for layer in layersList:
		layerID = layersList[layerNum]['id']
		layerOP = op.LAYERS.op('layer_'+layerID)
		clipRow = layerOP.GetClips()
		
		scriptOp.appendRow(clipRow)
		layerNum = layerNum+1
	
	#scriptOp.copy(scriptOp.inputs[0])	# no need to call .clear() above when copying
	#scriptOp.insertRow(['color', 'size', 'shape'], 0)
	#scriptOp.appendRow(['red', '3', 'square'])
	#scriptOp[1,0] += '**'

	return
