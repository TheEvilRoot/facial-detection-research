import sys
import cv2
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore

from detect import process

def pix_from_file(file, widget):
    return QPixmap(file).scaled(widget.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)

app = QApplication(sys.argv[1:])
window = QMainWindow()
root = QWidget()
layout = QVBoxLayout()

source_image = None

source_image_view = QLabel('Source placeholder')
source_image_view.setMaximumHeight(300)
source_image_view.setScaledContents(False)

result_image_view = QLabel('Result placeholder')
result_image_view.setMaximumHeight(300)
result_image_view.setScaledContents(False)

layout.addWidget(source_image_view)
layout.addWidget(result_image_view)

select_file_label = QLabel("Select file")
layout.addWidget(select_file_label)

def select_click(button):
    global source_image
    data = QFileDialog.getOpenFileName(window, 'Open image', '~', 'Image files (*.jpg *.png)')
    if data is None:
        return
    file_name, _ = data
    if file_name is None or len(file_name) == 0:
        return
    source_image = file_name
    source_image_view.setPixmap(pix_from_file(file_name, source_image_view))

def submit_click(button):
    if source_image is None:
        return
    image = cv2.imread(source_image) 
    image = process(image)
    height, width, channel = image.shape 
    bpl = 3 * width
    qimage = QImage(image.data, width, height, bpl, QImage.Format_RGB888).rgbSwapped()
    result_image_view.setPixmap(QPixmap(qimage).scaled(result_image_view.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))

select_button = QPushButton("Select")
select_button.clicked.connect(lambda: select_click(select_button)) 
layout.addWidget(select_button)

submit_button = QPushButton("Process")
submit_button.clicked.connect(lambda: submit_click(submit_button))
layout.addWidget(submit_button)

root.setLayout(layout)

window.setWindowTitle('Facial detection')
window.setMinimumWidth(900)
window.setMinimumHeight(600)
window.setCentralWidget(root)
window.show()
app.exec_()

