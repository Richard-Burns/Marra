from TDStoreTools import StorageManager
import TDFunctions as TDF
import os

p = parent()
pp = parent().par
engineEnabled = pp.Touchenginemode
toxFolder = pp.Toxfolder
clipTemplate = op('base_template')
toxDir = op.PROJECT.ProjectDir()+"lib/mixing/clips/"

class Clips:
	"""
	Manages all clip logic
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		
	def Create(self, type,layerID, filePath=None):
		
		# generate id for clip
		clipID = op.UTILS.CreateID()
		toxName = "New Clip"
		
		# figure out which tox to load based on the type
		if filePath:
			toxToLoad = filePath
			toxFolder, toxName = os.path.split(filePath)
			
			if type == "movie":
				toxToLoad = pp.Movieplayer
		else:
			toxToLoad = pp.Template
			
		# first we copy our clip template op into position
		
		newClip = p.copy(clipTemplate)
		newClip.name = "clip_"+clipID
		newClip.par.Name = toxName
		newClip.par.Id = clipID
		newClip.par.Compositionid = op.LAYERS.op('layer_'+layerID).par.Compositionid
		newClip.par.Type = type
		newClip.tags.add('projectObject')

		# when creating an empty clip we give it a generic name
		if not filePath:
			numClips = op('opfind_clips').numRows-1
			newClip.par.Name = "Clip "+str(numClips)
			

		externalPath = toxDir + newClip.name + ".tox"
		newClip.par.externaltox = externalPath

		# we need to delete the placeholder ops from template before we go creating our new ones
		newClip.op('base_tox').destroy()
		newClip.op('base_template_tox').destroy()
			
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


		# if we created a movie we need to set the file and initialize that moviefilein
		if type == "movie":
			newCOMP.par.File = filePath
			newCOMP.par.Reload.pulse()
			newCOMP.par.externaltox = ''
			newCOMP.par.enableexternaltox = False

		# if we created an empty new tox we need to change it from template to a new internal path
		if not filePath:
			newClipExternalPath = pp.Toxfolder + "/generated/" + newClip.par.Id + ".tox"
			newCOMP.tags.add('projectObject')
			newCOMP.par.externaltox = newClipExternalPath
			
		
		op.UTILS.LayoutCOMPs(p, "clip", 200)
		
		return clipID
		
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
				
		op.UTILS.LayoutCOMPs(p, "clip", 200)
		return
		
	def Delete(self, clipid):
		try:
			compOP = op('clip_'+clipid)
			op.UTILS.DeleteExternalTox(compOP.op('base_tox').par.externaltox.eval())
			op.UTILS.DeleteExternalTox(compOP.par.externaltox.eval())
			compOP.destroy()
			op.UTILS.SetStatus('info', 'deleted Clip: ' +clipid)
		except:
			op.UTILS.SetStatus('warn', "couldn't delete "+ clipid+ " - it probably doesn't exist")
		op.LAYERS.CheckAllLayersForMissingClips()
		op.UTILS.LayoutCOMPs(p, "clip", 200)
		return
		
	def DeleteAll(self):
		op.UTILS.DeleteAllCOMPs(p, "clip")
		return
		
	def OpenClipNetwork(self, clipID):
		p = ui.panes.createFloating(type=PaneType.NETWORKEDITOR, monitorSpanWidth=0.8, monitorSpanHeight=0.8)
		p.owner = op.CLIPS.op('clip_'+clipID).op('base_tox')
		return
		
	def Trigger(self, clipID):
		if clipID != '':
			op('clip_'+clipID).Trigger()
		return

	def SaveToLibrary(self, clipID):
		path = ui.chooseFile(start=pp.Toxfolder,load=False,fileTypes=['tox'],title='Save tox as:')
		if (path):
			op('clip_'+clipID).op('base_tox').save(path)