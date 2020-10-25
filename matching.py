#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  4 12:37:39 2020

@author: Trang
"""

import pandas as pd
from fuzzywuzzy import fuzz
import re

#Read data
orbis = pd.read_csv('bioo.csv')
print (orbis)
patstat = pd.read_csv('patstat.csv')
print (patstat)

"""
orbisMap = {}
'Accenture'
'A'
orbisMap['A'] = None
orbisMap = {
        'A' : []
}
orbisMap = {
        'A' : ['Accenture']
}
'Barclays'
orbisMap = {
        'A' : ['Accenture'],
        'B' : ['Barclays]
}
'Amazon'
orbisMap = {
        'A' : ['Accenture', 'Amazon'],
        'B' : ['Barclays]
}
"""

orbisMap = {}
for index, row in orbis.iterrows():
    name = row['Company name Latin alphabet']
    firstChar = name[0]
    if firstChar not in orbisMap:
        orbisMap[firstChar] = []
    orbisMap[firstChar].append(row)

print(orbisMap['A'][0]['Company name Latin alphabet'])
#For each row in patstat
#Find a match in orbis with partial = 100%
#Pull matching data from orbis to patstat
#Produce results with both orbis and patstat data + matching score

def getMatchingScore(pair):
    partialRatio = fuzz.partial_ratio(*pair)
    fuzzRatio = fuzz.ratio(*pair)
    tokenRatio = fuzz.token_sort_ratio(*pair)
    return (partialRatio,fuzzRatio, tokenRatio)

passtatFormatName = []
orbisNameList = []
partialScoreList = []
fuzzRatioList = []
tokenRatioList = []
orbisIdList = []

        
def scrubbing(name):
    re.sub('[^A-Za-z0-9]+', '', name)
    m = re.search('.*(?=(\s)+((L|l)(I|i)(M|m)(I|i)(T|t)(E|e)(D|d)|(L|l)(T|t)(D|d)|(P|p)(L|l)(C|c)|(L|l)(L|l)(C|c)|(I|i)(N|n)(C|c)))', name)
    if (m == None):
        return name
    return m.group(0)

def formatName(name):
    name = re.sub('[^A-Za-z0-9\s]+', '', name)
    name = re.sub('([Ll][Tt][Dd](\.)*(\,)*)', 'LIMITED', name)
    return name;

for patstatIndex, patstatRow in patstat.iterrows():
    patstatName = formatName(patstatRow['applicants'])
    firstChar = patstatName[0]
    print('finding {}..'.format(patstatName))
    matchingScore = ()
    hasMatch = False
    for orbisRow in orbisMap[firstChar]:
        orbisName = formatName(orbisRow['Company name Latin alphabet'])
        orbisId = orbisRow['BvD ID number']
        matchingScore = getMatchingScore((patstatName, orbisName))
        if matchingScore[0] == 100 and matchingScore[1] > 70:
            passtatFormatName.append(patstatName)
            orbisNameList.append(orbisName)
            partialScoreList.append(matchingScore[0])
            fuzzRatioList.append(matchingScore[1])
            tokenRatioList.append(matchingScore[2])
            orbisIdList.append(orbisId)
            hasMatch = True
            break
        
    if (hasMatch == False):
        passtatFormatName.append('')
        orbisNameList.append('')
        orbisIdList.append('')
        partialScoreList.append(0)
        fuzzRatioList.append(0)
        tokenRatioList.append(0)


result = patstat.copy(deep = True)
result['passtatFormatName'] = passtatFormatName
result['OrbisName'] = orbisNameList
result['PartialRatio'] = partialScoreList
result['FuzzRatio'] = fuzzRatioList
result['tokenRatio'] = tokenRatioList
result['OrbisId'] = orbisIdList

print(result)
result.to_csv('out.csv')
