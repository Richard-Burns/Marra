from TDStoreTools import StorageManager
import TDFunctions as TDF
import datetime

p = parent()
pp = p.par

class Utilities:

	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp

	def SetStatus(self, type, status):
		op(pp.Statuswidget).par.Value = status
		ct = datetime.datetime.now()
		op('fifo1').appendRow([ct, type, status])
		return