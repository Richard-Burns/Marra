from TDStoreTools import StorageManager
import TDFunctions as TDF

class ClipTemplate:

	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp

	def ConnectSettings(self):
		try:
			op('base_tox').setInputs([op('select_settings')])
		except:
			debug("couldnt connect settings to TOX, does your TOX have a DAT input for settings?")
		return

	def Trigger(self):
		try:
			op('base_tox').par.Initialize.pulse()
		except:
			pass