from time import sleep
import os, sys
from runinback import runInBack
from shellcommand import shellCommand
from timer import timer

################################################################################################################         
## dirWatchdog                                                                                                ##         
## AUTHOR Alejandro Dirgan                                                                                    ##
## VERSION 0.1                                                                                                ##                     
## DATE Nov 2017                                                                                              ##
################################################################################################################         

#------------------------------------------------   
class dirWatchdog():
#------------------------------------------------   

#------------------------------------------------   
	def __init__(self, ignoreFiles="._downloading"):
#------------------------------------------------   
		self.errorMessage = "OK: (dirWatchdog)"
		self.dirs2watch = {}
		self.ignoreFiles = ignoreFiles
		
		self.startWatchLoop = False
		self.exitWatchLoop=False
		self.timeforChecking = .5
		self.dirSizeChecking = False
		
		self.timer = timer()
		self.timer.setTimer(timerId='mainLoop',timeoutinseconds=self.timeforChecking)
		self.timer.startTimer('mainLoop')
		
#------------------------------------------------   
	def setTimeForChecking(self, time):
#------------------------------------------------   
		self.timeforChecking = time
        
#------------------------------------------------   
	def getLastMessage(self):
#------------------------------------------------   
		returnValue = self.errorMessage
		self.errorMessage = "OK: (dirWatchdog)"
		return returnValue

#------------------------------------------------   
	def addDir(self, dirName, path):
#------------------------------------------------   
		if not os.path.isdir(path): 
			self.errorMessage = "ERROR: (dirWatchdog) directory: [%s] not found!"%(path)
		else:
			self.errorMessage = "OK: (dirWatchdog) directory: [%s] added to be watched!"%path
			self.dirs2watch[dirName]=[os.path.abspath(path),dict ([(f, None) for f in os.listdir(os.path.abspath(path))]),set(),set(),set(), False, False, False, False]

#------------------------------------------------   
	def dirHasChanged(self, dirName):
#------------------------------------------------   
		returnValue = self.dirs2watch[dirName][5]
		self.dirs2watch[dirName][5] = False
		return returnValue

#------------------------------------------------   
	def dirAdded(self, dirName):
#------------------------------------------------   
		returnValue = sself.dirs2watch[dirName][6]
		sself.dirs2watch[dirName][6] = False
		return returnValue

#------------------------------------------------   
	def dirRemoved(self, dirName):
#------------------------------------------------   
		returnValue = self.dirs2watch[dirName][7]
		self.dirs2watch[dirName][7] = False
		return returnValue

#------------------------------------------------   
	def dirModified(self, dirName):
#------------------------------------------------   
		returnValue = self.dirs2watch[dirName][8]
		self.dirs2watch[dirName][8] = False
		return returnValue

#------------------------------------------------   
	def startWatch(self):
#------------------------------------------------   
		self.startWatchLoop = True
		runInBack(self.watch).start()

#------------------------------------------------   
	def stopWatch(self):
#------------------------------------------------   
		self.exitWatchLoop = True
		
#------------------------------------------------   
	def watch(self):
