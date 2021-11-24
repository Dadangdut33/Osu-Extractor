import os
from os import listdir
from os.path import isfile, join
import shutil

path = "C:\Games\Osu\Songs"

list_subfolders_with_paths = [f.path for f in os.scandir(path) if f.is_dir()]

print(list_subfolders_with_paths)

print(len(list_subfolders_with_paths))

onlyfiles = [f for f in listdir(list_subfolders_with_paths[0]) if isfile(join(list_subfolders_with_paths[0], f))]

print(onlyfiles)
print(len(onlyfiles))

# Find mp3 file
for file in onlyfiles:
    if file.endswith(".mp3"):
        print(file)
        print(list_subfolders_with_paths[0])
        print(list_subfolders_with_paths[0] + "\\" + file)
        shutil.copy2(list_subfolders_with_paths[0] + "\\" + file, f".\output\song\\test.mp3")
        break