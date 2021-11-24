import os
from osu_extractor.GetData import getSubFolder, getAllItemsInFolder, getFolderName, extractFiles

dir_path = os.path.dirname(os.path.realpath(__file__))

path = "C:\Games\Osu\Songs"

beatmapsPath = getSubFolder(path)
print(len(beatmapsPath))

# # Tests
# beatmap_3 = getAllItemsInFolder(beatmapsPath[3])

# extractFiles(beatmapsPath[3], beatmap_3, ".jpg", dir_path + "\\output\\img\\")