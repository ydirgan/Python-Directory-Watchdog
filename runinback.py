from threading import Thread

################################################################################################################         
## runInBack                                                                                                  ##         
## AUTHOR Alejandro Dirgan                                                                                    ##
## VERSION 0.1                                                                                                ##                     
## DATE Nov 2015                                                                                              ##
################################################################################################################         

#------------------------------------------------   
class runInBack():
#------------------------------------------------   

#------------------------------------------------
	def __init__(self, _process, _args=()):
#------------------------------------------------
		self.process = _process
		self.args = _args
		self.process = Thread(target=_process, args=_args)
		self.process.deamon = True
		self.lastError = ''
		self.finished = False
      
#------------------------------------------------
	def start(self):
#------------------------------------------------
		try:
			self.process.start()
		except:
			self.lastError = "Error: unable to start thread"
			print self.lastError
  
#------------------------------------------------
	def isAlive(self):
#------------------------------------------------
		return self.process.isAlive()

#------------------------------------------------
	def join(self):
#------------------------------------------------
			return self.process.join()
         
#------------------------------------------------
	def stop(self):
#------------------------------------------------
		try:
			self.process._Thread__stop()
			self.process.join()
			self.finished = True     
		except:
			self.lastError = str(self.getName()) + ' could not be terminated'
			print(self.lastError)

#------------------------------------------------
if __name__=='__main__':
#------------------------------------------------
	pass
