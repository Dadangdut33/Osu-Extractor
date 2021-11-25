import os
from os import listdir
from os.path import isfile, join
import shutil
from termcolor import colored

def getSubFolder(path):
    return [f.path for f in os.scandir(path) if f.is_dir()]

def getAllItemsInFolder(path):
    return [f for f in listdir(path) if isfile(join(path, f))]

def getFolderName(path):
    return path.split("\\")[-1]

def extractFiles(root, itemInsideFolder, type, outputDirPlusName):
    print(colored(f"Extracting {type} files from {root}", "green"))
    for file in itemInsideFolder:
        if file.endswith(type):
            shutil.copy2(root + "\\" + file, outputDirPlusName)

def createPathIfNotExist(path):
    if not os.path.exists(path):
        os.makedirs(path)

def keepCertainListByKeyword(list, keyWord):
    keyWord = keyWord.lower() # Case insensitive
    return [item for item in list if keyWord in item.lower()]