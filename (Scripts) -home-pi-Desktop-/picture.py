import cv2
from datetime import datetime
import time

cap = cv2.VideoCapture(0)
cap.set(3, 1920)
cap.set(4, 1088)
ret , frame = cap.read()

cv2.imwrite("images_" + datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p") + ".jpg", frame)
cv2.destroyAllWindows()

