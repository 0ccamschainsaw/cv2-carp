import cv2
import numpy as np
import pickle

#manual method to select parking spaces, as irregularities present. plus camera remains in the same place.
w, h = 110, 49

try:
    with open('CarParkPos', 'rb') as file:
        poslist = pickle.load(file)
except:
    poslist = []

def mouseClick(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:
        poslist.append((x,y))
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(poslist):   #i is iteration number
            x1, y1 = pos
            if x1 < x < x + w and y1 < y < y + h :
                poslist.pop(i)
    with open('CarParkPos', 'wb') as file:
        pickle.dump(poslist, file)
        

while True:
    img = cv2.imread('assets\carParkImg.png', -1)
    for pos in poslist:
        cv2.rectangle(img, pos, (pos[0]+w, pos[1]+h), (255,0,255), 2)        #w = 110, h = 49
    
    cv2.imshow('Image', img)
    cv2.setMouseCallback('Image', mouseClick) 
    cv2.waitKey(1)
    if cv2.waitKey(1) == ord('q'):
        break