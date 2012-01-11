
'''
Created on 20 May 2011

@author: jjm20
'''
class EPrimeParser():
    header = {}
    experimentalLists = {}
   
    def __buildBlock(self, line, dataBlock):

        lineComponents = [substr.strip() for substr in line.split(':')]
       
        if lineComponents[0] in dataBlock:
            if type(dataBlock[lineComponents[0]]) is list:
                dataBlock[lineComponents[0]].append(lineComponents[1])
            else:
                dataBlock[lineComponents[0]] = [dataBlock[lineComponents[0]],lineComponents[1]]
        else:
            dataBlock[lineComponents[0]] = lineComponents[1]
        return dataBlock
   
    def __getDistinctIdentifiers(self, trialDict):
       
        uniqueIdentifiers = set()
        for key in trialDict:
            keyComponents = key.split('.')
            uniqueIdentifiers.add(keyComponents[0])
           
        return uniqueIdentifiers
           
    def __getIdentierAttributes(self, identifier, trialDict):
       
        attributeDict = {}
        for key in trialDict:
            if key.startswith(identifier):
                keyComponents = key.split('.')
                if len(keyComponents) > 1 :
                    attributeDict[keyComponents[1]] = trialDict[key]
        return attributeDict
       
         
   
   
    def __createTrialDict(self,trialDict):
        uniqueIdentifiers = self.__getDistinctIdentifiers(trialDict)
       
        loggingObjects = {}
        attributes = {}
       
        outputData = {'loggingObjects':loggingObjects, 'attributes':attributes}
        for identifier in uniqueIdentifiers:
            identifierAttributes = self.__getIdentierAttributes(identifier, trialDict)
           
            if len(identifierAttributes) > 0:
                if 'ACC' in identifierAttributes or 'OnsetDelay' in identifierAttributes:
                    loggingObjects[identifier]=(identifierAttributes)
                elif 'Sample' in identifierAttributes and 'Cycle' in identifierAttributes:
                    outputData['Sample'] = identifierAttributes['Sample']
                    outputData['Cycle'] = identifierAttributes['Cycle']
                    outputData['list'] = identifier
                   
            else:
                if identifier != 'Running' and identifier != 'Procedure' and identifier != 'Group':
                    attributes[identifier] = trialDict[identifier]
                   
        return outputData        
       
    def __init__(self, dataFile):
   
        import codecs
       
        self.experimentalLists = {}
        self.header = {}
        currentDataBlock = {}
        currentLevel = 0
       
        datalist = []
        for line in codecs.open(dataFile, encoding='utf-16'):
       
            line = line.strip()
            if line.startswith("***"):
                #its a marker line
                line = line.replace('*','')
               
                marker = [substr.strip() for substr in line.strip().split(' ')]
                if marker[1] == 'Start':
                    #its the start of a new block
                    currentDataBlock['level'] = currentLevel
                   
                else:
                    #its the end of this block
                    if marker[0] == 'Header':
                        self.header = currentDataBlock
                        currentDataBlock = {}
                    else:
                        datalist.append(currentDataBlock)
                        currentDataBlock = {}
                       
            elif line.startswith('Level:'):
                currentLevel = [substr.strip() for substr in line.split(':')][1]
            else:
                self.__buildBlock(line,currentDataBlock)            
                   
        trialList = [self.__createTrialDict(trialDict) for trialDict in datalist]
   
        for trial in trialList:
            if 'list' in trial:
                if trial['list'] in self.experimentalLists:
                    self.experimentalLists[trial['list']].append(trial)
                else:
                    self.experimentalLists[trial['list']] = [trial]
       
   
   
   
   
    def getExperimentalLists(self):
        return self.experimentalLists
   
    def getHeader(self):
        return self.header
   
   



