import os
from os import listdir
from os.path import isfile, join
import shutil

def getSubFolder(path):
    return [f.path for f in os.scandir(path) if f.is_dir()]

def getAllItemsInFolder(path):
    return [f for f in listdir(path) if isfile(join(path, f))]

def getFolderName(path):
    return path.split("\\")[-1]

def extractFiles(root, itemInsideFolder, type, outputDir):
    print(f"Extracting {type} files from {root}")
    for file in itemInsideFolder:
        if file.endswith(type):
            shutil.copy2(root + "\\" + file, outputDir)