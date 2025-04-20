from TDStoreTools import StorageManager
import TDFunctions as TDF

p = parent()
pp = p.par
feedTemplate = op('base_template')
names = op('table_feed_default_names')
toxDir = "feeds/"

class Feeds:

	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		
	def Create(self):
		# generate id for screen
		feedID = op.UTILS.CreateID()
		numFeeds = parent().GetInfoTable().numRows-1
		nameIncrement = pp.Nameincrement
		numNames = names.numRows
		createdTime = op.UTILS.Timestamp()

		newName = names[nameIncrement,0]
		
		if nameIncrement < numNames-1:
			pp.Nameincrement = nameIncrement+1
		else:
			pp.Nameincrement = 0
			
		newColour = op('noise_comp_colours').sample(x=numFeeds,y=0)

		newFeed = p.copy(feedTemplate)
		newFeed.name = 'feed_'+feedID
		
		newFeed.par.Name = newName
		newFeed.par.Id = feedID
		newFeed.par.Feedcolorr = newColour[0]
		newFeed.par.Feedcolorg = newColour[1]
		newFeed.par.Feedcolorb = newColour[2]
		newFeed.par.Created = createdTime
		newFeed.par.display = 1
		newFeed.par.enable = 1
		newFeed.tags.add('projectObject')
		externalPath = op.PROJECT.ProjectDir() + toxDir + newFeed.name + ".tox"
		newFeed.par.externaltox = externalPath

		op.UTILS.LayoutCOMPs(p, "feed", 200)
		op.UTILS.SetStatus("info","Created new feed")
		return
		
	def LoadFromProject(self, projectName):
		p.DeleteAll()
		toxFolder = op.PROJECT.ProjectDir() + toxDir
		toxes = op.UTILS.GetFilesFromFolder(toxFolder)
		
		for nTox in toxes:
			try:
				newTox = p.loadTox(toxFolder + nTox)
				newTox.par.enableexternaltox = True
				newTox.par.externaltox = toxFolder + nTox
			except:
				pass
				
		op.UTILS.LayoutCOMPs(p, "feed", 200)
		return
		
	def Delete(self, feedID):
		compOP = op('feed_'+feedID)
		op.UTILS.DeleteExternalTox(compOP.par.externaltox.eval())
		compOP.destroy()
		op.UTILS.SetStatus("info","Deleted Feed: " + feedID)
		op.UTILS.LayoutCOMPs(p, "feed", 200)
		return
		
	def DeleteAll(self):
		op.UTILS.DeleteAllCOMPs(p, "feed")
		return
		
	def GetInfoTable(self):
		return op('null_get_feeds')
		
	def GetNumberOfFeeds(self):
		return p.GetInfoTable().numRows-1