#------------------------------------------------   
		secondTry = False
		while not self.exitWatchLoop:
			if self.timer.expired('mainLoop'):
				for dirN in self.dirs2watch:
					try:
						currentDir = dict ([(f, os.stat("%s/%s"%(self.dirs2watch[dirN][0],f)).st_mtime) for f in os.listdir (self.dirs2watch[dirN][0])])
					except: pass
					for directory in [newFile for newFile in currentDir if not newFile in self.dirs2watch[dirN][1] and not self.ignoreFiles in newFile]: 
						#print "added"
						self.dirs2watch[dirN][5]=True
						self.dirs2watch[dirN][6]=True
						self.dirs2watch[dirN][2].add(directory)
						self.dirs2watch[dirN][3].discard(directory)
						self.dirs2watch[dirN][4].discard(directory)

					for directory in [newFile for newFile in self.dirs2watch[dirN][1] if not newFile in currentDir and not self.ignoreFiles in newFile]: 
						#print "removed"
						self.dirs2watch[dirN][5]=True
						self.dirs2watch[dirN][7]=True
						self.dirs2watch[dirN][3].add(directory)
						self.dirs2watch[dirN][2].discard(directory)
						self.dirs2watch[dirN][4].discard(directory)
					
					if secondTry:
						try:
							for directory in currentDir:
								if currentDir[directory] != self.dirs2watch[dirN][1][directory]:
									#print "modified"
									self.dirs2watch[dirN][5]=True
									self.dirs2watch[dirN][8]=True
									self.dirs2watch[dirN][2].discard(directory)
									self.dirs2watch[dirN][3].discard(directory)
									self.dirs2watch[dirN][4].add(directory)
						except:
							pass
					else:
						secondTry = True			
					
					self.dirs2watch[dirN][1] = currentDir
				self.timer.startTimer('mainLoop')
			
			sleep(.1)
		
#------------------------------------------------   
	def popAdded(self, dirName):
#------------------------------------------------   
		returnValue = None
		try:
			returnValue = self.dirs2watch[dirName][2].pop()
		except:
			pass
		
		return returnValue
		
#------------------------------------------------   
	def discardAdded(self, dirName):
#------------------------------------------------   
		try:
			self.dirs2watch[dirName][2]=set()
		except:
			pass
		
		return self
		
#------------------------------------------------   
	def popRemoved(self, dirName):
#------------------------------------------------   
		returnValue = None
		try:
			returnValue = self.dirs2watch[dirName][3].pop()
		except:
			pass
		
		return returnValue

#------------------------------------------------   
	def discardRemoved(self, dirName):
#------------------------------------------------   
		try:
			self.dirs2watch[dirName][3]=set()
		except:
			pass
		
		return self

#------------------------------------------------   
	def popModified(self, dirName):
#------------------------------------------------   
		returnValue = None
		try:
			returnValue = self.dirs2watch[dirName][4].pop()
		except:
			pass
		
		return returnValue

#------------------------------------------------   
	def discardModified(self, dirName):
#------------------------------------------------   
		try:
			self.dirs2watch[dirName][4]=set()
		except:
			pass
		
		return self

#-------------------------------------------------------------------------------------------------------------------
if __name__=='__main__':
#-------------------------------------------------------------------------------------------------------------------
	dWatch = dirWatchdog()
	dWatch.addDir("music","/home/ydirgan/python")
	
	lastMessage = dWatch.getLastMessage()
	print lastMessage
	if not "OK:" in lastMessage:
		exit(0)
		
	dWatch.startWatch()
	
	try:
		while True:
			if dWatch.dirHasChanged("music"):
				addedElement = -1
				while addedElement!=None: #process until last element of added queue left!
					addedElement = dWatch.popAdded("music")
					if addedElement != None: 
						print "file/dir (%s) added to path"%addedElement 
						#print "copying added element (%s) to /home/ydirgan/Music"%addedElement
						#shellCommand('cp -r "/home/ydirgan/Dropbox/STAGING/%s" /home/ydirgan/Music/.'%addedElement).run()
						#print "removing added element (%s) from /home/ydirgan/Dropbox/STAGING"%addedElement
						#shellCommand('rm -rf "/home/ydirgan/Dropbox/STAGING/%s"'%addedElement).run()
						#print "Done"
				
				removedElement = -1
				while removedElement!=None: #process until last element of removed queue left!
					removedElement = dWatch.popRemoved("music")
					if removedElement != None: 
						print "file/dir (%s) removed to path"%removedElement 

				modifiedElement = -1
				while modifiedElement!=None: #process until last element of removed queue left!
					modifiedElement = dWatch.popModified("music")
					if modifiedElement != None: 
						print "file/dir (%s) modified to path"%modifiedElement 

				
			sleep(.5)
	except KeyboardInterrupt:
		dWatch.stopWatch()
