import os
import glob


def remove_auto_graphs():
    file_list = glob.glob("../graphs/auto_graph*.txt")
    for filePath in file_list:
        try:
            os.remove(filePath)
        except FileNotFoundError:
            print("File not found : ", filePath)
