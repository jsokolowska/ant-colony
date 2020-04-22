import os
import glob

file_list = glob.glob("../graphs/auto_graph*.txt")
for filePath in file_list:
    try:
        os.remove(filePath)
    except FileNotFoundError:
        print("File not found : ", filePath)