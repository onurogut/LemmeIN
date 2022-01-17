import cv2
import numpy as np
import face_recognition
import os
import time
from datetime import datetime
import sqlite3 as sql

vt = sql.connect('ogrenciler.sqlite')
path = 'ogrenciler'
images = []
classNames = []
myList = os.listdir(path)
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)
def findEncodings(images):
    encodeList = []


    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

encodeListKnown = findEncodings(images)
print('Yüzler tanındı')

def markAttendance(name):
    with open('yoklama.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
            if name not in nameList:
                now = datetime.now()
                dtString = now.strftime('%H:%M:%S')
                f.writelines(f'\n{name},{dtString}')
                print ("yeni ogrenci bekleniyor.")
                db = sql.connect("ogrenciler.sqlite")
                cs= db.cursor()
                cs.execute("insert into girisler values (?, ?, ?)",(name,dtString,cs.lastrowid))
                db.commit()
                cv2.destroyAllWindows()
                cv2.waitKey(0)
                time.sleep(1)
                break

faceDetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
class Video(object):
    def __init__(self):
        self.video=cv2.VideoCapture(1)
    def __del__(self):
        self.video.release()
    def get_frame(self):
        ret,frame=self.video.read()
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
            success, img = self.video.read()
            imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)    
            facesCurFrame = face_recognition.face_locations(imgS)
            encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)
            for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
                matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
                matchIndex = np.argmin(faceDis)
                if matches[matchIndex]:
                    name = classNames[matchIndex].upper()
                    markAttendance(name)
                    print (name)
                break
            cv2.imshow("Kontrol Penceresi", img)
            cv2.waitKey(1)
        ret,jpg=cv2.imencode('.jpg',frame)
        return jpg.tobytes()


    
        

