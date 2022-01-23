# Internal
import os
from os.path import isfile, join
import shutil
# External
from termcolor import colored

def getSubFolder(path):
    return [f.path for f in os.scandir(path) if f.is_dir()]

def getAllItemsInFolder(path):
    return [f for f in os.listdir(path) if isfile(join(path, f))]

def getFileTypeListInFolder(path):
    lists = [f.name.split(".")[-1] for f in os.scandir(path) if f.is_file()]
    return list(set(lists)) # remove dupe

def getFolderName(path):
    return path.split("\\")[-1]

def extractFiles(root, itemInsideFolder, type, outputDir, beatMapName, printProgress=False):
    if printProgress:
        print(colored(f"\nExtracting {type} files from {root}", "green"))
    createPathIfNotExist(outputDir)
    for file in itemInsideFolder:
        if file.endswith(type):
            shutil.copy2(root + "\\" + file, outputDir + "\\" + f"{beatMapName} {file}")

def createPathIfNotExist(path):
    if not os.path.exists(path):
        os.makedirs(path)

def keepCertainListByKeyword(list, keyWord):
    return [item for item in list if keyWord.lower() in item.lower()]