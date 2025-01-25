from TDStoreTools import StorageManager
import TDFunctions as TDF

p = parent()
pp = p.par
feedTemplate = op('base_template')
names = op('table_feed_default_names')

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

		op.UTILS.LayoutCOMPs(p, "feed", 200)
		op.UTILS.SetStatus("info","Created new feed")
		return
		
	def Delete(self, feedID):
		op('feed_'+feedID).destroy()
		op.UTILS.SetStatus("info","Deleted Feed: " + feedID)
		op.UTILS.LayoutCOMPs(p, "feed", 200)
		return
		
	def GetInfoTable(self):
		return op('null_get_feeds')
		
	def GetNumberOfFeeds(self):
		return p.GetInfoTable().numRows-1