import cv2
from PyQt5 import QtCore , QtGui
import os
class cameraManger(QtCore.QThread):
    def __init__(self , window_):
        QtCore.QThread.__init__(self)
        self.user_name = ""
        self.window_viewer =  window_
    def set_user_name(self , user_name):
        self.user_name = user_name
    def run(self):
        BASE_FOLDER = "dataSet"
        USER_NAME = self.user_name
        folder_path = os.path.join(os.getcwd(), BASE_FOLDER, USER_NAME)
        if not os.path.isdir(folder_path):
            os.makedirs(folder_path)
        WANTED_IMAGES = 100
        curent_image_counter = 0
        CAMERA_INDEX = 0  # the default camera index is 0
        camera = cv2.VideoCapture(CAMERA_INDEX)
        faceClassifier = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
        while True:
            is_suc, image = camera.read()
            if is_suc:
                file_name = os.path.join(folder_path, "image_{}.png".format(curent_image_counter))
                if curent_image_counter >= WANTED_IMAGES:
                    print("done collecting images...")
                    break
                gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                faces = faceClassifier.detectMultiScale(gray_image)

                if len(faces) == 1:
                    for face in faces:
                        x, y, w, h = face[0], face[1], face[2], face[3]
                        pt1 = (x, y)
                        pt2 = (x + w, y + h)
                        cv2.rectangle(image, pt1, pt2, color=(255, 255, 0), thickness=2)
                        sub_image = gray_image[y:y + h, x:x + w]
                        cv2.imwrite(file_name, sub_image)
                        self.window_viewer.setPixmap(QtGui.QPixmap(file_name))
                        curent_image_counter += 1

        camera.release()
        cv2.destroyAllWindows()
