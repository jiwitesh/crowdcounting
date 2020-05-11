import base64
import errno
import os
import shutil


def checkIfInputFolderExist(path, userName):
    try:
        # if os.path.isdir("ids/" + userName):
        if os.path.isdir(path + "/" + userName):
            shutil.rmtree(path + "/" + userName)
            return path + "/" + userName + ".....deleted successfully.\n"
        else:
            print('File does not exists. ')
    except OSError as s:
        print(s)


def deleteExistingTrainingFolder(path):
    try:
        # if os.path.isdir("ids/" + userName):
        if os.path.isdir(path):
            shutil.rmtree(path)
            return path + ".....deleted successfully.\n"
        else:
            print('File does not exists. ')
    except OSError as s:
        print(s)


def decodeImage(imgstring, imageLoc):
    imgdata = base64.b64decode(imgstring)

    with open(imageLoc, 'wb') as f:
        f.write(imgdata)
        f.close()


def checkIfInputFileExist(imageLoc):
    if os.path.exists(imageLoc):
        os.remove(imageLoc)
    else:
        return 'File does not exists'


def createDirectoryForTrainingImages(userId, projectId):
    try:
        path = os.path.join("data/", userId)
        if not os.path.isdir(path):
            os.makedirs(path)

        path = os.path.join(path, projectId)
        if not os.path.isdir(path):
            os.makedirs(path)
    except OSError as ex:
        if ex.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            pass
