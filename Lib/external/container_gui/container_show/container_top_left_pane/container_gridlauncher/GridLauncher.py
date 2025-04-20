from TDStoreTools import StorageManager
import TDFunctions as TDF

p = parent()
pp = p.par

class GridLauncher:

	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		
	def SelectLayerByItem(self, itemID):
		layerID = op.LAYERS.GetInfoTable()[itemID,'Id']
		pp.Selectedclipid = ''
		pp.Selectedlayerid = layerID
		op.PARAMETERS.SetParameterObject("layer", layerID)
		return
		
		
	def SelectObject(self, layer, column):
		pp.Selectedlayer = layer
		pp.Selectedcolumn = column
		layerID = ""
		clipID = ""
		pp.Selectedlayerid = layerID
		pp.Selectedclipid = clipdID
		return

	def Scroll(self, direction):
		# this function is called from ./container_layers/container_grid_columns/container_layer_crop
		# theres a mouse chop in there with some slope logic that executes this function
		curScroll = pp.Columnscroll
		colNumber = op.MIXER.par.Columnnumber
		
		if direction == "left" and curScroll > 0:
			pp.Columnscroll = curScroll-1
		
		if direction == "right" and curScroll < colNumber-1:
			pp.Columnscroll = curScroll+1