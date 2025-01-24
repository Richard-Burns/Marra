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
	# change this path to decide which ops to get params for
	parentPath = op.WARPA
	templatePath = parentPath.op('base_template')
	cloneOPNames = "mapping_*"
	
	scriptOp.clear()
	
	names = []
	
	for p in templatePath.customPars:
		names.append(p.name)
	
	scriptOp.insertRow(names)
	for o in parentPath.findChildren(type=COMP, name=cloneOPNames, maxDepth=1):
		values = []
		for p in o.customPars:
			values.append(p.eval())
	
		if o.name != templatePath.name:
			scriptOp.appendRow(values)

	return
