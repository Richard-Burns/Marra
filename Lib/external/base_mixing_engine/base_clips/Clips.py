from TDStoreTools import StorageManager
import TDFunctions as TDF
import uuid
import os

p = parent()
pp = parent().par
engineEnabled = pp.Touchenginemode
toxFolder = pp.Toxfolder
clipTemplate = op('base_template')

class Clips:
	"""
	Manages all clip logic
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		
	def SetClipPosition(self, opToMove, yPos):
		# set pos based on how many clips we have
		clipFinder = op('opfind_clips')
		clipFinder.par.cookpulse.pulse()
		xPos = (clipFinder.numRows-1)*yPos
		opToMove.nodeX = xPos
		opToMove.nodeY = yPos
		return
		
		
	def CreateClip(self, type,layerID, filePath=None):
		
		# generate id for clip
		clipID = str(uuid.uuid1())
		clipID = clipID.replace('-','_')
		toxName = "New Clip"
		
		# figure out which tox to load based on the type
		if filePath:
			toxToLoad = filePath
			toxFolder, toxName = os.path.split(filePath)
			
			if type == "movie":
				toxToLoad = pp.Movieplayer
			if type == "notch":
				toxToLoad = pp.Notchplayer
		else:
			toxToLoad = pp.Template
			
		# first we copy our clip template op into position
		
		newClip = p.copy(clipTemplate)
		newClip.name = "clip_"+clipID
		newClip.par.Name = toxName
		newClip.par.Id = clipID
		newClip.par.Compositionid = op.LAYERS.op('layer_'+layerID).par.Compositionid
		p.SetClipPosition(newClip,200)
			
		# now we create our external tox inside our new clip
		# check if touchengine is enabled
		if engineEnabled:
			newCOMP = newClip.create(engineCOMP, "base_tox")
			newCOMP.par.file = toxToLoad
			#newCOMP.par.reload.pulse()
			newCOMP.par.callbacks = 'text_enginecallbacks'
			op.UTILS.SetStatus('info', 'created new engine COMP:'+ newClip.par.Name)
			
		else:
			newCOMP = newClip.create(baseCOMP, "base_tox")
			newCOMP.par.externaltox = toxToLoad
			newCOMP.par.enableexternaltoxpulse.pulse()
			newClip.ConnectSettings()
			op.UTILS.SetStatus('info', 'created new standard COMP:'+ newClip.par.Name)
			
		
		p.LayoutClips()
		
		return clipID
		
	def DeleteClip(self, clipid):
		try:
			op('clip_'+clipid).destroy()
			op.UTILS.SetStatus('info', 'deleted Clip: ' +clipid)
		except:
			op.UTILS.SetStatus('warn', "couldn't delete "+ clipid+ " - it probably doesn't exist")
		p.LayoutClips()
		op.LAYERS.CheckAllLayersForMissingClips()
		return
		
	def DeleteAllClips(self):
		opsToDelete = p.findChildren(name="clip_*", type=COMP)
		for delOp in opsToDelete:
			delOp.destroy()
			
		op.UTILS.SetStatus('info', 'deleted all clips in the project')
		return
		
	def LayoutClips(self):
		clips = p.findChildren(type=COMP, name="clip*")
		
		nodeX = 0
		
		for c in clips:
			c.nodeX = nodeX
			nodeX = nodeX+200
		return
		
	def OpenClipNetwork(self, clipID):
		p = ui.panes.createFloating(type=PaneType.NETWORKEDITOR, monitorSpanWidth=0.8, monitorSpanHeight=0.8)
		p.owner = op.CLIPS.op('clip_'+clipID).op('base_tox')
		return