import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QButtonGroup
from PIL import ImageQt
from User_interface import Ui_MainWindow
from Core import main

class MyWidget(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.correction_level = 1
        self.encoding_type = 'UTF8'
        self.image = None
        
        self.button_group = QButtonGroup()
        self.button_group.addButton(self.digit_button)
        self.button_group.addButton(self.alphadigit_button)
        self.button_group.addButton(self.UTF8_button)    
        
        self.GenerateButton.clicked.connect(self.generate)
        self.SaveButton.clicked.connect(self.save)
        self.CorrectionSlider.valueChanged.connect(self.change_level)
        self.button_group.buttonClicked.connect(self.encode_choice)
        
    def generate(self):
        data = self.DataEdit.toPlainText()
        response, self.image = main(data, self.encoding_type, self.correction_level)
        
        if response == 0:
            self.ErrorLine.setText('Присутствуют недопустимые символы')
            
        elif response == 1:
            self.ErrorLine.setText('Недопустимый объём данных')
            
        else:
            self.ErrorLine.setText('Код сгенерирован успешно')
            self.PictureLabel.setPixmap(ImageQt.toqpixmap(self.image))
        
    def save(self):
        if self.image == None:
            self.ErrorLine.setText('Отсутствует код для сохранения')
            
        else:
            path = self.PathLine.text()
            
            try:
                if os.path.exists(path):
                    os.remove(path)
                self.image.save(path)
                    
            except Exception:
                self.ErrorLine.setText('Проверьте правильность указанного пути')
                
            else:
                self.ErrorLine.setText('Успешно сохранено')               
                                
    def change_level(self, number):
        self.correction_level = number
        
    def encode_choice(self, button):
        if button == self.digit_button:
            self.encoding_type = 'digit'
            
        elif button == self.alphadigit_button:
            self.encoding_type = 'alphadigit'
            
        else:
            self.encoding_type = 'UTF8'
        
 
app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())