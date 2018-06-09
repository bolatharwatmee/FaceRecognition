import cv2
from PyQt5 import QtCore , QtGui
import os
import sys
import serial
import pickle
class cameraDetector(QtCore.QThread):
    def __init__(self , window_):
        QtCore.QThread.__init__(self)
        self.window_viewer =  window_
    def run(self):
        CAMERA_INDEX = 0  # the default camera index is 0
        camera = cv2.VideoCapture(CAMERA_INDEX)
        if not camera.isOpened():
            print("please check the camera...")
            sys.exit(1)
        faceClassifier = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
        face_recognizer = cv2.face.createLBPHFaceRecognizer()
        face_recognizer.load('faces.xml')
        users = pickle.load(open("faces_names" , 'rb'))
        arduino_board = serial.Serial("/dev/ttyACM0" , 9600)
        while True:
            is_suc, image = camera.read()
            if is_suc:
                gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                faces = faceClassifier.detectMultiScale(gray_image)
                if len(faces) > 0:
                    for face in faces:
                        x, y, w, h = face[0], face[1], face[2], face[3]
                        pt1 = (x, y)
                        pt2 = (x + w, y + h)
                        cv2.rectangle(image, pt1, pt2, color=(255, 255, 0), thickness=2)
                        sub_image = gray_image[y:y + h, x:x + w]
                        result = face_recognizer.predict(sub_image)
                        user_name = users[result]
                        if "yale"  in user_name :
                            arduino_board.write(b'b')
                            user_name = "none"
                        else:
                            arduino_board.write(b'a')
                        cv2.putText(image, user_name, pt1, cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.8, color=(0, 255, 0))

                cv2.imwrite( "temp.png",image )
                self.window_viewer.setPixmap(QtGui.QPixmap("temp.png"))
        camera.release()
        cv2.destroyAllWindows()
        arduino_board.close()
