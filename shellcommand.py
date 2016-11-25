###############################################################################################################			
## shellcommand																															  ##			
## AUTHOR Alejandro Dirgan																												##
## VERSION 0.1																																##							
## DATE Nov 2015																															 ##
################################################################################################################			

#------------------------------------------------
class shellCommand():
#------------------------------------------------
	
	RETURNCODE = 0
	OUTPUT = 1
	NOERROR = 0
	
#------------------------------------------------
	def __init__(self, command):
#------------------------------------------------
		self.returnCode = 0
		self.commandLine = command
		
#------------------------------------------------
	def run(self, sortedOutput=False):
#------------------------------------------------
		returnOutput=list()
		p = Popen(self.commandLine, shell=True, stdout=PIPE, stderr=STDOUT)
		for i in iter(p.stdout.readline, b''):
			returnOutput.append(i.replace('\n','').strip())
		self.returnCode = p.wait() 
		
		if sortedOutput:
			commandOutput = sorted(returnOutput)
		else:
			commandOutput = (returnOutput)

		return iter(commandOutput)

#------------------------------------------------
	def runBackground(self):
#------------------------------------------------
		p = Popen(self.commandLine, shell=True, stdout=PIPE, stderr=STDOUT)
		
		return p

#------------------------------------------------
	def replaceCommand(self, command):
#------------------------------------------------
		self.commandLine = command
		
		return self
			  
#------------------------------------------------
	def status(self):
#------------------------------------------------
		return self.returnCode

#------------------------------------------------
if __name__=='__main__':
#------------------------------------------------
	pass
