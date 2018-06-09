import cv2
from PyQt5 import QtCore
import numpy
import os
import pickle
class trainingManger(QtCore.QThread):
    def __init__(self , model_name):
        QtCore.QThread.__init__(self)
        self.__model_name = model_name
    def run(self):
        face_recognizer = cv2.face.createLBPHFaceRecognizer()
        BASE_FOLDER = os.path.join(os.getcwd(), "dataSet")
        input_images = []
        output_lables = []
        output_lables_names = []
        available_users = os.listdir(BASE_FOLDER)
        for user_folder_name in available_users:
            user_folder_path = os.path.join(BASE_FOLDER, user_folder_name)
            for image_name in os.listdir(user_folder_path):
                if image_name.endswith("png") or image_name.endswith("pgm"):
                    image_path = os.path.join(user_folder_path, image_name)
                    img = cv2.imread(image_path, 0)
                    input_images.append(img)
                    if user_folder_name not in output_lables_names:
                        output_lables_names.append(user_folder_name)
                    user_index = output_lables_names.index(user_folder_name)
                    output_lables.append(user_index)

        input_images_array = numpy.array(input_images)
        output_labels_array = numpy.array(output_lables)
        pickle.dump(output_lables_names , open("faces_names" , 'wb') )
        print(output_lables_names )
        face_recognizer.train(input_images_array, output_labels_array)
        face_recognizer.save(self.__model_name)

