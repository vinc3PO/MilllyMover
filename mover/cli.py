import shutil
import os

def findFileinFolder(path=None, result=None, extensionList=None):
    if not result:
        result = []
        extensionList = []
    for dirPath in os.listdir(path):
        if os.path.isfile(os.path.join(path, dirPath)):
            extension = os.path.splitext(dirPath)[1]
            if extension and len(extension) < 5 :
                result.append(os.path.join(path, dirPath))
                if extension not in extensionList:
                    extensionList.append(extension)
        else:
            result, extensionList = findFileinFolder(os.path.join(path, dirPath), result, extensionList)
    return result, extensionList
