class DebugMode:
    __COLORS = {
        'black': "\033[30m",
        'red': "\033[31m",
        'green': "\033[32m",
        'yellow': "\033[33m",
        'blue': "\033[34m",
        'magenta': "\033[35m",
        'cyan': "\033[36m",
        'white': "\033[37m",
        'reset': "\033[0m"
    }

    def __init__(self, debugMode=True, logFile=None):
        self.debugMode = debugMode
        if logFile != None:
            self.logFile = open(logFile, "w")
        else:
            self.logFile = None
    
    # call Destructor to close the file when the object is deleted or program ends
    def __del__(self):
        if self.logFile != None:
            self.logFile.close()

    def setDebugMode(self, debugMode):
        self.debugMode = debugMode

    def getDebugMode(self):
        return self.debugMode

    def debugPrint(self, message=None, fonction=None):
        if self.debugMode:
            if fonction != None:
                fonction()
            elif message != None:
                print(self.__COLORS["blue"] + message + self.__COLORS['reset'])

    def warningPrint(self, message):
        if self.debugMode:
            print(self.__COLORS["yellow"] + message + self.__COLORS['reset'])

    def logPrint(self, message):
        if self.logFile != None:
            if self.debugMode:
                print(self.__COLORS["green"] + "écriture dans le file" + self.__COLORS['reset'])
            self.logFile.write(message + "\n")
        else:
            raise Exception("No log file defined!")