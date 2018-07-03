import cv2
import numpy as nu
from matplotlib import pyplot as plt

cap = cv2.VideoCapture(1)
if cap.isOpened() == False:
    quit()

while True:
    _, frame = cap.read()

    color = ('b', 'g', 'r')
    for i, col in enumerate(color):
        histr = cv2.calcHist([frame],[i],None, [265], [0,256])
        plt.plot(histr, color = col)
        plt.xlim([0, 256])
    plt.show()

    if cv2.waitKey(30) >= 0:
        break

        
