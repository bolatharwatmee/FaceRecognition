from PyQt5 import QtWidgets , QtGui ,QtCore
from  main_interface import Ui_MainWindow
from add_new_photos import cameraManger
import sqlite3
import sys
from trainingThread import trainingManger
from  camera_detector import cameraDetector
class mainWindowInterface(QtWidgets.QMainWindow , Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        self.namevalid.setVisible(False)
        self.nidvalid.setVisible(False)
        self.face_model_name = "faces.xml"
        self.trainer = trainingManger(self.face_model_name)
        self.trainer.finished.connect(self.unfreazeapp)
        self.appStackedPages.setCurrentIndex(0)
        self.databaseName = "FACE_RECOGNITION_APP"
        self.app_table_name = "FACE_RECOGNITION_USERS"
        name_validator = QtGui.QRegExpValidator(QtCore.QRegExp("[a-z A-Z]+"))
        self.nameLin.setValidator(name_validator)
        self.addBtn.clicked.connect(self.goto_add_new_user_window)
        self.BackButton.clicked.connect(self.goto_Main_Menu)
        self.addTrainingImagesBtn.clicked.connect(self.collect_data_set)
        self.camera_ref = cameraManger(self.imageViewerLbl)
        self.camera_ref.finished.connect(self.training_finshed)
        self.saveUserBtn.clicked.connect(self.validate_user_data)
        self.check_databaseExistance()
        self.trainBtn.clicked.connect(self.startDataTraining)
        self.checkBtn.clicked.connect(self.start_detection)
        self.show()

    def goto_add_new_user_window(self):
        self.appStackedPages.setCurrentIndex(1)
        self.is_images_taken = False

    def goto_Main_Menu(self):
        self.appStackedPages.setCurrentIndex(0)


    def collect_data_set(self):
        user_name = self.nameLin.text()
        if(len(user_name)>=12):
            self.camera_ref.set_user_name(user_name)
            self.camera_ref.start()
        else:
            self.show_warning_message_dialog("registration error", "enter valid name first")

    def training_finshed(self):
        self.is_images_taken = True

    def validate_user_data(self):
        if not self.is_images_taken:
            self.show_warning_message_dialog("registration error" , "select dataset first")
            return None
        if len(self.lnidLin.text())<14:
            self.show_warning_message_dialog("registration error", "nid must be =14")
            return None
        if len(self.addressLin.text())<10:
            self.show_warning_message_dialog("registration error", "pls insert valid address")
            return None

        user_dict = {'user_name': self.nameLin.text()
                   , 'user_address': self.addressLin.text(),
                     'user_nid': self.lnidLin.text(),
                     'user_gender': 'male' if self.maleCheckOpt.isChecked() else 'female'
                     }
        self.insert_user(user_dict)
        print("all good.............")

        self.appStackedPages.setCurrentIndex(0)

    def insert_user(self , user):
        connection = sqlite3.connect(self.databaseName)
        sql_qur = '''INSERT INTO  {} (user_name , ADDRESS , user_nid , gender) values('{}' , '{}' , '{}' , '{}') '''.format(
            self.app_table_name,
            user['user_name'],
            user['user_address'],
            user['user_nid'],
            user['user_gender'])
        connection.execute(sql_qur)
        connection.commit()
        connection.close()
    def show_warning_message_dialog(self , title, body):
        messageBox = QtWidgets.QMessageBox()
        messageBox.setIcon(QtWidgets.QMessageBox.Warning)
        messageBox.setWindowTitle(title)
        messageBox.setText(body)
        messageBox.exec_()
    def startDataTraining(self):
        self.trainer.start()
        self.setDisabled(True)

    def unfreazeapp(self):
        self.setDisabled(False)

    def check_databaseExistance(self):
        connection = sqlite3.connect(self.databaseName)
        is_table_exist_qur = "SELECT name FROM sqlite_master WHERE type='table';"
        rows = connection.execute(is_table_exist_qur)
        is_table_exist = False
        for row in rows:
            if self.app_table_name in row[0]:
                is_table_exist = True
                print("table is already existed...")
        if is_table_exist == False:
            print("new table created")

            creat_table_qur ='''CREATE TABLE {}
             (ID INTEGER PRIMARY KEY AUTOINCREMENT,
             user_name           TEXT    NOT NULL,
             user_nid            CHAR(16)     NOT NULL,
             ADDRESS             CHAR(100)    NOT NULL,
             gender              CHAR(10)     NOT NULL);'''.format(self.app_table_name)
            connection.execute(creat_table_qur)
        connection.close()


    def start_detection(self):
        self.detector = cameraDetector(self.camera_viewer)
        self.detector.start()
        self.appStackedPages.setCurrentIndex(2)


app = QtWidgets.QApplication(sys.argv)
main_window = mainWindowInterface()
app.exec_()