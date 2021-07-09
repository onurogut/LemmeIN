import cv2 

video=cv2.VideoCapture(0)

faceDetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

while True:
    ret,frame=video.read()
    faces=faceDetect.detectMultiScale(frame, 1.3, 5)
    for x,y,w,h in faces:
        x1,y1=x+w, y+h
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 1)
        cv2.line(frame, (x,y), (x+30, y),(0,255,0), 6) #Top Left
        cv2.line(frame, (x,y), (x, y+30),(0,255,0), 6)

        cv2.line(frame, (x1,y), (x1-30, y),(0,255,0), 6) #Top Right
        cv2.line(frame, (x1,y), (x1, y+30),(0,255,0), 6)

        cv2.line(frame, (x,y1), (x+30, y1),(0,255,0), 6) #Bottom Left
        cv2.line(frame, (x,y1), (x, y1-30),(0,255,0), 6)

        cv2.line(frame, (x1,y1), (x1-30, y1),(0,255,0), 6) #Bottom right
        cv2.line(frame, (x1,y1), (x1, y1-30),(0,255,0), 6)

    cv2.imshow("Frame", frame)
    k=cv2.waitKey(1)
    if k==ord('q'):
        break
video.release()
cv2.destroyAllWindows()