"""
step 1: create text file organized in columns of time, light, error
step 2: create batch file for text file made above
step 3: use batch to run period04 and output a results file
step 4: parse results file for frequency, compare between .3 and 1
step 5: delete files made during execution and return
"""

import os
import random
import string
from subprocess import check_output

class rrLyraeBinary(object):
    
    name = ""
    classifying_function = ""
    obsList = []
    #generate random str of length ten for directory name
    dirName = ''.join(random.choice(string.lowercase) for i in range(15))

    def __init__(self, name, classifying_function):
        """
        Constructor for the classification
        """
        self.name = name
        self.classifying_function = classifying_function
        
    def run(self, observations):
        """
        Method to be called to run the observations data that was
        aquired from the transient observation class
        """
        self.obsList = observations
        self.createFile()
        freq = self.makeBatch()
        self.cleanUp()
        result = self.classifying_function(freq)
        last_obs = observations[-1]
        return last_obs.object_id, last_obs.time, self.name, result
        
    def createFile(self):
        """
        Using the list of Observations given, create a text file organized in
        columns of light, time, error for period04
        """
        os.makedirs(self.dirName)
        file = open(self.dirName + '/LyraeData.dat', 'w+')
        for x in self.obsList:
            file.write(str(x.to_tuple()[1]) + " " + str(x.to_tuple()[2]) + " " + str(x.to_tuple()[3]))
            file.write("\n")
        file.close()
         
    def makeBatch(self):
        """
        Make and run the batch file for period04 to run, extract 
        the frequency period04 returns, and return that frequency
        """
        batFile = open(self.dirName + '/out.bat', 'w+')
        batFile.write("import tou LyraeData.dat\n")
        batFile.write("fourier 0 20 o n\n")
        batFile.write("savefreqs period04freqs.txt\n")
        batFile.write("exit\n")
        batFile.close()
        #period04 -batch=out.bat
        oldPath = os.getcwd()
        os.chdir(self.dirName)
        check_output(["period04","-batch=out.bat"])
        os.chdir(oldPath)
        freqFile = open(self.dirName + '/period04freqs.txt', 'r')
        r = ""
        for line in freqFile:
            r = line.split('\t')[1]
        freqFile.close()
        return float(r)
        
    def cleanUp(self):
        """
        delete the files we made to avoid cluttering the computer and
        name conflicts when this is run again
        """
        os.remove(self.dirName + '/LyraeData.dat')
        os.remove(self.dirName + '/out.bat')
        os.remove(self.dirName + '/period04freqs.txt')
        os.rmdir(self.dirName)
