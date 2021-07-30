from zipfile import ZipFile
import os
from os.path import basename
from datetime import datetime

with ZipFile("archived_" + datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p") + ".zip", 'w') as zipObj:
   for folderName, subfolders, filenames in os.walk('/home/pi/Desktop'):
      for filename in filenames:
        if 'recordings_' in filename:
          filePath = os.path.join(folderName, filename)
          zipObj.write(filePath, basename(filePath))
          print("Zipped: " + basename(filePath))
          os.remove(filePath)
        if 'images_' in filename:
          filePath = os.path.join(folderName, filename)
          zipObj.write(filePath, basename(filePath))
          print("Zipped: " + basename(filePath))
          os.remove(filePath)

