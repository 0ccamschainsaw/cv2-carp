import cv2
import pickle
import numpy as np
import cvzone

cap = cv2.VideoCapture('assets\carPark.mp4')
w, h = 110, 49

with open('CarParkPos', 'rb') as file:
        poslist = pickle.load(file)

def checkparkspace(framepro):
     spaces = 0
     for pos in poslist:
        x, y = pos
        imgcrop = framepro[y:y+h, x:x+w]
        #cv2.imshow(str(x*y), imgcrop)  #shows each individual car space image

        count = cv2.countNonZero(imgcrop)
        cvzone.putTextRect(frame, str(count), (x+5, y+h-5), scale = 0.8,  thickness=1, offset=5, colorR=(200, 0, 200))
        if count < 450:
             color = (0, 200, 0)
             thicc = 7
             spaces += 1
        else :
             color = (0 , 0 , 200)
             thicc = 3

        cv2.rectangle(frame, (x,y), (x+w, y+h), color, thicc)
     cvzone.putTextRect(frame, f'Free: {spaces}/{len(poslist)}', (50, 60),scale = 2 , thickness=2, offset=10, colorR=(0, 200, 0))

while True:
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)                                         #loop video
    ret, frame = cap.read()
    framegray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frameblur = cv2.GaussianBlur(framegray, (3,3), 1)
    framethresh = cv2.adaptiveThreshold(frameblur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    frameMedian = cv2.medianBlur(framethresh, 5)
    kernel = np.ones((3, 3), np.uint8)
    frameDilate = cv2.dilate(framethresh, kernel, iterations=1)

    checkparkspace(frameMedian)
    #for pos in poslist:
         #cv2.rectangle(frame, pos, (pos[0]+w, pos[1]+h), (255,0,255), 1)        #for diplaying rectangles of parking spaces
    
    cv2.imshow('output', frame)
    cv2.waitKey(5)      #10 to slow down the video
    if cv2.waitKey(1) == ord('q'):
        break

#framethresh: adjust values so that the number of pixels in the  empty spaces is very very less comparedd to the occupied spaces
#framedilate: make pixels thicker, easy to detetct