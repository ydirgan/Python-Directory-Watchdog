from datetime import datetime
from sys import exit
from time import sleep
import traceback

################################################################################################################         
## timer                                                                                                      ##         
## AUTHOR Alejandro Dirgan                                                                                    ##
## VERSION 0.1                                                                                                ##                     
## DATE Nov 2015                                                                                              ##
################################################################################################################         

#------------------------------------------------
class timer():
#------------------------------------------------
    
	def __init__(self): 
		self.error = 0
		self.timers = {}
		self.timers['timer1'] = { 'timerId': 'timer1', 
                                'timeout': 60,
                                'start': 0,
                                'stop': 0,
                                'started': False,
                                'diff': 0,
                                'seconds': 0,
                                'days': 0,
                                'microseconds': 0 }
                                
#------------------------------------------------
	def setTimer(self, timerId='timer1', timeoutinseconds=60, startNow=False): 
#------------------------------------------------
		self.error = 0
		try: 
			self.timers[timerId] = { 'timerId': timerId, 
                                   'timeout': timeoutinseconds,
                                   'start': 0,
                                   'stop': 0,
                                   'started': False,
                                   'diff': 0,
                                   'seconds': 0,
                                   'days': 0,
                                   'microseconds': 0 }
			returnValue = timerId                         
		except: 
			self.error = -1
          
		if startNow: self.startTimer(timerId=timerId)   

		return self 

#------------------------------------------------
	def setTimeout(self, timerId='timer1', timeoutinseconds=60): 
#------------------------------------------------
		self.error = 0     
		try: 
			self.timers[timerId]['timeout'] = timeoutinseconds
			returnValue = timeoutinseconds 
		except: 
			self.error = -1

		return self
       
#------------------------------------------------
	def expired(self, timerId='timer1'): 
#------------------------------------------------
		self.error = 0
		returnValue = False
		try: 
			if self.timeLapsed(timerId=timerId) > self.timers[timerId]['timeout']: 
				returnValue = True
		except: 
			self.error = -1
       
		return returnValue
             
#------------------------------------------------
	def startTimer(self, timerId='timer1'): 
#------------------------------------------------
		self.error = 0
		try: 
			self.timers[timerId]['started'] = True
		except: 
			self.error = -1
		try: 
			self.timers[timerId]['start'] = datetime.now()
		except: 
			self.error = -1

		return self       

#------------------------------------------------
	def stopTimer(self, timerId='timer1'): 
#------------------------------------------------
		self.error = 0
		try: 
			self.timers[timerId]['started'] = False
		except: 
			self.error = -1
		try: 
			self.timers[timerId]['stop'] = datetime.now()
		except: 
			self.error = -1

		self.timeDifference(timerId=timerId)

		return self       

#------------------------------------------------
	def timeLapsed(self, p=6, timerId = 'timer1'): 
#------------------------------------------------
		self.error = 0
		precisionTimeElapsed = 0.0
		try: 
			if self.timers[timerId]['started']: 
				precisionTimeElapsed=(datetime.now() - self.timers[timerId]['start']).total_seconds()
			else: 
				precisionTimeElapsed=self.timers[timerId]['diff']
		except: 
			self.error = -1

		return precisionTimeElapsed

#------------------------------------------------
	def isStarted(self, timerId='timer1'): 
#------------------------------------------------
		return self.timers[timerId]['started']

#------------------------------------------------
	def timeDifference(self, p=6, timerId='timer1'): 
#------------------------------------------------
		self.error = 0
		try: 
			self.timers[timerId]['diff'] = (self.timers[timerId]['stop'] - self.timers[timerId]['start']).total_seconds()
			returnValue = self.timers[timerId]['diff']
			self.timers[timerId]['seconds'] = self.timers[timerId]['diff'].total_seconds()
			self.timers[timerId]['days'] = self.timers[timerId]['diff'].days
			self.timers[timerId]['microseconds'] = self.timers[timerId]['diff'].microseconds
		except: 
			self.error = -1

		return self

#-------------------------------------------------------------------------------------------------------------------
if __name__=='__main__':
#-------------------------------------------------------------------------------------------------------------------
	t1=timer()
	t1.setTimeout(timeoutinseconds=1)
	t1.startTimer()
	 
	try:
		while True:
			if t1.expired(): 
				print t1.timeLapsed()
			sleep(1)
	except KeyboardInterrupt:
		exit(0)
