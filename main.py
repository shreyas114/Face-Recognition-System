import cv2
import numpy as np
import sqlite3

# Load Haar Cascade for face detection
faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Initialize webcam
cam = cv2.VideoCapture(0)

def insertorupdate(Id, Name, age):
    conn = sqlite3.connect("sqlite.db")
    cmd = "SELECT * FROM STUDENTS WHERE ID=?"
    cursor = conn.execute(cmd, (Id,))
    isRecordExist = 0
    for row in cursor:
        isRecordExist = 1
    if isRecordExist == 1:
        conn.execute("UPDATE STUDENTS SET NAME=?, age=? WHERE ID=?", (Name, age, Id))
    else:
        conn.execute("INSERT INTO STUDENTS (Id, Name, age) VALUES (?, ?, ?)", (Id, Name, age))
    conn.commit()
    conn.close()

# Get user input
Id = input('Enter User Id: ')
Name = input("Enter User Name: ")
age = input("Enter User Age: ")

# Insert or update the user information in the database
insertorupdate(Id, Name, age)

# Detect faces and save images
sampleNum = 0
while True:
    ret, img = cam.read()
    if not ret:
        print("Failed to grab frame")
        break
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceDetect.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        sampleNum += 1
        cv2.imwrite(f"dataset/user.{Id}.{sampleNum}.jpg", gray[y:y+h, x:x+w])
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 0), 2)
        cv2.waitKey(400)
    cv2.imshow("Face", img)
    cv2.waitKey(1);
    if sampleNum >= 20:
        break

cam.release()
cv2.destroyAllWindows()
