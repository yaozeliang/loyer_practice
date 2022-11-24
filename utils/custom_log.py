
import os 
import sys
import logging
from functools import wraps
from datetime import datetime
from pytz import timezone

"""
LOGGING LEVEL PRIORITY
CRITICAL   50
ERROR      40
WARNING    30
INFO       20
DEBUG      10
NOTSET     0
"""

PARIS_TIME_ZONE = "Europe/Paris"
DEFAULT_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_FOLDER = 'logs'
LOG_LEVEL = logging.INFO 
TODAY = datetime.now().strftime("%Y%m%d")
LOG_FORMAT = '%(asctime)s|{}.py|%(levelname)s|%(message)s'

def Singleton(cls):
    instance = {}
    @wraps(cls)
    def get_instance(*args,**kwargs):
        if cls not in instance:
            instance[cls] = cls(*args,**kwargs)
        return instance[cls]
    return get_instance

def datetime2Utc(dt:datetime, timeformat:str=DEFAULT_TIME_FORMAT)->str:
    """Receive a datetime object and return utc time with string format"""
    return dt.astimezone(timezone('utc')).strftime(timeformat)

def datetime2Paris(dt:datetime, timeformat:str=DEFAULT_TIME_FORMAT)->str:
    """Receive a datetime object and return Paris time with string format"""
    return dt.astimezone(timezone(PARIS_TIME_ZONE)).strftime(timeformat)


@Singleton
class customLogging:

    def __init__(self, filename:str)->None:
        self.fileName = filename
        self.folderPath = f"{LOG_FOLDER}"
        self.completePath = f"./{LOG_FOLDER}/{TODAY}.log"
        if not os.path.exists(self.folderPath):
            os.makedirs(self.folderPath)
        self.format ="{0}|{1}.py|{2}|{3}"
        self.dateTimeFormat = '%Y-%m-%d %H:%M:%S'

    def write(self, msg)->None:
        today = datetime.now().strftime("%Y%m%d")
        self.completePath = f"./{LOG_FOLDER}/{today}.log"
        with open(self.completePath,encoding='utf-8', mode='a') as file:
            file.write(str(msg)+'\n')
        sys.stdout.write(str(msg)+'\n')
        print(str(msg)+'\n')
    
    def getDateTimeNow(self)->str:
        return datetime.now()
    
    def critical(self, msg:str)->None:
        msg = self.format.format(datetime2Paris(self.getDateTimeNow()), self.fileName, "CRITICAL", msg)
        self.write(msg)
        
    def error(self, msg:str)->None:
        msg = self.format.format(datetime2Paris(self.getDateTimeNow()), self.fileName, "ERROR", msg)      
        self.write(msg)  

    def warning(self, msg:str)->None:
        msg = self.format.format(datetime2Paris(self.getDateTimeNow()), self.fileName, "WARNING", msg)   
        self.write(msg) 
        
    def info(self, msg:str)->None:
        msg = self.format.format(datetime2Paris(self.getDateTimeNow()), self.fileName, "INFO", msg) 
        self.write(msg)
    
    def debug(self, msg:str)->None:
        msg = self.format.format(datetime2Paris(self.getDateTimeNow()), self.fileName, "DEBUG", msg)