from typing import List
from random import randrange


def readCompleteInstance(filename, deleteLines):
    file = open(filename, 'r')
    lines = file.readlines()
    citys = readCitys()

    count = 0
    newLines: List[List[str]] = []
    for line in lines:
        if count >= deleteLines:
            components = line.split()
            components.append(citys[randrange(0, len(citys)-1)])
            newLines.append(components)
        count += 1

    return newLines

def readPartialInstance(filename, deleteLines):
    file = open(filename, 'r')
    lines = file.readlines()
    citys = readCitys()

    count = 0
    newLines: List[List[str]] = []
    width = None
    height = None
    for line in lines:
        if count >= deleteLines:
            components = line.split()
            components.append(width)
            components.append(height)
            components.append(citys[randrange(0, len(citys) - 1)])

            newLines.append(components)
        else:
            components = line.split()
            if len(components) != 0 and components[0] == "%Labelsize:":
                width = components[1]
                height = components[2]
        count += 1

    return newLines


def readCitys():
    file = open("../res/city_names.txt", 'r')
    citys = file.readlines()
    for i in range(len(citys)):
        citys[i] = citys[i].strip()
    return citys
