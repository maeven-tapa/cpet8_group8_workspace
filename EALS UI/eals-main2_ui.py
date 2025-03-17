# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'eals-main2.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QDateEdit, QFrame,
    QGridLayout, QGroupBox, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QMainWindow, QPushButton,
    QRadioButton, QSizePolicy, QSpacerItem, QStackedWidget,
    QTableWidget, QTableWidgetItem, QTextBrowser, QTextEdit,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1280, 734)
        MainWindow.setMinimumSize(QSize(0, 0))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setMinimumSize(QSize(1280, 720))
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.main_page = QWidget()
        self.main_page.setObjectName(u"main_page")
        self.gridLayout_2 = QGridLayout(self.main_page)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.line = QFrame(self.main_page)
        self.line.setObjectName(u"line")
        self.line.setMinimumSize(QSize(10, 0))
        self.line.setStyleSheet(u"border: 0px;")
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_2.addWidget(self.line, 0, 0, 2, 1)

        self.frame = QFrame(self.main_page)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(501, 684))
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_3 = QGridLayout(self.frame)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.frame_2 = QFrame(self.frame)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(481, 491))
        self.frame_2.setStyleSheet(u"border-radius: 0px;")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.lineEdit = QLineEdit(self.frame_2)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(380, 250, 431, 61))
        self.lineEdit.setStyleSheet(u"background-color: rgb(238, 238, 238);")
        self.lineEdit_2 = QLineEdit(self.frame_2)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setGeometry(QRect(380, 380, 441, 61))
        self.lineEdit_2.setStyleSheet(u"background-color: rgb(238, 238, 238);")
        self.pushButton = QPushButton(self.frame_2)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(840, 380, 71, 61))
        self.pushButton.setStyleSheet(u"background-color: rgb(204, 204, 204);")
        icon = QIcon()
        icon.addFile(u"../../Downloads/eye.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setIconSize(QSize(41, 47))
        self.login_btn = QPushButton(self.frame_2)
        self.login_btn.setObjectName(u"login_btn")
        self.login_btn.setGeometry(QRect(550, 470, 211, 41))
        self.login_btn.setStyleSheet(u"background-color: rgb(204, 204, 204);")
        self.label_3 = QLabel(self.frame_2)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(590, 30, 111, 91))
        self.label_3.setStyleSheet(u"background-color: rgb(241, 241, 241);")
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_4 = QLabel(self.frame_2)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(390, 220, 81, 16))
        self.label_5 = QLabel(self.frame_2)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(380, 340, 81, 16))
        self.label_6 = QLabel(self.frame_2)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(590, 150, 111, 20))
        self.label_6.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.frame_2, 0, 0, 1, 1)


        self.gridLayout_2.addWidget(self.frame, 0, 1, 2, 1)

        self.stackedWidget.addWidget(self.main_page)
        self.admin_changpass_page = QWidget()
        self.admin_changpass_page.setObjectName(u"admin_changpass_page")
        self.gridLayout_4 = QGridLayout(self.admin_changpass_page)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.verticalSpacer_3 = QSpacerItem(20, 44, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_4.addItem(self.verticalSpacer_3, 0, 2, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(78, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_2, 1, 0, 1, 1)

        self.frame_3 = QFrame(self.admin_changpass_page)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(1071, 491))
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.lineEdit_3 = QLineEdit(self.frame_3)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        self.lineEdit_3.setGeometry(QRect(90, 290, 881, 61))
        self.lineEdit_3.setStyleSheet(u"background-color: rgb(238, 238, 238);")
        self.label_7 = QLabel(self.frame_3)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(100, 260, 81, 16))
        self.label_8 = QLabel(self.frame_3)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(260, 130, 561, 54))
        font = QFont()
        font.setPointSize(28)
        self.label_8.setFont(font)
        self.label_8.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_9 = QLabel(self.frame_3)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(170, 190, 771, 29))
        font1 = QFont()
        font1.setPointSize(12)
        self.label_9.setFont(font1)
        self.label_9.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.change_pass_btn = QPushButton(self.frame_3)
        self.change_pass_btn.setObjectName(u"change_pass_btn")
        self.change_pass_btn.setGeometry(QRect(490, 400, 121, 41))
        self.change_pass_btn.setStyleSheet(u"background-color: rgb(204, 204, 204);")
        self.label_10 = QLabel(self.frame_3)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setGeometry(QRect(490, 40, 111, 91))
        self.label_10.setStyleSheet(u"background-color: rgb(241, 241, 241);")
        self.label_10.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.frame_3, 1, 1, 2, 3)

        self.horizontalSpacer_4 = QSpacerItem(77, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_4, 1, 4, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(78, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_3, 2, 0, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(77, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_5, 2, 4, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(78, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_6, 3, 0, 1, 1)

        self.frame_4 = QFrame(self.admin_changpass_page)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMinimumSize(QSize(1071, 81))
        self.frame_4.setStyleSheet(u"background-color: transparent;\n"
"border: None;")
        self.frame_4.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_4.addWidget(self.frame_4, 3, 1, 1, 3)

        self.horizontalSpacer_7 = QSpacerItem(77, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_7, 3, 4, 1, 1)

        self.verticalSpacer_4 = QSpacerItem(20, 44, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_4.addItem(self.verticalSpacer_4, 4, 1, 1, 1)

        self.verticalSpacer_5 = QSpacerItem(20, 44, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_4.addItem(self.verticalSpacer_5, 4, 3, 1, 1)

        self.stackedWidget.addWidget(self.admin_changpass_page)
        self.veri1_employee_page = QWidget()
        self.veri1_employee_page.setObjectName(u"veri1_employee_page")
        self.gridLayout_5 = QGridLayout(self.veri1_employee_page)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.line_6 = QFrame(self.veri1_employee_page)
        self.line_6.setObjectName(u"line_6")
        self.line_6.setMinimumSize(QSize(10, 0))
        self.line_6.setStyleSheet(u"border: 0px;")
        self.line_6.setFrameShape(QFrame.Shape.VLine)
        self.line_6.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_5.addWidget(self.line_6, 0, 0, 5, 1)

        self.line_4 = QFrame(self.veri1_employee_page)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setMinimumSize(QSize(10, 0))
        self.line_4.setStyleSheet(u"border: 0px;")
        self.line_4.setFrameShape(QFrame.Shape.HLine)
        self.line_4.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_5.addWidget(self.line_4, 0, 1, 1, 7)

        self.line_7 = QFrame(self.veri1_employee_page)
        self.line_7.setObjectName(u"line_7")
        self.line_7.setMinimumSize(QSize(10, 0))
        self.line_7.setStyleSheet(u"border: 0px;")
        self.line_7.setFrameShape(QFrame.Shape.VLine)
        self.line_7.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_5.addWidget(self.line_7, 0, 8, 5, 1)

        self.label_11 = QLabel(self.veri1_employee_page)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setMinimumSize(QSize(591, 541))
        self.label_11.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.label_11.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_5.addWidget(self.label_11, 1, 1, 1, 3)

        self.line_2 = QFrame(self.veri1_employee_page)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setMinimumSize(QSize(10, 0))
        self.line_2.setStyleSheet(u"border: 0px;")
        self.line_2.setFrameShape(QFrame.Shape.VLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_5.addWidget(self.line_2, 1, 4, 1, 1)

        self.frame_6 = QFrame(self.veri1_employee_page)
        self.frame_6.setObjectName(u"frame_6")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_6.sizePolicy().hasHeightForWidth())
        self.frame_6.setSizePolicy(sizePolicy)
        self.frame_6.setMinimumSize(QSize(591, 541))
        self.frame_6.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_6 = QGridLayout(self.frame_6)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.label_16 = QLabel(self.frame_6)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setMinimumSize(QSize(574, 511))
        self.label_16.setStyleSheet(u"background-color: rgb(241, 241, 241);")
        self.label_16.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_6.addWidget(self.label_16, 0, 0, 1, 3)

        self.label_17 = QLabel(self.frame_6)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setMinimumSize(QSize(261, 60))
        self.label_17.setStyleSheet(u"border: 1px solid black;")
        self.label_17.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_6.addWidget(self.label_17, 1, 0, 1, 1)

        self.frame_8 = QFrame(self.frame_6)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setStyleSheet(u"background-color: transparent;\n"
"border: none;")
        self.frame_8.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_8.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_6.addWidget(self.frame_8, 1, 1, 1, 1)

        self.label_18 = QLabel(self.frame_6)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setMinimumSize(QSize(121, 58))
        self.label_18.setStyleSheet(u"background-color: rgb(230, 230, 230);")
        self.label_18.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_6.addWidget(self.label_18, 1, 2, 1, 1)


        self.gridLayout_5.addWidget(self.frame_6, 1, 5, 1, 3)

        self.line_3 = QFrame(self.veri1_employee_page)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setMinimumSize(QSize(20, 0))
        self.line_3.setStyleSheet(u"border: 0px;")
        self.line_3.setFrameShape(QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_5.addWidget(self.line_3, 2, 1, 1, 7)

        self.label_12 = QLabel(self.veri1_employee_page)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setMinimumSize(QSize(101, 51))
        self.label_12.setMaximumSize(QSize(101, 16777215))
        self.label_12.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.label_12.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_5.addWidget(self.label_12, 3, 1, 1, 1)

        self.label_14 = QLabel(self.veri1_employee_page)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setMinimumSize(QSize(0, 0))
        self.label_14.setMaximumSize(QSize(101, 16777215))
        self.label_14.setStyleSheet(u"background-color: transparent;\n"
"border: none;")
        self.label_14.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_5.addWidget(self.label_14, 3, 2, 1, 1)

        self.label_13 = QLabel(self.veri1_employee_page)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setMinimumSize(QSize(781, 51))
        self.label_13.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.label_13.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_5.addWidget(self.label_13, 3, 3, 1, 3)

        self.label_15 = QLabel(self.veri1_employee_page)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setMinimumSize(QSize(0, 0))
        self.label_15.setMaximumSize(QSize(101, 16777215))
        self.label_15.setStyleSheet(u"background-color: transparent;\n"
"border: none;")
        self.label_15.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_5.addWidget(self.label_15, 3, 6, 1, 1)

        self.veri1_cancel_btn = QPushButton(self.veri1_employee_page)
        self.veri1_cancel_btn.setObjectName(u"veri1_cancel_btn")
        self.veri1_cancel_btn.setMinimumSize(QSize(101, 51))
        self.veri1_cancel_btn.setMaximumSize(QSize(101, 16777215))
        self.veri1_cancel_btn.setStyleSheet(u"background-color: rgb(204, 204, 204);")

        self.gridLayout_5.addWidget(self.veri1_cancel_btn, 3, 7, 1, 1)

        self.line_5 = QFrame(self.veri1_employee_page)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setMinimumSize(QSize(20, 0))
        self.line_5.setStyleSheet(u"border: 0px;")
        self.line_5.setFrameShape(QFrame.Shape.HLine)
        self.line_5.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_5.addWidget(self.line_5, 4, 1, 1, 7)

        self.stackedWidget.addWidget(self.veri1_employee_page)
        self.veri2_employee_page = QWidget()
        self.veri2_employee_page.setObjectName(u"veri2_employee_page")
        self.gridLayout_8 = QGridLayout(self.veri2_employee_page)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.line_13 = QFrame(self.veri2_employee_page)
        self.line_13.setObjectName(u"line_13")
        self.line_13.setMinimumSize(QSize(10, 0))
        self.line_13.setStyleSheet(u"border: 0px;")
        self.line_13.setFrameShape(QFrame.Shape.VLine)
        self.line_13.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_8.addWidget(self.line_13, 0, 0, 5, 1)

        self.line_12 = QFrame(self.veri2_employee_page)
        self.line_12.setObjectName(u"line_12")
        self.line_12.setMinimumSize(QSize(10, 0))
        self.line_12.setStyleSheet(u"border: 0px;")
        self.line_12.setFrameShape(QFrame.Shape.HLine)
        self.line_12.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_8.addWidget(self.line_12, 0, 1, 1, 5)

        self.line_11 = QFrame(self.veri2_employee_page)
        self.line_11.setObjectName(u"line_11")
        self.line_11.setMinimumSize(QSize(10, 0))
        self.line_11.setStyleSheet(u"border: 0px;")
        self.line_11.setFrameShape(QFrame.Shape.VLine)
        self.line_11.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_8.addWidget(self.line_11, 0, 6, 5, 1)

        self.frame_7 = QFrame(self.veri2_employee_page)
        self.frame_7.setObjectName(u"frame_7")
        sizePolicy.setHeightForWidth(self.frame_7.sizePolicy().hasHeightForWidth())
        self.frame_7.setSizePolicy(sizePolicy)
        self.frame_7.setMinimumSize(QSize(591, 541))
        self.frame_7.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_7 = QGridLayout(self.frame_7)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.label_21 = QLabel(self.frame_7)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setMinimumSize(QSize(574, 511))
        self.label_21.setStyleSheet(u"background-color: rgb(241, 241, 241);")
        self.label_21.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_7.addWidget(self.label_21, 0, 0, 1, 2)


        self.gridLayout_8.addWidget(self.frame_7, 1, 1, 1, 5)

        self.line_9 = QFrame(self.veri2_employee_page)
        self.line_9.setObjectName(u"line_9")
        self.line_9.setMinimumSize(QSize(20, 0))
        self.line_9.setStyleSheet(u"border: 0px;")
        self.line_9.setFrameShape(QFrame.Shape.HLine)
        self.line_9.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_8.addWidget(self.line_9, 2, 1, 1, 5)

        self.label_20 = QLabel(self.veri2_employee_page)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setMinimumSize(QSize(101, 51))
        self.label_20.setMaximumSize(QSize(101, 16777215))
        self.label_20.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.label_20.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_8.addWidget(self.label_20, 3, 1, 1, 1)

        self.label_19 = QLabel(self.veri2_employee_page)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setMinimumSize(QSize(0, 0))
        self.label_19.setMaximumSize(QSize(101, 16777215))
        self.label_19.setStyleSheet(u"background-color: transparent;\n"
"border: none;")
        self.label_19.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_8.addWidget(self.label_19, 3, 2, 1, 1)

        self.label_26 = QLabel(self.veri2_employee_page)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setMinimumSize(QSize(781, 51))
        self.label_26.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.label_26.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_8.addWidget(self.label_26, 3, 3, 1, 1)

        self.label_25 = QLabel(self.veri2_employee_page)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setMinimumSize(QSize(0, 0))
        self.label_25.setMaximumSize(QSize(101, 16777215))
        self.label_25.setStyleSheet(u"background-color: transparent;\n"
"border: none;")
        self.label_25.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_8.addWidget(self.label_25, 3, 4, 1, 1)

        self.veri2_cancel_btn = QPushButton(self.veri2_employee_page)
        self.veri2_cancel_btn.setObjectName(u"veri2_cancel_btn")
        self.veri2_cancel_btn.setMinimumSize(QSize(101, 51))
        self.veri2_cancel_btn.setMaximumSize(QSize(101, 16777215))
        self.veri2_cancel_btn.setStyleSheet(u"background-color: rgb(204, 204, 204);")

        self.gridLayout_8.addWidget(self.veri2_cancel_btn, 3, 5, 1, 1)

        self.line_8 = QFrame(self.veri2_employee_page)
        self.line_8.setObjectName(u"line_8")
        self.line_8.setMinimumSize(QSize(20, 0))
        self.line_8.setStyleSheet(u"border: 0px;")
        self.line_8.setFrameShape(QFrame.Shape.HLine)
        self.line_8.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_8.addWidget(self.line_8, 4, 1, 1, 5)

        self.stackedWidget.addWidget(self.veri2_employee_page)
        self.veri_employee_page = QWidget()
        self.veri_employee_page.setObjectName(u"veri_employee_page")
        self.gridLayout_20 = QGridLayout(self.veri_employee_page)
        self.gridLayout_20.setObjectName(u"gridLayout_20")
        self.verticalSpacer_6 = QSpacerItem(20, 38, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_20.addItem(self.verticalSpacer_6, 0, 1, 1, 1)

        self.verticalSpacer_7 = QSpacerItem(20, 38, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_20.addItem(self.verticalSpacer_7, 0, 2, 1, 1)

        self.horizontalSpacer_8 = QSpacerItem(53, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_20.addItem(self.horizontalSpacer_8, 1, 0, 1, 1)

        self.frame_31 = QFrame(self.veri_employee_page)
        self.frame_31.setObjectName(u"frame_31")
        self.frame_31.setMinimumSize(QSize(1121, 591))
        self.frame_31.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_31.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_19 = QGridLayout(self.frame_31)
        self.gridLayout_19.setObjectName(u"gridLayout_19")
        self.frame_32 = QFrame(self.frame_31)
        self.frame_32.setObjectName(u"frame_32")
        self.frame_32.setStyleSheet(u"background-color: transparent;\n"
"border: none;")
        self.frame_32.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_32.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_19.addWidget(self.frame_32, 0, 0, 1, 1)

        self.label_40 = QLabel(self.frame_31)
        self.label_40.setObjectName(u"label_40")
        self.label_40.setMinimumSize(QSize(130, 130))
        self.label_40.setMaximumSize(QSize(130, 130))
        self.label_40.setStyleSheet(u"background-color: rgb(241, 241, 241);")
        self.label_40.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_19.addWidget(self.label_40, 0, 1, 1, 1)

        self.frame_33 = QFrame(self.frame_31)
        self.frame_33.setObjectName(u"frame_33")
        self.frame_33.setStyleSheet(u"background-color: transparent;\n"
"border: none;")
        self.frame_33.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_33.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_19.addWidget(self.frame_33, 0, 2, 1, 1)

        self.label_38 = QLabel(self.frame_31)
        self.label_38.setObjectName(u"label_38")
        font2 = QFont()
        font2.setPointSize(28)
        font2.setBold(True)
        self.label_38.setFont(font2)
        self.label_38.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_19.addWidget(self.label_38, 1, 0, 1, 3)

        self.label_39 = QLabel(self.frame_31)
        self.label_39.setObjectName(u"label_39")
        self.label_39.setFont(font)
        self.label_39.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_19.addWidget(self.label_39, 2, 0, 1, 3)

        self.groupBox_4 = QGroupBox(self.frame_31)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setMinimumSize(QSize(1061, 301))
        self.gridLayout_18 = QGridLayout(self.groupBox_4)
        self.gridLayout_18.setObjectName(u"gridLayout_18")
        self.tableWidget = QTableWidget(self.groupBox_4)
        if (self.tableWidget.columnCount() < 3):
            self.tableWidget.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.horizontalHeader().setDefaultSectionSize(222)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)

        self.gridLayout_18.addWidget(self.tableWidget, 0, 0, 1, 1)


        self.gridLayout_19.addWidget(self.groupBox_4, 3, 0, 1, 3)


        self.gridLayout_20.addWidget(self.frame_31, 1, 1, 2, 3)

        self.horizontalSpacer_10 = QSpacerItem(52, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_20.addItem(self.horizontalSpacer_10, 1, 4, 1, 1)

        self.horizontalSpacer_9 = QSpacerItem(53, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_20.addItem(self.horizontalSpacer_9, 2, 0, 1, 1)

        self.horizontalSpacer_11 = QSpacerItem(52, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_20.addItem(self.horizontalSpacer_11, 2, 4, 1, 1)

        self.verticalSpacer_9 = QSpacerItem(20, 37, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_20.addItem(self.verticalSpacer_9, 3, 1, 1, 1)

        self.verticalSpacer_8 = QSpacerItem(20, 37, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_20.addItem(self.verticalSpacer_8, 3, 3, 1, 1)

        self.stackedWidget.addWidget(self.veri_employee_page)
        self.employee_enroll_page = QWidget()
        self.employee_enroll_page.setObjectName(u"employee_enroll_page")
        self.gridLayout_9 = QGridLayout(self.employee_enroll_page)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.frame_5 = QFrame(self.employee_enroll_page)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.frame_5.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_13 = QGridLayout(self.frame_5)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.groupBox_3 = QGroupBox(self.frame_5)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setMinimumSize(QSize(591, 221))
        self.groupBox_3.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.gridLayout_11 = QGridLayout(self.groupBox_3)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.frame_16 = QFrame(self.groupBox_3)
        self.frame_16.setObjectName(u"frame_16")
        self.frame_16.setMinimumSize(QSize(171, 0))
        self.frame_16.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_16.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_11.addWidget(self.frame_16, 0, 0, 2, 1)

        self.label_30 = QLabel(self.groupBox_3)
        self.label_30.setObjectName(u"label_30")
        self.label_30.setMinimumSize(QSize(190, 190))
        self.label_30.setStyleSheet(u"background-color: rgb(241, 241, 241);")

        self.gridLayout_11.addWidget(self.label_30, 0, 1, 2, 1)

        self.frame_18 = QFrame(self.groupBox_3)
        self.frame_18.setObjectName(u"frame_18")
        self.frame_18.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_18.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_11.addWidget(self.frame_18, 0, 2, 2, 1)

        self.frame_17 = QFrame(self.groupBox_3)
        self.frame_17.setObjectName(u"frame_17")
        self.frame_17.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_17.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_11.addWidget(self.frame_17, 0, 3, 1, 1)

        self.pushButton_7 = QPushButton(self.groupBox_3)
        self.pushButton_7.setObjectName(u"pushButton_7")
        self.pushButton_7.setMinimumSize(QSize(51, 51))
        self.pushButton_7.setMaximumSize(QSize(101, 16777215))
        self.pushButton_7.setStyleSheet(u"background-color: rgb(204, 204, 204);")

        self.gridLayout_11.addWidget(self.pushButton_7, 1, 3, 1, 1)


        self.gridLayout_13.addWidget(self.groupBox_3, 0, 0, 1, 1)

        self.groupBox = QGroupBox(self.frame_5)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setMinimumSize(QSize(551, 371))
        self.groupBox.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.gridLayout_12 = QGridLayout(self.groupBox)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.label_22 = QLabel(self.groupBox)
        self.label_22.setObjectName(u"label_22")

        self.gridLayout_12.addWidget(self.label_22, 0, 0, 1, 1)

        self.frame_9 = QFrame(self.groupBox)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setStyleSheet(u"background-color: transparent;\n"
"border: none;")
        self.frame_9.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_9.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_12.addWidget(self.frame_9, 0, 1, 1, 1)

        self.lineEdit_4 = QLineEdit(self.groupBox)
        self.lineEdit_4.setObjectName(u"lineEdit_4")
        self.lineEdit_4.setMinimumSize(QSize(491, 61))
        self.lineEdit_4.setStyleSheet(u"background-color: rgb(238, 238, 238);")

        self.gridLayout_12.addWidget(self.lineEdit_4, 1, 0, 1, 2)

        self.line_10 = QFrame(self.groupBox)
        self.line_10.setObjectName(u"line_10")
        self.line_10.setMinimumSize(QSize(0, 15))
        self.line_10.setFrameShape(QFrame.Shape.HLine)
        self.line_10.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_12.addWidget(self.line_10, 2, 0, 1, 2)

        self.label_23 = QLabel(self.groupBox)
        self.label_23.setObjectName(u"label_23")

        self.gridLayout_12.addWidget(self.label_23, 3, 0, 1, 1)

        self.frame_10 = QFrame(self.groupBox)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setStyleSheet(u"background-color: transparent;\n"
"border: none;")
        self.frame_10.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_10.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_12.addWidget(self.frame_10, 3, 1, 1, 1)

        self.lineEdit_5 = QLineEdit(self.groupBox)
        self.lineEdit_5.setObjectName(u"lineEdit_5")
        self.lineEdit_5.setMinimumSize(QSize(491, 61))
        self.lineEdit_5.setStyleSheet(u"background-color: rgb(238, 238, 238);")

        self.gridLayout_12.addWidget(self.lineEdit_5, 4, 0, 1, 2)

        self.line_14 = QFrame(self.groupBox)
        self.line_14.setObjectName(u"line_14")
        self.line_14.setMinimumSize(QSize(0, 15))
        self.line_14.setFrameShape(QFrame.Shape.HLine)
        self.line_14.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_12.addWidget(self.line_14, 5, 0, 1, 2)

        self.label_24 = QLabel(self.groupBox)
        self.label_24.setObjectName(u"label_24")

        self.gridLayout_12.addWidget(self.label_24, 6, 0, 1, 1)

        self.frame_12 = QFrame(self.groupBox)
        self.frame_12.setObjectName(u"frame_12")
        self.frame_12.setStyleSheet(u"background-color: transparent;\n"
"border: none;")
        self.frame_12.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_12.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_12.addWidget(self.frame_12, 6, 1, 1, 1)

        self.frame_11 = QFrame(self.groupBox)
        self.frame_11.setObjectName(u"frame_11")
        self.frame_11.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.frame_11.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_11.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame_11)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.radioButton = QRadioButton(self.frame_11)
        self.radioButton.setObjectName(u"radioButton")

        self.horizontalLayout.addWidget(self.radioButton)

        self.radioButton_2 = QRadioButton(self.frame_11)
        self.radioButton_2.setObjectName(u"radioButton_2")

        self.horizontalLayout.addWidget(self.radioButton_2)

        self.radioButton_3 = QRadioButton(self.frame_11)
        self.radioButton_3.setObjectName(u"radioButton_3")

        self.horizontalLayout.addWidget(self.radioButton_3)


        self.gridLayout_12.addWidget(self.frame_11, 7, 0, 1, 2)


        self.gridLayout_13.addWidget(self.groupBox, 0, 2, 2, 3)

        self.line_17 = QFrame(self.frame_5)
        self.line_17.setObjectName(u"line_17")
        self.line_17.setFrameShape(QFrame.Shape.VLine)
        self.line_17.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_13.addWidget(self.line_17, 0, 1, 4, 1)

        self.enroll_employee_btn = QPushButton(self.frame_5)
        self.enroll_employee_btn.setObjectName(u"enroll_employee_btn")
        self.enroll_employee_btn.setMinimumSize(QSize(101, 51))
        self.enroll_employee_btn.setMaximumSize(QSize(16777215, 16777215))
        self.enroll_employee_btn.setStyleSheet(u"background-color: rgb(204, 204, 204);")

        self.gridLayout_13.addWidget(self.enroll_employee_btn, 3, 3, 1, 1)

        self.add_employee_btn = QPushButton(self.frame_5)
        self.add_employee_btn.setObjectName(u"add_employee_btn")
        self.add_employee_btn.setMinimumSize(QSize(101, 51))
        self.add_employee_btn.setMaximumSize(QSize(16777215, 16777215))
        self.add_employee_btn.setStyleSheet(u"background-color: rgb(204, 204, 204);")

        self.gridLayout_13.addWidget(self.add_employee_btn, 3, 4, 1, 1)

        self.groupBox_2 = QGroupBox(self.frame_5)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setMinimumSize(QSize(591, 401))
        self.gridLayout_10 = QGridLayout(self.groupBox_2)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.label_28 = QLabel(self.groupBox_2)
        self.label_28.setObjectName(u"label_28")
        self.label_28.setMinimumSize(QSize(281, 27))

        self.gridLayout_10.addWidget(self.label_28, 0, 0, 1, 1)

        self.frame_13 = QFrame(self.groupBox_2)
        self.frame_13.setObjectName(u"frame_13")
        self.frame_13.setStyleSheet(u"background-color: transparent;\n"
"border: none;")
        self.frame_13.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_13.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_10.addWidget(self.frame_13, 0, 1, 1, 1)

        self.lineEdit_6 = QLineEdit(self.groupBox_2)
        self.lineEdit_6.setObjectName(u"lineEdit_6")
        self.lineEdit_6.setMinimumSize(QSize(491, 61))
        self.lineEdit_6.setStyleSheet(u"background-color: rgb(238, 238, 238);")

        self.gridLayout_10.addWidget(self.lineEdit_6, 1, 0, 1, 2)

        self.line_15 = QFrame(self.groupBox_2)
        self.line_15.setObjectName(u"line_15")
        self.line_15.setMinimumSize(QSize(0, 25))
        self.line_15.setFrameShape(QFrame.Shape.HLine)
        self.line_15.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_10.addWidget(self.line_15, 2, 0, 1, 2)

        self.label_27 = QLabel(self.groupBox_2)
        self.label_27.setObjectName(u"label_27")
        self.label_27.setMinimumSize(QSize(281, 41))

        self.gridLayout_10.addWidget(self.label_27, 3, 0, 1, 1)

        self.frame_14 = QFrame(self.groupBox_2)
        self.frame_14.setObjectName(u"frame_14")
        self.frame_14.setStyleSheet(u"background-color: transparent;\n"
"border: none;")
        self.frame_14.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_14.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_10.addWidget(self.frame_14, 3, 1, 1, 1)

        self.lineEdit_7 = QLineEdit(self.groupBox_2)
        self.lineEdit_7.setObjectName(u"lineEdit_7")
        self.lineEdit_7.setMinimumSize(QSize(491, 61))
        self.lineEdit_7.setStyleSheet(u"background-color: rgb(238, 238, 238);")

        self.gridLayout_10.addWidget(self.lineEdit_7, 4, 0, 1, 2)

        self.line_16 = QFrame(self.groupBox_2)
        self.line_16.setObjectName(u"line_16")
        self.line_16.setMinimumSize(QSize(0, 25))
        self.line_16.setFrameShape(QFrame.Shape.HLine)
        self.line_16.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_10.addWidget(self.line_16, 5, 0, 1, 2)

        self.label_29 = QLabel(self.groupBox_2)
        self.label_29.setObjectName(u"label_29")
        self.label_29.setMinimumSize(QSize(281, 41))

        self.gridLayout_10.addWidget(self.label_29, 6, 0, 1, 1)

        self.frame_15 = QFrame(self.groupBox_2)
        self.frame_15.setObjectName(u"frame_15")
        self.frame_15.setStyleSheet(u"background-color: transparent;\n"
"border: none;")
        self.frame_15.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_15.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_10.addWidget(self.frame_15, 6, 1, 1, 1)

        self.lineEdit_8 = QLineEdit(self.groupBox_2)
        self.lineEdit_8.setObjectName(u"lineEdit_8")
        self.lineEdit_8.setMinimumSize(QSize(491, 61))
        self.lineEdit_8.setStyleSheet(u"background-color: rgb(238, 238, 238);")

        self.gridLayout_10.addWidget(self.lineEdit_8, 7, 0, 1, 2)

        self.line_18 = QFrame(self.groupBox_2)
        self.line_18.setObjectName(u"line_18")
        self.line_18.setMinimumSize(QSize(0, 5))
        self.line_18.setStyleSheet(u"border: none;")
        self.line_18.setFrameShape(QFrame.Shape.HLine)
        self.line_18.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_10.addWidget(self.line_18, 8, 0, 1, 2)


        self.gridLayout_13.addWidget(self.groupBox_2, 1, 0, 3, 1)

        self.frame_19 = QFrame(self.frame_5)
        self.frame_19.setObjectName(u"frame_19")
        self.frame_19.setStyleSheet(u"background-color: transparent;\n"
"border: none;")
        self.frame_19.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_19.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_13.addWidget(self.frame_19, 2, 2, 1, 3)

        self.enroll_employee_btn_2 = QPushButton(self.frame_5)
        self.enroll_employee_btn_2.setObjectName(u"enroll_employee_btn_2")
        self.enroll_employee_btn_2.setMinimumSize(QSize(101, 51))
        self.enroll_employee_btn_2.setMaximumSize(QSize(16777215, 16777215))
        self.enroll_employee_btn_2.setStyleSheet(u"background-color: rgb(204, 204, 204);")

        self.gridLayout_13.addWidget(self.enroll_employee_btn_2, 3, 2, 1, 1)


        self.gridLayout_9.addWidget(self.frame_5, 0, 1, 1, 1)

        self.stackedWidget.addWidget(self.employee_enroll_page)
        self.edit_employee_page = QWidget()
        self.edit_employee_page.setObjectName(u"edit_employee_page")
        self.gridLayout_32 = QGridLayout(self.edit_employee_page)
        self.gridLayout_32.setObjectName(u"gridLayout_32")
        self.frame_47 = QFrame(self.edit_employee_page)
        self.frame_47.setObjectName(u"frame_47")
        self.frame_47.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.frame_47.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_47.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_28 = QGridLayout(self.frame_47)
        self.gridLayout_28.setObjectName(u"gridLayout_28")
        self.groupBox_10 = QGroupBox(self.frame_47)
        self.groupBox_10.setObjectName(u"groupBox_10")
        self.groupBox_10.setMinimumSize(QSize(591, 221))
        self.groupBox_10.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.gridLayout_29 = QGridLayout(self.groupBox_10)
        self.gridLayout_29.setObjectName(u"gridLayout_29")
        self.frame_48 = QFrame(self.groupBox_10)
        self.frame_48.setObjectName(u"frame_48")
        self.frame_48.setMinimumSize(QSize(171, 0))
        self.frame_48.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_48.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_29.addWidget(self.frame_48, 0, 0, 2, 1)

        self.label_51 = QLabel(self.groupBox_10)
        self.label_51.setObjectName(u"label_51")
        self.label_51.setMinimumSize(QSize(190, 190))
        self.label_51.setStyleSheet(u"background-color: rgb(241, 241, 241);")
        self.label_51.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_29.addWidget(self.label_51, 0, 1, 2, 1)

        self.frame_49 = QFrame(self.groupBox_10)
        self.frame_49.setObjectName(u"frame_49")
        self.frame_49.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_49.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_29.addWidget(self.frame_49, 0, 2, 2, 1)

        self.frame_50 = QFrame(self.groupBox_10)
        self.frame_50.setObjectName(u"frame_50")
        self.frame_50.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_50.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_29.addWidget(self.frame_50, 0, 3, 1, 1)

        self.edit_pfp_btn = QPushButton(self.groupBox_10)
        self.edit_pfp_btn.setObjectName(u"edit_pfp_btn")
        self.edit_pfp_btn.setMinimumSize(QSize(51, 51))
        self.edit_pfp_btn.setMaximumSize(QSize(101, 16777215))
        self.edit_pfp_btn.setStyleSheet(u"background-color: rgb(204, 204, 204);")

        self.gridLayout_29.addWidget(self.edit_pfp_btn, 1, 3, 1, 1)


        self.gridLayout_28.addWidget(self.groupBox_10, 0, 0, 1, 1)

        self.line_27 = QFrame(self.frame_47)
        self.line_27.setObjectName(u"line_27")
        self.line_27.setFrameShape(QFrame.Shape.VLine)
        self.line_27.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_28.addWidget(self.line_27, 0, 1, 4, 1)

        self.groupBox_11 = QGroupBox(self.frame_47)
        self.groupBox_11.setObjectName(u"groupBox_11")
        self.groupBox_11.setMinimumSize(QSize(551, 371))
        self.groupBox_11.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.gridLayout_30 = QGridLayout(self.groupBox_11)
        self.gridLayout_30.setObjectName(u"gridLayout_30")
        self.label_52 = QLabel(self.groupBox_11)
        self.label_52.setObjectName(u"label_52")

        self.gridLayout_30.addWidget(self.label_52, 0, 0, 1, 1)

        self.frame_51 = QFrame(self.groupBox_11)
        self.frame_51.setObjectName(u"frame_51")
        self.frame_51.setStyleSheet(u"background-color: transparent;\n"
"border: none;")
        self.frame_51.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_51.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_30.addWidget(self.frame_51, 0, 1, 1, 1)

        self.lineEdit_9 = QLineEdit(self.groupBox_11)
        self.lineEdit_9.setObjectName(u"lineEdit_9")
        self.lineEdit_9.setMinimumSize(QSize(491, 61))
        self.lineEdit_9.setStyleSheet(u"background-color: rgb(238, 238, 238);")

        self.gridLayout_30.addWidget(self.lineEdit_9, 1, 0, 1, 2)

        self.line_28 = QFrame(self.groupBox_11)
        self.line_28.setObjectName(u"line_28")
        self.line_28.setMinimumSize(QSize(0, 15))
        self.line_28.setFrameShape(QFrame.Shape.HLine)
        self.line_28.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_30.addWidget(self.line_28, 2, 0, 1, 2)

        self.label_53 = QLabel(self.groupBox_11)
        self.label_53.setObjectName(u"label_53")

        self.gridLayout_30.addWidget(self.label_53, 3, 0, 1, 1)

        self.frame_52 = QFrame(self.groupBox_11)
        self.frame_52.setObjectName(u"frame_52")
        self.frame_52.setStyleSheet(u"background-color: transparent;\n"
"border: none;")
        self.frame_52.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_52.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_30.addWidget(self.frame_52, 3, 1, 1, 1)

        self.lineEdit_10 = QLineEdit(self.groupBox_11)
        self.lineEdit_10.setObjectName(u"lineEdit_10")
        self.lineEdit_10.setMinimumSize(QSize(491, 61))
        self.lineEdit_10.setStyleSheet(u"background-color: rgb(238, 238, 238);")

        self.gridLayout_30.addWidget(self.lineEdit_10, 4, 0, 1, 2)

        self.line_29 = QFrame(self.groupBox_11)
        self.line_29.setObjectName(u"line_29")
        self.line_29.setMinimumSize(QSize(0, 15))
        self.line_29.setFrameShape(QFrame.Shape.HLine)
        self.line_29.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_30.addWidget(self.line_29, 5, 0, 1, 2)

        self.label_54 = QLabel(self.groupBox_11)
        self.label_54.setObjectName(u"label_54")

        self.gridLayout_30.addWidget(self.label_54, 6, 0, 1, 1)

        self.frame_53 = QFrame(self.groupBox_11)
        self.frame_53.setObjectName(u"frame_53")
        self.frame_53.setStyleSheet(u"background-color: transparent;\n"
"border: none;")
        self.frame_53.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_53.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_30.addWidget(self.frame_53, 6, 1, 1, 1)

        self.frame_54 = QFrame(self.groupBox_11)
        self.frame_54.setObjectName(u"frame_54")
        self.frame_54.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.frame_54.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_54.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_54)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.radioButton_13 = QRadioButton(self.frame_54)
        self.radioButton_13.setObjectName(u"radioButton_13")

        self.horizontalLayout_5.addWidget(self.radioButton_13)

        self.radioButton_14 = QRadioButton(self.frame_54)
        self.radioButton_14.setObjectName(u"radioButton_14")

        self.horizontalLayout_5.addWidget(self.radioButton_14)

        self.radioButton_15 = QRadioButton(self.frame_54)
        self.radioButton_15.setObjectName(u"radioButton_15")

        self.horizontalLayout_5.addWidget(self.radioButton_15)


        self.gridLayout_30.addWidget(self.frame_54, 7, 0, 1, 2)


        self.gridLayout_28.addWidget(self.groupBox_11, 0, 2, 2, 4)

        self.groupBox_12 = QGroupBox(self.frame_47)
        self.groupBox_12.setObjectName(u"groupBox_12")
        self.groupBox_12.setMinimumSize(QSize(591, 401))
        self.gridLayout_31 = QGridLayout(self.groupBox_12)
        self.gridLayout_31.setObjectName(u"gridLayout_31")
        self.label_55 = QLabel(self.groupBox_12)
        self.label_55.setObjectName(u"label_55")
        self.label_55.setMinimumSize(QSize(281, 27))

        self.gridLayout_31.addWidget(self.label_55, 0, 0, 1, 1)

        self.frame_55 = QFrame(self.groupBox_12)
        self.frame_55.setObjectName(u"frame_55")
        self.frame_55.setStyleSheet(u"background-color: transparent;\n"
"border: none;")
        self.frame_55.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_55.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_31.addWidget(self.frame_55, 0, 1, 1, 1)

        self.lineEdit_11 = QLineEdit(self.groupBox_12)
        self.lineEdit_11.setObjectName(u"lineEdit_11")
        self.lineEdit_11.setMinimumSize(QSize(491, 61))
        self.lineEdit_11.setStyleSheet(u"background-color: rgb(238, 238, 238);")

        self.gridLayout_31.addWidget(self.lineEdit_11, 1, 0, 1, 2)

        self.line_30 = QFrame(self.groupBox_12)
        self.line_30.setObjectName(u"line_30")
        self.line_30.setMinimumSize(QSize(0, 25))
        self.line_30.setFrameShape(QFrame.Shape.HLine)
        self.line_30.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_31.addWidget(self.line_30, 2, 0, 1, 2)

        self.label_56 = QLabel(self.groupBox_12)
        self.label_56.setObjectName(u"label_56")
        self.label_56.setMinimumSize(QSize(281, 41))

        self.gridLayout_31.addWidget(self.label_56, 3, 0, 1, 1)

        self.frame_56 = QFrame(self.groupBox_12)
        self.frame_56.setObjectName(u"frame_56")
        self.frame_56.setStyleSheet(u"background-color: transparent;\n"
"border: none;")
        self.frame_56.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_56.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_31.addWidget(self.frame_56, 3, 1, 1, 1)

        self.lineEdit_12 = QLineEdit(self.groupBox_12)
        self.lineEdit_12.setObjectName(u"lineEdit_12")
        self.lineEdit_12.setMinimumSize(QSize(491, 61))
        self.lineEdit_12.setStyleSheet(u"background-color: rgb(238, 238, 238);")

        self.gridLayout_31.addWidget(self.lineEdit_12, 4, 0, 1, 2)

        self.line_31 = QFrame(self.groupBox_12)
        self.line_31.setObjectName(u"line_31")
        self.line_31.setMinimumSize(QSize(0, 25))
        self.line_31.setFrameShape(QFrame.Shape.HLine)
        self.line_31.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_31.addWidget(self.line_31, 5, 0, 1, 2)

        self.label_57 = QLabel(self.groupBox_12)
        self.label_57.setObjectName(u"label_57")
        self.label_57.setMinimumSize(QSize(281, 41))

        self.gridLayout_31.addWidget(self.label_57, 6, 0, 1, 1)

        self.frame_57 = QFrame(self.groupBox_12)
        self.frame_57.setObjectName(u"frame_57")
        self.frame_57.setStyleSheet(u"background-color: transparent;\n"
"border: none;")
        self.frame_57.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_57.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_31.addWidget(self.frame_57, 6, 1, 1, 1)

        self.lineEdit_13 = QLineEdit(self.groupBox_12)
        self.lineEdit_13.setObjectName(u"lineEdit_13")
        self.lineEdit_13.setMinimumSize(QSize(491, 61))
        self.lineEdit_13.setStyleSheet(u"background-color: rgb(238, 238, 238);")

        self.gridLayout_31.addWidget(self.lineEdit_13, 7, 0, 1, 2)

        self.line_32 = QFrame(self.groupBox_12)
        self.line_32.setObjectName(u"line_32")
        self.line_32.setMinimumSize(QSize(0, 5))
        self.line_32.setStyleSheet(u"border: none;")
        self.line_32.setFrameShape(QFrame.Shape.HLine)
        self.line_32.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_31.addWidget(self.line_32, 8, 0, 1, 2)


        self.gridLayout_28.addWidget(self.groupBox_12, 1, 0, 3, 1)

        self.frame_58 = QFrame(self.frame_47)
        self.frame_58.setObjectName(u"frame_58")
        self.frame_58.setStyleSheet(u"background-color: transparent;\n"
"border: none;")
        self.frame_58.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_58.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_28.addWidget(self.frame_58, 2, 2, 1, 4)

        self.archive_employee_btn = QPushButton(self.frame_47)
        self.archive_employee_btn.setObjectName(u"archive_employee_btn")
        self.archive_employee_btn.setMinimumSize(QSize(101, 51))
        self.archive_employee_btn.setMaximumSize(QSize(16777215, 16777215))
        self.archive_employee_btn.setStyleSheet(u"background-color: rgb(204, 204, 204);")

        self.gridLayout_28.addWidget(self.archive_employee_btn, 3, 3, 1, 1)

        self.save_employee_btn = QPushButton(self.frame_47)
        self.save_employee_btn.setObjectName(u"save_employee_btn")
        self.save_employee_btn.setMinimumSize(QSize(101, 51))
        self.save_employee_btn.setMaximumSize(QSize(16777215, 16777215))
        self.save_employee_btn.setStyleSheet(u"background-color: rgb(204, 204, 204);")

        self.gridLayout_28.addWidget(self.save_employee_btn, 3, 4, 1, 1)

        self.edit_employee_back_btn = QPushButton(self.frame_47)
        self.edit_employee_back_btn.setObjectName(u"edit_employee_back_btn")
        self.edit_employee_back_btn.setMinimumSize(QSize(101, 51))
        self.edit_employee_back_btn.setMaximumSize(QSize(16777215, 16777215))
        self.edit_employee_back_btn.setStyleSheet(u"background-color: rgb(204, 204, 204);")

        self.gridLayout_28.addWidget(self.edit_employee_back_btn, 3, 5, 1, 1)


        self.gridLayout_32.addWidget(self.frame_47, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.edit_employee_page)
        self.employee_enroll_bio2_page = QWidget()
        self.employee_enroll_bio2_page.setObjectName(u"employee_enroll_bio2_page")
        self.gridLayout_16 = QGridLayout(self.employee_enroll_bio2_page)
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.frame_25 = QFrame(self.employee_enroll_bio2_page)
        self.frame_25.setObjectName(u"frame_25")
        self.frame_25.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_25.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_17 = QGridLayout(self.frame_25)
        self.gridLayout_17.setObjectName(u"gridLayout_17")
        self.label_35 = QLabel(self.frame_25)
        self.label_35.setObjectName(u"label_35")
        self.label_35.setMinimumSize(QSize(701, 661))
        self.label_35.setStyleSheet(u"background-color: rgb(241, 241, 241);")
        self.label_35.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_17.addWidget(self.label_35, 0, 0, 6, 1)

        self.frame_26 = QFrame(self.frame_25)
        self.frame_26.setObjectName(u"frame_26")
        self.frame_26.setMinimumSize(QSize(201, 0))
        self.frame_26.setMaximumSize(QSize(16777215, 16777215))
        self.frame_26.setStyleSheet(u"background-color: transparent;\n"
"border: none;")
        self.frame_26.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_26.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_17.addWidget(self.frame_26, 0, 1, 2, 1)

        self.frame_30 = QFrame(self.frame_25)
        self.frame_30.setObjectName(u"frame_30")
        self.frame_30.setMinimumSize(QSize(0, 201))
        self.frame_30.setMaximumSize(QSize(16777215, 16777215))
        self.frame_30.setStyleSheet(u"background-color: transparent;\n"
"border: none;")
        self.frame_30.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_30.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_17.addWidget(self.frame_30, 0, 2, 1, 1)

        self.frame_29 = QFrame(self.frame_25)
        self.frame_29.setObjectName(u"frame_29")
        self.frame_29.setMinimumSize(QSize(0, 0))
        self.frame_29.setMaximumSize(QSize(16777215, 16777215))
        self.frame_29.setStyleSheet(u"background-color: transparent;\n"
"border: none;")
        self.frame_29.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_29.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_17.addWidget(self.frame_29, 0, 3, 2, 2)

        self.label_37 = QLabel(self.frame_25)
        self.label_37.setObjectName(u"label_37")
        self.label_37.setMinimumSize(QSize(0, 0))
        self.label_37.setStyleSheet(u"background-color: rgb(230, 230, 230);")
        self.label_37.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_17.addWidget(self.label_37, 1, 2, 1, 1)

        self.label_36 = QLabel(self.frame_25)
        self.label_36.setObjectName(u"label_36")
        self.label_36.setMinimumSize(QSize(0, 49))
        self.label_36.setMaximumSize(QSize(16777215, 49))
        self.label_36.setFont(font)
        self.label_36.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_17.addWidget(self.label_36, 2, 1, 1, 4)

        self.label_34 = QLabel(self.frame_25)
        self.label_34.setObjectName(u"label_34")
        self.label_34.setMinimumSize(QSize(0, 38))
        self.label_34.setMaximumSize(QSize(16777215, 38))
        font3 = QFont()
        font3.setPointSize(10)
        self.label_34.setFont(font3)
        self.label_34.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_17.addWidget(self.label_34, 3, 1, 1, 4)

        self.frame_28 = QFrame(self.frame_25)
        self.frame_28.setObjectName(u"frame_28")
        self.frame_28.setMinimumSize(QSize(511, 251))
        self.frame_28.setMaximumSize(QSize(16777215, 16777215))
        self.frame_28.setStyleSheet(u"background-color: transparent;\n"
"border: none;")
        self.frame_28.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_28.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_17.addWidget(self.frame_28, 4, 1, 1, 4)

        self.frame_27 = QFrame(self.frame_25)
        self.frame_27.setObjectName(u"frame_27")
        self.frame_27.setStyleSheet(u"background-color: transparent;\n"
"border: none;")
        self.frame_27.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_27.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_17.addWidget(self.frame_27, 5, 1, 1, 3)

        self.face_cancel_btn = QPushButton(self.frame_25)
        self.face_cancel_btn.setObjectName(u"face_cancel_btn")
        self.face_cancel_btn.setMinimumSize(QSize(101, 51))
        self.face_cancel_btn.setMaximumSize(QSize(101, 16777215))
        self.face_cancel_btn.setStyleSheet(u"background-color: rgb(204, 204, 204);")

        self.gridLayout_17.addWidget(self.face_cancel_btn, 5, 4, 1, 1)


        self.gridLayout_16.addWidget(self.frame_25, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.employee_enroll_bio2_page)
        self.hr_feedback_page = QWidget()
        self.hr_feedback_page.setObjectName(u"hr_feedback_page")
        self.gridLayout_21 = QGridLayout(self.hr_feedback_page)
        self.gridLayout_21.setObjectName(u"gridLayout_21")
        self.frame_34 = QFrame(self.hr_feedback_page)
        self.frame_34.setObjectName(u"frame_34")
        self.frame_34.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_34.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_45 = QGridLayout(self.frame_34)
        self.gridLayout_45.setObjectName(u"gridLayout_45")
        self.groupBox_13 = QGroupBox(self.frame_34)
        self.groupBox_13.setObjectName(u"groupBox_13")
        self.groupBox_13.setMinimumSize(QSize(581, 80))
        self.gridLayout_43 = QGridLayout(self.groupBox_13)
        self.gridLayout_43.setObjectName(u"gridLayout_43")
        self.frame_70 = QFrame(self.groupBox_13)
        self.frame_70.setObjectName(u"frame_70")
        self.frame_70.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.frame_70.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_70.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_70)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.radioButton_7 = QRadioButton(self.frame_70)
        self.radioButton_7.setObjectName(u"radioButton_7")

        self.horizontalLayout_3.addWidget(self.radioButton_7)

        self.radioButton_8 = QRadioButton(self.frame_70)
        self.radioButton_8.setObjectName(u"radioButton_8")

        self.horizontalLayout_3.addWidget(self.radioButton_8)

        self.radioButton_9 = QRadioButton(self.frame_70)
        self.radioButton_9.setObjectName(u"radioButton_9")

        self.horizontalLayout_3.addWidget(self.radioButton_9)


        self.gridLayout_43.addWidget(self.frame_70, 0, 0, 1, 1)


        self.gridLayout_45.addWidget(self.groupBox_13, 0, 0, 1, 1)

        self.line_19 = QFrame(self.frame_34)
        self.line_19.setObjectName(u"line_19")
        self.line_19.setFrameShape(QFrame.Shape.VLine)
        self.line_19.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_45.addWidget(self.line_19, 0, 1, 6, 1)

        self.groupBox_5 = QGroupBox(self.frame_34)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.groupBox_5.setMinimumSize(QSize(611, 571))
        self.gridLayout_44 = QGridLayout(self.groupBox_5)
        self.gridLayout_44.setObjectName(u"gridLayout_44")
        self.tableWidget_2 = QTableWidget(self.groupBox_5)
        if (self.tableWidget_2.columnCount() < 3):
            self.tableWidget_2.setColumnCount(3)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(0, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(1, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(2, __qtablewidgetitem5)
        self.tableWidget_2.setObjectName(u"tableWidget_2")
        self.tableWidget_2.horizontalHeader().setDefaultSectionSize(176)
        self.tableWidget_2.horizontalHeader().setStretchLastSection(True)

        self.gridLayout_44.addWidget(self.tableWidget_2, 0, 0, 1, 1)


        self.gridLayout_45.addWidget(self.groupBox_5, 0, 2, 4, 3)

        self.groupBox_6 = QGroupBox(self.frame_34)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.groupBox_6.setMinimumSize(QSize(581, 401))
        self.gridLayout_42 = QGridLayout(self.groupBox_6)
        self.gridLayout_42.setObjectName(u"gridLayout_42")
        self.textEdit = QTextEdit(self.groupBox_6)
        self.textEdit.setObjectName(u"textEdit")

        self.gridLayout_42.addWidget(self.textEdit, 0, 0, 1, 1)


        self.gridLayout_45.addWidget(self.groupBox_6, 1, 0, 1, 1)

        self.frame_71 = QFrame(self.frame_34)
        self.frame_71.setObjectName(u"frame_71")
        self.frame_71.setMinimumSize(QSize(571, 0))
        self.frame_71.setStyleSheet(u"background-color: transparent;\n"
"border: none;")
        self.frame_71.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_71.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_45.addWidget(self.frame_71, 2, 0, 1, 1)

        self.label_81 = QLabel(self.frame_34)
        self.label_81.setObjectName(u"label_81")
        self.label_81.setMinimumSize(QSize(0, 49))
        self.label_81.setMaximumSize(QSize(16777215, 49))
        self.label_81.setFont(font1)
        self.label_81.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_45.addWidget(self.label_81, 3, 0, 2, 1)

        self.frame_69 = QFrame(self.frame_34)
        self.frame_69.setObjectName(u"frame_69")
        self.frame_69.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_69.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_45.addWidget(self.frame_69, 4, 2, 2, 1)

        self.send_feedback_btn = QPushButton(self.frame_34)
        self.send_feedback_btn.setObjectName(u"send_feedback_btn")
        self.send_feedback_btn.setMinimumSize(QSize(101, 51))
        self.send_feedback_btn.setMaximumSize(QSize(16777215, 16777215))
        self.send_feedback_btn.setStyleSheet(u"background-color: rgb(204, 204, 204);")

        self.gridLayout_45.addWidget(self.send_feedback_btn, 4, 3, 2, 1)

        self.cancel_feedback_btn = QPushButton(self.frame_34)
        self.cancel_feedback_btn.setObjectName(u"cancel_feedback_btn")
        self.cancel_feedback_btn.setMinimumSize(QSize(101, 51))
        self.cancel_feedback_btn.setMaximumSize(QSize(16777215, 16777215))
        self.cancel_feedback_btn.setStyleSheet(u"background-color: rgb(204, 204, 204);")

        self.gridLayout_45.addWidget(self.cancel_feedback_btn, 4, 4, 2, 1)

        self.frame_72 = QFrame(self.frame_34)
        self.frame_72.setObjectName(u"frame_72")
        self.frame_72.setMinimumSize(QSize(571, 0))
        self.frame_72.setStyleSheet(u"background-color: transparent;\n"
"border: none;")
        self.frame_72.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_72.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_45.addWidget(self.frame_72, 5, 0, 1, 1)


        self.gridLayout_21.addWidget(self.frame_34, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.hr_feedback_page)
        self.admin_employee_page = QWidget()
        self.admin_employee_page.setObjectName(u"admin_employee_page")
        self.gridLayout_59 = QGridLayout(self.admin_employee_page)
        self.gridLayout_59.setObjectName(u"gridLayout_59")
        self.employee_settings_btn = QPushButton(self.admin_employee_page)
        self.employee_settings_btn.setObjectName(u"employee_settings_btn")
        self.employee_settings_btn.setMinimumSize(QSize(71, 71))
        self.employee_settings_btn.setMaximumSize(QSize(71, 71))

        self.gridLayout_59.addWidget(self.employee_settings_btn, 4, 0, 1, 1)

        self.line_48 = QFrame(self.admin_employee_page)
        self.line_48.setObjectName(u"line_48")
        self.line_48.setStyleSheet(u"border: 0px;\n"
"")
        self.line_48.setFrameShape(QFrame.Shape.VLine)
        self.line_48.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_59.addWidget(self.line_48, 0, 1, 6, 1)

        self.frame_94 = QFrame(self.admin_employee_page)
        self.frame_94.setObjectName(u"frame_94")
        self.frame_94.setStyleSheet(u"background-color: transparent;\n"
"border: none;")
        self.frame_94.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_94.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_59.addWidget(self.frame_94, 5, 0, 1, 1)

        self.line_44 = QFrame(self.admin_employee_page)
        self.line_44.setObjectName(u"line_44")
        self.line_44.setFrameShape(QFrame.Shape.HLine)
        self.line_44.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_59.addWidget(self.line_44, 3, 0, 1, 1)

        self.employee_employee_btn = QPushButton(self.admin_employee_page)
        self.employee_employee_btn.setObjectName(u"employee_employee_btn")
        self.employee_employee_btn.setMinimumSize(QSize(71, 71))
        self.employee_employee_btn.setMaximumSize(QSize(71, 71))

        self.gridLayout_59.addWidget(self.employee_employee_btn, 2, 0, 1, 1)

        self.line_45 = QFrame(self.admin_employee_page)
        self.line_45.setObjectName(u"line_45")
        self.line_45.setFrameShape(QFrame.Shape.HLine)
        self.line_45.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_59.addWidget(self.line_45, 1, 0, 1, 1)

        self.employee_home_btn = QPushButton(self.admin_employee_page)
        self.employee_home_btn.setObjectName(u"employee_home_btn")
        self.employee_home_btn.setMinimumSize(QSize(71, 71))
        self.employee_home_btn.setMaximumSize(QSize(71, 71))

        self.gridLayout_59.addWidget(self.employee_home_btn, 0, 0, 1, 1)

        self.frame_84 = QFrame(self.admin_employee_page)
        self.frame_84.setObjectName(u"frame_84")
        self.frame_84.setMinimumSize(QSize(1148, 684))
        self.frame_84.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_84.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_23 = QGridLayout(self.frame_84)
        self.gridLayout_23.setObjectName(u"gridLayout_23")
        self.groupBox_7 = QGroupBox(self.frame_84)
        self.groupBox_7.setObjectName(u"groupBox_7")
        self.groupBox_7.setMinimumSize(QSize(461, 481))
        self.gridLayout_22 = QGridLayout(self.groupBox_7)
        self.gridLayout_22.setObjectName(u"gridLayout_22")
        self.line_42 = QFrame(self.groupBox_7)
        self.line_42.setObjectName(u"line_42")
        self.line_42.setFrameShape(QFrame.Shape.HLine)
        self.line_42.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_22.addWidget(self.line_42, 4, 0, 1, 3)

        self.label_41 = QLabel(self.groupBox_7)
        self.label_41.setObjectName(u"label_41")

        self.gridLayout_22.addWidget(self.label_41, 0, 0, 1, 1)

        self.label_80 = QLabel(self.groupBox_7)
        self.label_80.setObjectName(u"label_80")

        self.gridLayout_22.addWidget(self.label_80, 5, 0, 1, 2)

        self.textBrowser = QTextBrowser(self.groupBox_7)
        self.textBrowser.setObjectName(u"textBrowser")

        self.gridLayout_22.addWidget(self.textBrowser, 2, 0, 1, 3)

        self.line_20 = QFrame(self.groupBox_7)
        self.line_20.setObjectName(u"line_20")
        self.line_20.setMinimumSize(QSize(0, 3))
        self.line_20.setFrameShape(QFrame.Shape.HLine)
        self.line_20.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_22.addWidget(self.line_20, 3, 0, 1, 3)

        self.comboBox = QComboBox(self.groupBox_7)
        self.comboBox.setObjectName(u"comboBox")

        self.gridLayout_22.addWidget(self.comboBox, 0, 1, 1, 2)


        self.gridLayout_23.addWidget(self.groupBox_7, 0, 1, 1, 3)

        self.frame_37 = QFrame(self.frame_84)
        self.frame_37.setObjectName(u"frame_37")
        self.frame_37.setMinimumSize(QSize(461, 0))
        self.frame_37.setStyleSheet(u"background-color: transparent;\n"
"border: none;")
        self.frame_37.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_37.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_23.addWidget(self.frame_37, 1, 1, 1, 3)

        self.line_34 = QFrame(self.frame_84)
        self.line_34.setObjectName(u"line_34")
        self.line_34.setFrameShape(QFrame.Shape.HLine)
        self.line_34.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_23.addWidget(self.line_34, 3, 1, 1, 3)

        self.employee_edit_btn = QPushButton(self.frame_84)
        self.employee_edit_btn.setObjectName(u"employee_edit_btn")
        self.employee_edit_btn.setMinimumSize(QSize(101, 51))
        self.employee_edit_btn.setMaximumSize(QSize(16777215, 16777215))
        self.employee_edit_btn.setStyleSheet(u"background-color: rgb(204, 204, 204);")

        self.gridLayout_23.addWidget(self.employee_edit_btn, 4, 1, 2, 1)

        self.employee_add_btn = QPushButton(self.frame_84)
        self.employee_add_btn.setObjectName(u"employee_add_btn")
        self.employee_add_btn.setMinimumSize(QSize(101, 51))
        self.employee_add_btn.setMaximumSize(QSize(16777215, 16777215))
        self.employee_add_btn.setStyleSheet(u"background-color: rgb(204, 204, 204);")

        self.gridLayout_23.addWidget(self.employee_add_btn, 5, 2, 1, 1)

        self.employee_view_btn = QPushButton(self.frame_84)
        self.employee_view_btn.setObjectName(u"employee_view_btn")
        self.employee_view_btn.setMinimumSize(QSize(101, 51))
        self.employee_view_btn.setMaximumSize(QSize(16777215, 16777215))
        self.employee_view_btn.setStyleSheet(u"background-color: rgb(204, 204, 204);")

        self.gridLayout_23.addWidget(self.employee_view_btn, 5, 3, 1, 1)

        self.groupBox_20 = QGroupBox(self.frame_84)
        self.groupBox_20.setObjectName(u"groupBox_20")
        self.groupBox_20.setMinimumSize(QSize(631, 311))
        self.gridLayout_55 = QGridLayout(self.groupBox_20)
        self.gridLayout_55.setObjectName(u"gridLayout_55")
        self.tableWidget_7 = QTableWidget(self.groupBox_20)
        if (self.tableWidget_7.columnCount() < 3):
            self.tableWidget_7.setColumnCount(3)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tableWidget_7.setHorizontalHeaderItem(0, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tableWidget_7.setHorizontalHeaderItem(1, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.tableWidget_7.setHorizontalHeaderItem(2, __qtablewidgetitem8)
        self.tableWidget_7.setObjectName(u"tableWidget_7")
        self.tableWidget_7.horizontalHeader().setDefaultSectionSize(180)
        self.tableWidget_7.horizontalHeader().setStretchLastSection(True)

        self.gridLayout_55.addWidget(self.tableWidget_7, 0, 0, 1, 1)

        self.line_33 = QFrame(self.groupBox_20)
        self.line_33.setObjectName(u"line_33")
        self.line_33.setFrameShape(QFrame.Shape.HLine)
        self.line_33.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_55.addWidget(self.line_33, 1, 0, 1, 1)

        self.label_66 = QLabel(self.groupBox_20)
        self.label_66.setObjectName(u"label_66")

        self.gridLayout_55.addWidget(self.label_66, 2, 0, 1, 1)


        self.gridLayout_23.addWidget(self.groupBox_20, 0, 0, 6, 1)

        self.manage_hr_btn = QPushButton(self.frame_84)
        self.manage_hr_btn.setObjectName(u"manage_hr_btn")
        self.manage_hr_btn.setMinimumSize(QSize(101, 51))
        self.manage_hr_btn.setMaximumSize(QSize(16777215, 16777215))
        self.manage_hr_btn.setStyleSheet(u"background-color: rgb(204, 204, 204);")

        self.gridLayout_23.addWidget(self.manage_hr_btn, 2, 1, 1, 3)


        self.gridLayout_59.addWidget(self.frame_84, 0, 2, 6, 1)

        self.stackedWidget.addWidget(self.admin_employee_page)
        self.admin_hr_page = QWidget()
        self.admin_hr_page.setObjectName(u"admin_hr_page")
        self.gridLayout_60 = QGridLayout(self.admin_hr_page)
        self.gridLayout_60.setObjectName(u"gridLayout_60")
        self.frame_61 = QFrame(self.admin_hr_page)
        self.frame_61.setObjectName(u"frame_61")
        self.frame_61.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_61.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_63 = QGridLayout(self.frame_61)
        self.gridLayout_63.setObjectName(u"gridLayout_63")
        self.groupBox_31 = QGroupBox(self.frame_61)
        self.groupBox_31.setObjectName(u"groupBox_31")
        self.groupBox_31.setMinimumSize(QSize(631, 291))
        self.gridLayout_62 = QGridLayout(self.groupBox_31)
        self.gridLayout_62.setObjectName(u"gridLayout_62")
        self.tableWidget_12 = QTableWidget(self.groupBox_31)
        if (self.tableWidget_12.columnCount() < 3):
            self.tableWidget_12.setColumnCount(3)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.tableWidget_12.setHorizontalHeaderItem(0, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.tableWidget_12.setHorizontalHeaderItem(1, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.tableWidget_12.setHorizontalHeaderItem(2, __qtablewidgetitem11)
        self.tableWidget_12.setObjectName(u"tableWidget_12")
        self.tableWidget_12.horizontalHeader().setDefaultSectionSize(233)
        self.tableWidget_12.horizontalHeader().setProperty(u"showSortIndicator", False)
        self.tableWidget_12.horizontalHeader().setStretchLastSection(True)

        self.gridLayout_62.addWidget(self.tableWidget_12, 0, 0, 1, 1)


        self.gridLayout_63.addWidget(self.groupBox_31, 0, 0, 1, 1)

        self.groupBox_32 = QGroupBox(self.frame_61)
        self.groupBox_32.setObjectName(u"groupBox_32")
        self.groupBox_32.setMinimumSize(QSize(571, 471))
        self.gridLayout_61 = QGridLayout(self.groupBox_32)
        self.gridLayout_61.setObjectName(u"gridLayout_61")
        self.label_74 = QLabel(self.groupBox_32)
        self.label_74.setObjectName(u"label_74")

        self.gridLayout_61.addWidget(self.label_74, 0, 0, 1, 1)

        self.lineEdit_19 = QLineEdit(self.groupBox_32)
        self.lineEdit_19.setObjectName(u"lineEdit_19")
        self.lineEdit_19.setMinimumSize(QSize(491, 61))
        self.lineEdit_19.setStyleSheet(u"background-color: rgb(238, 238, 238);")

        self.gridLayout_61.addWidget(self.lineEdit_19, 1, 0, 1, 2)

        self.line_57 = QFrame(self.groupBox_32)
        self.line_57.setObjectName(u"line_57")
        self.line_57.setMinimumSize(QSize(0, 15))
        self.line_57.setFrameShape(QFrame.Shape.HLine)
        self.line_57.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_61.addWidget(self.line_57, 2, 0, 1, 2)

        self.label_68 = QLabel(self.groupBox_32)
        self.label_68.setObjectName(u"label_68")

        self.gridLayout_61.addWidget(self.label_68, 3, 0, 1, 1)

        self.lineEdit_15 = QLineEdit(self.groupBox_32)
        self.lineEdit_15.setObjectName(u"lineEdit_15")
        self.lineEdit_15.setMinimumSize(QSize(491, 61))
        self.lineEdit_15.setStyleSheet(u"background-color: rgb(238, 238, 238);")

        self.gridLayout_61.addWidget(self.lineEdit_15, 4, 0, 1, 2)

        self.line_36 = QFrame(self.groupBox_32)
        self.line_36.setObjectName(u"line_36")
        self.line_36.setMinimumSize(QSize(0, 15))
        self.line_36.setFrameShape(QFrame.Shape.HLine)
        self.line_36.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_61.addWidget(self.line_36, 5, 0, 1, 2)

        self.label_69 = QLabel(self.groupBox_32)
        self.label_69.setObjectName(u"label_69")

        self.gridLayout_61.addWidget(self.label_69, 6, 0, 1, 1)

        self.lineEdit_14 = QLineEdit(self.groupBox_32)
        self.lineEdit_14.setObjectName(u"lineEdit_14")
        self.lineEdit_14.setMinimumSize(QSize(491, 61))
        self.lineEdit_14.setStyleSheet(u"background-color: rgb(238, 238, 238);")

        self.gridLayout_61.addWidget(self.lineEdit_14, 7, 0, 1, 2)

        self.line_37 = QFrame(self.groupBox_32)
        self.line_37.setObjectName(u"line_37")
        self.line_37.setMinimumSize(QSize(0, 15))
        self.line_37.setFrameShape(QFrame.Shape.HLine)
        self.line_37.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_61.addWidget(self.line_37, 8, 0, 1, 2)

        self.label_70 = QLabel(self.groupBox_32)
        self.label_70.setObjectName(u"label_70")
        self.label_70.setInputMethodHints(Qt.InputMethodHint.ImhMultiLine)
        self.label_70.setFrameShadow(QFrame.Shadow.Plain)
        self.label_70.setLineWidth(1)
        self.label_70.setTextFormat(Qt.TextFormat.AutoText)

        self.gridLayout_61.addWidget(self.label_70, 9, 0, 1, 1)

        self.manage_hr_add_btn = QPushButton(self.groupBox_32)
        self.manage_hr_add_btn.setObjectName(u"manage_hr_add_btn")
        self.manage_hr_add_btn.setMinimumSize(QSize(101, 42))
        self.manage_hr_add_btn.setMaximumSize(QSize(16777215, 16777215))
        self.manage_hr_add_btn.setStyleSheet(u"background-color: rgb(204, 204, 204);")

        self.gridLayout_61.addWidget(self.manage_hr_add_btn, 9, 1, 1, 1)


        self.gridLayout_63.addWidget(self.groupBox_32, 0, 1, 2, 4)

        self.groupBox_30 = QGroupBox(self.frame_61)
        self.groupBox_30.setObjectName(u"groupBox_30")
        self.groupBox_30.setMinimumSize(QSize(631, 341))
        self.gridLayout_64 = QGridLayout(self.groupBox_30)
        self.gridLayout_64.setObjectName(u"gridLayout_64")
        self.tableWidget_10 = QTableWidget(self.groupBox_30)
        if (self.tableWidget_10.columnCount() < 3):
            self.tableWidget_10.setColumnCount(3)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.tableWidget_10.setHorizontalHeaderItem(0, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.tableWidget_10.setHorizontalHeaderItem(1, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        self.tableWidget_10.setHorizontalHeaderItem(2, __qtablewidgetitem14)
        self.tableWidget_10.setObjectName(u"tableWidget_10")
        self.tableWidget_10.horizontalHeader().setDefaultSectionSize(150)
        self.tableWidget_10.horizontalHeader().setStretchLastSection(True)

        self.gridLayout_64.addWidget(self.tableWidget_10, 0, 0, 1, 1)

        self.line_35 = QFrame(self.groupBox_30)
        self.line_35.setObjectName(u"line_35")
        self.line_35.setFrameShape(QFrame.Shape.HLine)
        self.line_35.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_64.addWidget(self.line_35, 1, 0, 1, 1)

        self.label_67 = QLabel(self.groupBox_30)
        self.label_67.setObjectName(u"label_67")

        self.gridLayout_64.addWidget(self.label_67, 2, 0, 1, 1)


        self.gridLayout_63.addWidget(self.groupBox_30, 1, 0, 3, 1)

        self.frame_63 = QFrame(self.frame_61)
        self.frame_63.setObjectName(u"frame_63")
        self.frame_63.setStyleSheet(u"background-color: transparent;\n"
"border: none;\n"
"")
        self.frame_63.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_63.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_63.addWidget(self.frame_63, 2, 1, 1, 4)

        self.manage_edit_btn = QPushButton(self.frame_61)
        self.manage_edit_btn.setObjectName(u"manage_edit_btn")
        self.manage_edit_btn.setMinimumSize(QSize(101, 51))
        self.manage_edit_btn.setMaximumSize(QSize(16777215, 16777215))
        self.manage_edit_btn.setStyleSheet(u"background-color: rgb(204, 204, 204);")

        self.gridLayout_63.addWidget(self.manage_edit_btn, 3, 1, 1, 1)

        self.manage_deactivate_btn = QPushButton(self.frame_61)
        self.manage_deactivate_btn.setObjectName(u"manage_deactivate_btn")
        self.manage_deactivate_btn.setMinimumSize(QSize(101, 51))
        self.manage_deactivate_btn.setMaximumSize(QSize(16777215, 16777215))
        self.manage_deactivate_btn.setStyleSheet(u"background-color: rgb(204, 204, 204);")

        self.gridLayout_63.addWidget(self.manage_deactivate_btn, 3, 2, 1, 1)

        self.line_58 = QFrame(self.frame_61)
        self.line_58.setObjectName(u"line_58")
        self.line_58.setFrameShape(QFrame.Shape.VLine)
        self.line_58.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_63.addWidget(self.line_58, 3, 3, 1, 1)

        self.manager_hr_back_btn = QPushButton(self.frame_61)
        self.manager_hr_back_btn.setObjectName(u"manager_hr_back_btn")
        self.manager_hr_back_btn.setMinimumSize(QSize(101, 51))
        self.manager_hr_back_btn.setMaximumSize(QSize(16777215, 16777215))
        self.manager_hr_back_btn.setStyleSheet(u"background-color: rgb(204, 204, 204);")

        self.gridLayout_63.addWidget(self.manager_hr_back_btn, 3, 4, 1, 1)


        self.gridLayout_60.addWidget(self.frame_61, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.admin_hr_page)
        self.employee_enroll_bio1_page = QWidget()
        self.employee_enroll_bio1_page.setObjectName(u"employee_enroll_bio1_page")
        self.gridLayout_14 = QGridLayout(self.employee_enroll_bio1_page)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.frame_21 = QFrame(self.employee_enroll_bio1_page)
        self.frame_21.setObjectName(u"frame_21")
        self.frame_21.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_21.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_15 = QGridLayout(self.frame_21)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.frame_22 = QFrame(self.frame_21)
        self.frame_22.setObjectName(u"frame_22")
        self.frame_22.setMinimumSize(QSize(511, 251))
        self.frame_22.setMaximumSize(QSize(16777215, 16777215))
        self.frame_22.setStyleSheet(u"background-color: transparent;\n"
"border: none;")
        self.frame_22.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_22.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_15.addWidget(self.frame_22, 0, 1, 1, 2)

        self.frame_24 = QFrame(self.frame_21)
        self.frame_24.setObjectName(u"frame_24")
        self.frame_24.setStyleSheet(u"background-color: transparent;\n"
"border: none;")
        self.frame_24.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_24.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_15.addWidget(self.frame_24, 4, 1, 1, 1)

        self.label_33 = QLabel(self.frame_21)
        self.label_33.setObjectName(u"label_33")
        self.label_33.setMinimumSize(QSize(0, 38))
        self.label_33.setMaximumSize(QSize(16777215, 38))
        self.label_33.setFont(font3)
        self.label_33.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_15.addWidget(self.label_33, 2, 1, 1, 2)

        self.label_31 = QLabel(self.frame_21)
        self.label_31.setObjectName(u"label_31")
        self.label_31.setMinimumSize(QSize(701, 661))
        self.label_31.setStyleSheet(u"background-color: rgb(241, 241, 241);")
        self.label_31.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_15.addWidget(self.label_31, 0, 0, 5, 1)

        self.bio_cancel_btn = QPushButton(self.frame_21)
        self.bio_cancel_btn.setObjectName(u"bio_cancel_btn")
        self.bio_cancel_btn.setMinimumSize(QSize(101, 51))
        self.bio_cancel_btn.setMaximumSize(QSize(101, 16777215))
        self.bio_cancel_btn.setStyleSheet(u"background-color: rgb(204, 204, 204);")

        self.gridLayout_15.addWidget(self.bio_cancel_btn, 4, 2, 1, 1)

        self.label_32 = QLabel(self.frame_21)
        self.label_32.setObjectName(u"label_32")
        self.label_32.setMinimumSize(QSize(0, 49))
        self.label_32.setMaximumSize(QSize(16777215, 49))
        self.label_32.setFont(font)
        self.label_32.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_15.addWidget(self.label_32, 1, 1, 1, 2)

        self.frame_23 = QFrame(self.frame_21)
        self.frame_23.setObjectName(u"frame_23")
        self.frame_23.setMinimumSize(QSize(511, 251))
        self.frame_23.setMaximumSize(QSize(16777215, 16777215))
        self.frame_23.setStyleSheet(u"background-color: transparent;\n"
"border: none;")
        self.frame_23.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_23.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_15.addWidget(self.frame_23, 3, 1, 1, 2)


        self.gridLayout_14.addWidget(self.frame_21, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.employee_enroll_bio1_page)
        self.admin_settings_page = QWidget()
        self.admin_settings_page.setObjectName(u"admin_settings_page")
        self.gridLayout_46 = QGridLayout(self.admin_settings_page)
        self.gridLayout_46.setObjectName(u"gridLayout_46")
        self.settings_home_btn = QPushButton(self.admin_settings_page)
        self.settings_home_btn.setObjectName(u"settings_home_btn")
        self.settings_home_btn.setMinimumSize(QSize(71, 71))
        self.settings_home_btn.setMaximumSize(QSize(71, 71))

        self.gridLayout_46.addWidget(self.settings_home_btn, 0, 0, 1, 1)

        self.line_39 = QFrame(self.admin_settings_page)
        self.line_39.setObjectName(u"line_39")
        self.line_39.setStyleSheet(u"border: 0px;\n"
"")
        self.line_39.setFrameShape(QFrame.Shape.VLine)
        self.line_39.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_46.addWidget(self.line_39, 0, 1, 6, 1)

        self.frame_73 = QFrame(self.admin_settings_page)
        self.frame_73.setObjectName(u"frame_73")
        self.frame_73.setMinimumSize(QSize(1148, 684))
        self.frame_73.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_73.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_50 = QGridLayout(self.frame_73)
        self.gridLayout_50.setObjectName(u"gridLayout_50")
        self.groupBox_14 = QGroupBox(self.frame_73)
        self.groupBox_14.setObjectName(u"groupBox_14")
        self.groupBox_14.setMinimumSize(QSize(631, 311))
        self.gridLayout_51 = QGridLayout(self.groupBox_14)
        self.gridLayout_51.setObjectName(u"gridLayout_51")
        self.tableWidget_5 = QTableWidget(self.groupBox_14)
        if (self.tableWidget_5.columnCount() < 2):
            self.tableWidget_5.setColumnCount(2)
        __qtablewidgetitem15 = QTableWidgetItem()
        self.tableWidget_5.setHorizontalHeaderItem(0, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        self.tableWidget_5.setHorizontalHeaderItem(1, __qtablewidgetitem16)
        self.tableWidget_5.setObjectName(u"tableWidget_5")
        self.tableWidget_5.horizontalHeader().setDefaultSectionSize(300)
        self.tableWidget_5.horizontalHeader().setStretchLastSection(True)

        self.gridLayout_51.addWidget(self.tableWidget_5, 0, 0, 1, 1)

        self.line_60 = QFrame(self.groupBox_14)
        self.line_60.setObjectName(u"line_60")
        self.line_60.setMinimumSize(QSize(0, 0))
        self.line_60.setFrameShape(QFrame.Shape.HLine)
        self.line_60.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_51.addWidget(self.line_60, 1, 0, 1, 1)

        self.label_77 = QLabel(self.groupBox_14)
        self.label_77.setObjectName(u"label_77")
        self.label_77.setMinimumSize(QSize(0, 0))

        self.gridLayout_51.addWidget(self.label_77, 2, 0, 1, 1)


        self.gridLayout_50.addWidget(self.groupBox_14, 0, 1, 1, 1)

        self.groupBox_17 = QGroupBox(self.frame_73)
        self.groupBox_17.setObjectName(u"groupBox_17")
        self.gridLayout_48 = QGridLayout(self.groupBox_17)
        self.gridLayout_48.setObjectName(u"gridLayout_48")
        self.frame_82 = QFrame(self.groupBox_17)
        self.frame_82.setObjectName(u"frame_82")
        self.frame_82.setMinimumSize(QSize(166, 0))
        self.frame_82.setStyleSheet(u"background-color: transparent;\n"
"border: none;")
        self.frame_82.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_82.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_48.addWidget(self.frame_82, 1, 0, 1, 2)

        self.label_87 = QLabel(self.groupBox_17)
        self.label_87.setObjectName(u"label_87")
        self.label_87.setMinimumSize(QSize(0, 0))
        self.label_87.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_48.addWidget(self.label_87, 0, 4, 1, 1)

        self.label_86 = QLabel(self.groupBox_17)
        self.label_86.setObjectName(u"label_86")
        self.label_86.setMinimumSize(QSize(0, 0))
        self.label_86.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_48.addWidget(self.label_86, 0, 0, 1, 1)

        self.frame_83 = QFrame(self.groupBox_17)
        self.frame_83.setObjectName(u"frame_83")
        self.frame_83.setMinimumSize(QSize(143, 0))
        self.frame_83.setStyleSheet(u"background-color: transparent;\n"
"border: none;")
        self.frame_83.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_83.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_48.addWidget(self.frame_83, 1, 5, 1, 1)

        self.dateEdit_4 = QDateEdit(self.groupBox_17)
        self.dateEdit_4.setObjectName(u"dateEdit_4")

        self.gridLayout_48.addWidget(self.dateEdit_4, 0, 5, 1, 1)

        self.dateEdit_3 = QDateEdit(self.groupBox_17)
        self.dateEdit_3.setObjectName(u"dateEdit_3")

        self.gridLayout_48.addWidget(self.dateEdit_3, 0, 1, 1, 2)

        self.frame_81 = QFrame(self.groupBox_17)
        self.frame_81.setObjectName(u"frame_81")
        self.frame_81.setMinimumSize(QSize(68, 0))
        self.frame_81.setStyleSheet(u"background-color: transparent;\n"
"border: none;")
        self.frame_81.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_81.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_48.addWidget(self.frame_81, 0, 3, 1, 1)

        self.restore_btn = QPushButton(self.groupBox_17)
        self.restore_btn.setObjectName(u"restore_btn")
        self.restore_btn.setMinimumSize(QSize(151, 41))
        self.restore_btn.setMaximumSize(QSize(16777215, 16777215))
        self.restore_btn.setStyleSheet(u"background-color: rgb(204, 204, 204);")

        self.gridLayout_48.addWidget(self.restore_btn, 1, 2, 1, 3)


        self.gridLayout_50.addWidget(self.groupBox_17, 2, 0, 1, 1)

        self.groupBox_15 = QGroupBox(self.frame_73)
        self.groupBox_15.setObjectName(u"groupBox_15")
        self.groupBox_15.setMinimumSize(QSize(631, 311))
        self.gridLayout_52 = QGridLayout(self.groupBox_15)
        self.gridLayout_52.setObjectName(u"gridLayout_52")
        self.tableWidget_6 = QTableWidget(self.groupBox_15)
        if (self.tableWidget_6.columnCount() < 1):
            self.tableWidget_6.setColumnCount(1)
        __qtablewidgetitem17 = QTableWidgetItem()
        self.tableWidget_6.setHorizontalHeaderItem(0, __qtablewidgetitem17)
        self.tableWidget_6.setObjectName(u"tableWidget_6")
        self.tableWidget_6.horizontalHeader().setDefaultSectionSize(300)
        self.tableWidget_6.horizontalHeader().setStretchLastSection(True)

        self.gridLayout_52.addWidget(self.tableWidget_6, 0, 0, 1, 1)

        self.line_62 = QFrame(self.groupBox_15)
        self.line_62.setObjectName(u"line_62")
        self.line_62.setMinimumSize(QSize(0, 0))
        self.line_62.setFrameShape(QFrame.Shape.HLine)
        self.line_62.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_52.addWidget(self.line_62, 1, 0, 1, 1)

        self.label_78 = QLabel(self.groupBox_15)
        self.label_78.setObjectName(u"label_78")
        self.label_78.setMinimumSize(QSize(0, 0))

        self.gridLayout_52.addWidget(self.label_78, 2, 0, 1, 1)


        self.gridLayout_50.addWidget(self.groupBox_15, 1, 1, 3, 1)

        self.groupBox_18 = QGroupBox(self.frame_73)
        self.groupBox_18.setObjectName(u"groupBox_18")
        self.gridLayout_49 = QGridLayout(self.groupBox_18)
        self.gridLayout_49.setObjectName(u"gridLayout_49")
        self.label_88 = QLabel(self.groupBox_18)
        self.label_88.setObjectName(u"label_88")
        self.label_88.setMinimumSize(QSize(0, 0))
        self.label_88.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_49.addWidget(self.label_88, 0, 0, 1, 1)

        self.dateEdit_5 = QDateEdit(self.groupBox_18)
        self.dateEdit_5.setObjectName(u"dateEdit_5")

        self.gridLayout_49.addWidget(self.dateEdit_5, 0, 1, 1, 1)

        self.archive_btn = QPushButton(self.groupBox_18)
        self.archive_btn.setObjectName(u"archive_btn")
        self.archive_btn.setMinimumSize(QSize(151, 41))
        self.archive_btn.setMaximumSize(QSize(16777215, 16777215))
        self.archive_btn.setStyleSheet(u"background-color: rgb(204, 204, 204);")

        self.gridLayout_49.addWidget(self.archive_btn, 0, 2, 1, 1)


        self.gridLayout_50.addWidget(self.groupBox_18, 3, 0, 1, 1)

        self.groupBox_16 = QGroupBox(self.frame_73)
        self.groupBox_16.setObjectName(u"groupBox_16")
        self.groupBox_16.setMinimumSize(QSize(451, 351))
        self.gridLayout_47 = QGridLayout(self.groupBox_16)
        self.gridLayout_47.setObjectName(u"gridLayout_47")
        self.frame_99 = QFrame(self.groupBox_16)
        self.frame_99.setObjectName(u"frame_99")
        self.frame_99.setMinimumSize(QSize(138, 0))
        self.frame_99.setStyleSheet(u"background-color: transparent;\n"
"border: none;")
        self.frame_99.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_99.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_47.addWidget(self.frame_99, 0, 0, 1, 5)

        self.label_85 = QLabel(self.groupBox_16)
        self.label_85.setObjectName(u"label_85")
        self.label_85.setMinimumSize(QSize(471, 0))

        self.gridLayout_47.addWidget(self.label_85, 1, 0, 1, 5)

        self.frame_98 = QFrame(self.groupBox_16)
        self.frame_98.setObjectName(u"frame_98")
        self.frame_98.setMinimumSize(QSize(138, 0))
        self.frame_98.setStyleSheet(u"background-color: transparent;\n"
"border: none;")
        self.frame_98.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_98.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_47.addWidget(self.frame_98, 2, 0, 1, 5)

        self.lineEdit_17 = QLineEdit(self.groupBox_16)
        self.lineEdit_17.setObjectName(u"lineEdit_17")
        self.lineEdit_17.setMinimumSize(QSize(471, 41))
        self.lineEdit_17.setStyleSheet(u"background-color: rgb(238, 238, 238);")

        self.gridLayout_47.addWidget(self.lineEdit_17, 3, 0, 1, 5)

        self.label_84 = QLabel(self.groupBox_16)
        self.label_84.setObjectName(u"label_84")
        self.label_84.setMinimumSize(QSize(88, 0))
        self.label_84.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_47.addWidget(self.label_84, 4, 0, 1, 1)

        self.dateEdit = QDateEdit(self.groupBox_16)
        self.dateEdit.setObjectName(u"dateEdit")
        self.dateEdit.setMinimumSize(QSize(121, 24))

        self.gridLayout_47.addWidget(self.dateEdit, 4, 1, 1, 2)

        self.label_83 = QLabel(self.groupBox_16)
        self.label_83.setObjectName(u"label_83")
        self.label_83.setMinimumSize(QSize(0, 0))
        self.label_83.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_47.addWidget(self.label_83, 4, 3, 1, 1)

        self.dateEdit_2 = QDateEdit(self.groupBox_16)
        self.dateEdit_2.setObjectName(u"dateEdit_2")
        self.dateEdit_2.setMinimumSize(QSize(121, 24))

        self.gridLayout_47.addWidget(self.dateEdit_2, 4, 4, 1, 1)

        self.frame_90 = QFrame(self.groupBox_16)
        self.frame_90.setObjectName(u"frame_90")
        self.frame_90.setMinimumSize(QSize(138, 0))
        self.frame_90.setStyleSheet(u"background-color: transparent;\n"
"border: none;")
        self.frame_90.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_90.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_47.addWidget(self.frame_90, 5, 0, 1, 2)

        self.manual_backup_btn = QPushButton(self.groupBox_16)
        self.manual_backup_btn.setObjectName(u"manual_backup_btn")
        self.manual_backup_btn.setMinimumSize(QSize(151, 42))
        self.manual_backup_btn.setMaximumSize(QSize(16777215, 16777215))
        self.manual_backup_btn.setStyleSheet(u"background-color: rgb(204, 204, 204);")

        self.gridLayout_47.addWidget(self.manual_backup_btn, 5, 2, 1, 2)

        self.frame_91 = QFrame(self.groupBox_16)
        self.frame_91.setObjectName(u"frame_91")
        self.frame_91.setMinimumSize(QSize(138, 0))
        self.frame_91.setStyleSheet(u"background-color: transparent;\n"
"border: none;")
        self.frame_91.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_91.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_47.addWidget(self.frame_91, 5, 4, 1, 1)

        self.line_61 = QFrame(self.groupBox_16)
        self.line_61.setObjectName(u"line_61")
        self.line_61.setMinimumSize(QSize(0, 0))
        self.line_61.setFrameShape(QFrame.Shape.HLine)
        self.line_61.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_47.addWidget(self.line_61, 6, 0, 1, 5)

        self.label_82 = QLabel(self.groupBox_16)
        self.label_82.setObjectName(u"label_82")
        self.label_82.setMinimumSize(QSize(464, 0))

        self.gridLayout_47.addWidget(self.label_82, 7, 0, 1, 5)

        self.frame_93 = QFrame(self.groupBox_16)
        self.frame_93.setObjectName(u"frame_93")
        self.frame_93.setMinimumSize(QSize(138, 0))
        self.frame_93.setStyleSheet(u"background-color: transparent;\n"
"border: none;")
        self.frame_93.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_93.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_47.addWidget(self.frame_93, 8, 0, 1, 5)

        self.frame_75 = QFrame(self.groupBox_16)
        self.frame_75.setObjectName(u"frame_75")
        self.frame_75.setMinimumSize(QSize(471, 0))
        self.frame_75.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.frame_75.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_75.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_75)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.radioButton_10 = QRadioButton(self.frame_75)
        self.radioButton_10.setObjectName(u"radioButton_10")

        self.horizontalLayout_4.addWidget(self.radioButton_10)

        self.radioButton_11 = QRadioButton(self.frame_75)
        self.radioButton_11.setObjectName(u"radioButton_11")

        self.horizontalLayout_4.addWidget(self.radioButton_11)

        self.radioButton_12 = QRadioButton(self.frame_75)
        self.radioButton_12.setObjectName(u"radioButton_12")

        self.horizontalLayout_4.addWidget(self.radioButton_12)


        self.gridLayout_47.addWidget(self.frame_75, 9, 0, 1, 5)

        self.frame_88 = QFrame(self.groupBox_16)
        self.frame_88.setObjectName(u"frame_88")
        self.frame_88.setMinimumSize(QSize(138, 0))
        self.frame_88.setStyleSheet(u"background-color: transparent;\n"
"border: none;")
        self.frame_88.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_88.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_47.addWidget(self.frame_88, 10, 0, 1, 2)

        self.automatic_backup_btn = QPushButton(self.groupBox_16)
        self.automatic_backup_btn.setObjectName(u"automatic_backup_btn")
        self.automatic_backup_btn.setMinimumSize(QSize(151, 41))
        self.automatic_backup_btn.setMaximumSize(QSize(16777215, 16777215))
        self.automatic_backup_btn.setStyleSheet(u"background-color: rgb(204, 204, 204);")

        self.gridLayout_47.addWidget(self.automatic_backup_btn, 10, 2, 1, 2)

        self.frame_89 = QFrame(self.groupBox_16)
        self.frame_89.setObjectName(u"frame_89")
        self.frame_89.setMinimumSize(QSize(138, 0))
        self.frame_89.setStyleSheet(u"background-color: transparent;\n"
"border: none;")
        self.frame_89.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_89.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_47.addWidget(self.frame_89, 10, 4, 1, 1)

        self.frame_92 = QFrame(self.groupBox_16)
        self.frame_92.setObjectName(u"frame_92")
        self.frame_92.setMinimumSize(QSize(138, 0))
        self.frame_92.setStyleSheet(u"background-color: transparent;\n"
"border: none;")
        self.frame_92.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_92.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_47.addWidget(self.frame_92, 11, 0, 1, 5)

        self.line_59 = QFrame(self.groupBox_16)
        self.line_59.setObjectName(u"line_59")
        self.line_59.setMinimumSize(QSize(1, 0))
        self.line_59.setFrameShape(QFrame.Shape.HLine)
        self.line_59.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_47.addWidget(self.line_59, 12, 0, 1, 5)

        self.label_76 = QLabel(self.groupBox_16)
        self.label_76.setObjectName(u"label_76")
        self.label_76.setMinimumSize(QSize(461, 20))

        self.gridLayout_47.addWidget(self.label_76, 13, 0, 1, 5)


        self.gridLayout_50.addWidget(self.groupBox_16, 0, 0, 2, 1)


        self.gridLayout_46.addWidget(self.frame_73, 0, 2, 6, 1)

        self.line_40 = QFrame(self.admin_settings_page)
        self.line_40.setObjectName(u"line_40")
        self.line_40.setFrameShape(QFrame.Shape.HLine)
        self.line_40.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_46.addWidget(self.line_40, 1, 0, 1, 1)

        self.settings_employee_btn = QPushButton(self.admin_settings_page)
        self.settings_employee_btn.setObjectName(u"settings_employee_btn")
        self.settings_employee_btn.setMinimumSize(QSize(71, 71))
        self.settings_employee_btn.setMaximumSize(QSize(71, 71))

        self.gridLayout_46.addWidget(self.settings_employee_btn, 2, 0, 1, 1)

        self.line_41 = QFrame(self.admin_settings_page)
        self.line_41.setObjectName(u"line_41")
        self.line_41.setFrameShape(QFrame.Shape.HLine)
        self.line_41.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_46.addWidget(self.line_41, 3, 0, 1, 1)

        self.settings_settings_btn = QPushButton(self.admin_settings_page)
        self.settings_settings_btn.setObjectName(u"settings_settings_btn")
        self.settings_settings_btn.setMinimumSize(QSize(71, 71))
        self.settings_settings_btn.setMaximumSize(QSize(71, 71))

        self.gridLayout_46.addWidget(self.settings_settings_btn, 4, 0, 1, 1)

        self.frame_74 = QFrame(self.admin_settings_page)
        self.frame_74.setObjectName(u"frame_74")
        self.frame_74.setStyleSheet(u"background-color: transparent;\n"
"border: none;")
        self.frame_74.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_74.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_46.addWidget(self.frame_74, 5, 0, 1, 1)

        self.stackedWidget.addWidget(self.admin_settings_page)
        self.view_employee_page = QWidget()
        self.view_employee_page.setObjectName(u"view_employee_page")
        self.gridLayout_24 = QGridLayout(self.view_employee_page)
        self.gridLayout_24.setObjectName(u"gridLayout_24")
        self.frame_38 = QFrame(self.view_employee_page)
        self.frame_38.setObjectName(u"frame_38")
        self.frame_38.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_38.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_26 = QGridLayout(self.frame_38)
        self.gridLayout_26.setObjectName(u"gridLayout_26")
        self.groupBox_8 = QGroupBox(self.frame_38)
        self.groupBox_8.setObjectName(u"groupBox_8")
        self.groupBox_8.setMinimumSize(QSize(531, 664))
        self.gridLayout_25 = QGridLayout(self.groupBox_8)
        self.gridLayout_25.setObjectName(u"gridLayout_25")
        self.frame_44 = QFrame(self.groupBox_8)
        self.frame_44.setObjectName(u"frame_44")
        self.frame_44.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_44.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_25.addWidget(self.frame_44, 0, 0, 1, 5)

        self.label_46 = QLabel(self.groupBox_8)
        self.label_46.setObjectName(u"label_46")
        self.label_46.setMinimumSize(QSize(190, 190))
        self.label_46.setStyleSheet(u"background-color: rgb(241, 241, 241);")
        self.label_46.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_25.addWidget(self.label_46, 0, 5, 1, 1)

        self.frame_45 = QFrame(self.groupBox_8)
        self.frame_45.setObjectName(u"frame_45")
        self.frame_45.setMinimumSize(QSize(163, 0))
        self.frame_45.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_45.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_25.addWidget(self.frame_45, 0, 6, 1, 1)

        self.line_22 = QFrame(self.groupBox_8)
        self.line_22.setObjectName(u"line_22")
        self.line_22.setMinimumSize(QSize(0, 28))
        self.line_22.setFrameShape(QFrame.Shape.HLine)
        self.line_22.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_25.addWidget(self.line_22, 1, 0, 1, 7)

        self.label_44 = QLabel(self.groupBox_8)
        self.label_44.setObjectName(u"label_44")
        self.label_44.setMinimumSize(QSize(0, 0))

        self.gridLayout_25.addWidget(self.label_44, 2, 0, 1, 1)

        self.frame_43 = QFrame(self.groupBox_8)
        self.frame_43.setObjectName(u"frame_43")
        self.frame_43.setStyleSheet(u"background-color: transparent;\n"
"border: None;")
        self.frame_43.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_43.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_25.addWidget(self.frame_43, 2, 1, 1, 6)

        self.label_48 = QLabel(self.groupBox_8)
        self.label_48.setObjectName(u"label_48")
        self.label_48.setMinimumSize(QSize(0, 0))
        self.label_48.setStyleSheet(u"background-color: rgb(240, 240, 240);")
        self.label_48.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_25.addWidget(self.label_48, 3, 0, 1, 7)

        self.line_25 = QFrame(self.groupBox_8)
        self.line_25.setObjectName(u"line_25")
        self.line_25.setMinimumSize(QSize(0, 25))
        self.line_25.setFrameShape(QFrame.Shape.HLine)
        self.line_25.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_25.addWidget(self.line_25, 4, 0, 1, 7)

        self.label_43 = QLabel(self.groupBox_8)
        self.label_43.setObjectName(u"label_43")
        self.label_43.setMinimumSize(QSize(0, 0))

        self.gridLayout_25.addWidget(self.label_43, 5, 0, 2, 4)

        self.frame_42 = QFrame(self.groupBox_8)
        self.frame_42.setObjectName(u"frame_42")
        self.frame_42.setStyleSheet(u"background-color: transparent;\n"
"border: None;")
        self.frame_42.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_42.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_25.addWidget(self.frame_42, 6, 3, 1, 4)

        self.label_49 = QLabel(self.groupBox_8)
        self.label_49.setObjectName(u"label_49")
        self.label_49.setMinimumSize(QSize(0, 0))
        self.label_49.setStyleSheet(u"background-color: rgb(240, 240, 240);")
        self.label_49.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_25.addWidget(self.label_49, 7, 0, 1, 7)

        self.line_26 = QFrame(self.groupBox_8)
        self.line_26.setObjectName(u"line_26")
        self.line_26.setMinimumSize(QSize(0, 25))
        self.line_26.setFrameShape(QFrame.Shape.HLine)
        self.line_26.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_25.addWidget(self.line_26, 8, 0, 1, 7)

        self.label_47 = QLabel(self.groupBox_8)
        self.label_47.setObjectName(u"label_47")
        self.label_47.setMinimumSize(QSize(0, 0))

        self.gridLayout_25.addWidget(self.label_47, 9, 0, 2, 2)

        self.frame_40 = QFrame(self.groupBox_8)
        self.frame_40.setObjectName(u"frame_40")
        self.frame_40.setStyleSheet(u"background-color: transparent;\n"
"border: None;")
        self.frame_40.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_40.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_25.addWidget(self.frame_40, 10, 2, 1, 5)

        self.label_50 = QLabel(self.groupBox_8)
        self.label_50.setObjectName(u"label_50")
        self.label_50.setMinimumSize(QSize(0, 0))
        self.label_50.setStyleSheet(u"background-color: rgb(240, 240, 240);")
        self.label_50.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_25.addWidget(self.label_50, 11, 0, 1, 7)

        self.line_24 = QFrame(self.groupBox_8)
        self.line_24.setObjectName(u"line_24")
        self.line_24.setFrameShape(QFrame.Shape.HLine)
        self.line_24.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_25.addWidget(self.line_24, 12, 0, 1, 7)

        self.label_45 = QLabel(self.groupBox_8)
        self.label_45.setObjectName(u"label_45")

        self.gridLayout_25.addWidget(self.label_45, 13, 0, 2, 4)

        self.frame_41 = QFrame(self.groupBox_8)
        self.frame_41.setObjectName(u"frame_41")
        self.frame_41.setStyleSheet(u"background-color: transparent;\n"
"border: None;")
        self.frame_41.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_41.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_25.addWidget(self.frame_41, 14, 4, 1, 3)

        self.frame_39 = QFrame(self.groupBox_8)
        self.frame_39.setObjectName(u"frame_39")
        self.frame_39.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.frame_39.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_39.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_39)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.radioButton_4 = QRadioButton(self.frame_39)
        self.radioButton_4.setObjectName(u"radioButton_4")
        self.radioButton_4.setEnabled(False)

        self.horizontalLayout_2.addWidget(self.radioButton_4)

        self.radioButton_5 = QRadioButton(self.frame_39)
        self.radioButton_5.setObjectName(u"radioButton_5")
        self.radioButton_5.setEnabled(False)

        self.horizontalLayout_2.addWidget(self.radioButton_5)

        self.radioButton_6 = QRadioButton(self.frame_39)
        self.radioButton_6.setObjectName(u"radioButton_6")
        self.radioButton_6.setEnabled(False)

        self.horizontalLayout_2.addWidget(self.radioButton_6)


        self.gridLayout_25.addWidget(self.frame_39, 15, 0, 1, 7)

        self.line_23 = QFrame(self.groupBox_8)
        self.line_23.setObjectName(u"line_23")
        self.line_23.setFrameShape(QFrame.Shape.HLine)
        self.line_23.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_25.addWidget(self.line_23, 16, 0, 1, 7)


        self.gridLayout_26.addWidget(self.groupBox_8, 0, 0, 2, 1)

        self.groupBox_9 = QGroupBox(self.frame_38)
        self.groupBox_9.setObjectName(u"groupBox_9")
        self.groupBox_9.setMinimumSize(QSize(661, 591))
        self.gridLayout_27 = QGridLayout(self.groupBox_9)
        self.gridLayout_27.setObjectName(u"gridLayout_27")
        self.tableWidget_3 = QTableWidget(self.groupBox_9)
        if (self.tableWidget_3.columnCount() < 4):
            self.tableWidget_3.setColumnCount(4)
        __qtablewidgetitem18 = QTableWidgetItem()
        self.tableWidget_3.setHorizontalHeaderItem(0, __qtablewidgetitem18)
        __qtablewidgetitem19 = QTableWidgetItem()
        self.tableWidget_3.setHorizontalHeaderItem(1, __qtablewidgetitem19)
        __qtablewidgetitem20 = QTableWidgetItem()
        self.tableWidget_3.setHorizontalHeaderItem(2, __qtablewidgetitem20)
        __qtablewidgetitem21 = QTableWidgetItem()
        self.tableWidget_3.setHorizontalHeaderItem(3, __qtablewidgetitem21)
        self.tableWidget_3.setObjectName(u"tableWidget_3")
        self.tableWidget_3.horizontalHeader().setDefaultSectionSize(133)
        self.tableWidget_3.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_3.verticalHeader().setStretchLastSection(False)

        self.gridLayout_27.addWidget(self.tableWidget_3, 0, 0, 1, 1)


        self.gridLayout_26.addWidget(self.groupBox_9, 0, 1, 1, 2)

        self.frame_46 = QFrame(self.frame_38)
        self.frame_46.setObjectName(u"frame_46")
        self.frame_46.setStyleSheet(u"background-color: transparent;\n"
"border: None;")
        self.frame_46.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_46.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_26.addWidget(self.frame_46, 1, 1, 1, 1)

        self.view_employee_back_btn = QPushButton(self.frame_38)
        self.view_employee_back_btn.setObjectName(u"view_employee_back_btn")
        self.view_employee_back_btn.setMinimumSize(QSize(101, 51))
        self.view_employee_back_btn.setMaximumSize(QSize(16777215, 16777215))
        self.view_employee_back_btn.setStyleSheet(u"background-color: rgb(204, 204, 204);")

        self.gridLayout_26.addWidget(self.view_employee_back_btn, 1, 2, 1, 1)


        self.gridLayout_24.addWidget(self.frame_38, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.view_employee_page)
        self.admin_home_page = QWidget()
        self.admin_home_page.setObjectName(u"admin_home_page")
        self.gridLayout_33 = QGridLayout(self.admin_home_page)
        self.gridLayout_33.setObjectName(u"gridLayout_33")
        self.home_home_btn = QPushButton(self.admin_home_page)
        self.home_home_btn.setObjectName(u"home_home_btn")
        self.home_home_btn.setMinimumSize(QSize(71, 71))
        self.home_home_btn.setMaximumSize(QSize(71, 71))

        self.gridLayout_33.addWidget(self.home_home_btn, 0, 0, 1, 1)

        self.line_46 = QFrame(self.admin_home_page)
        self.line_46.setObjectName(u"line_46")
        self.line_46.setStyleSheet(u"border: 0px;\n"
"")
        self.line_46.setFrameShape(QFrame.Shape.VLine)
        self.line_46.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_33.addWidget(self.line_46, 0, 1, 6, 1)

        self.frame_85 = QFrame(self.admin_home_page)
        self.frame_85.setObjectName(u"frame_85")
        self.frame_85.setMinimumSize(QSize(1148, 684))
        self.frame_85.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_85.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_39 = QGridLayout(self.frame_85)
        self.gridLayout_39.setObjectName(u"gridLayout_39")
        self.groupBox_19 = QGroupBox(self.frame_85)
        self.groupBox_19.setObjectName(u"groupBox_19")
        self.groupBox_19.setMinimumSize(QSize(286, 151))
        self.gridLayout_35 = QGridLayout(self.groupBox_19)
        self.gridLayout_35.setObjectName(u"gridLayout_35")
        self.label_58 = QLabel(self.groupBox_19)
        self.label_58.setObjectName(u"label_58")
        self.label_58.setMinimumSize(QSize(0, 0))
        font4 = QFont()
        font4.setPointSize(34)
        self.label_58.setFont(font4)
        self.label_58.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_35.addWidget(self.label_58, 0, 0, 1, 1)


        self.gridLayout_39.addWidget(self.groupBox_19, 0, 0, 1, 1)

        self.groupBox_22 = QGroupBox(self.frame_85)
        self.groupBox_22.setObjectName(u"groupBox_22")
        self.groupBox_22.setMinimumSize(QSize(282, 151))
        self.gridLayout_36 = QGridLayout(self.groupBox_22)
        self.gridLayout_36.setObjectName(u"gridLayout_36")
        self.label_59 = QLabel(self.groupBox_22)
        self.label_59.setObjectName(u"label_59")
        self.label_59.setMinimumSize(QSize(0, 0))
        self.label_59.setFont(font4)
        self.label_59.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_36.addWidget(self.label_59, 0, 0, 1, 1)


        self.gridLayout_39.addWidget(self.groupBox_22, 0, 1, 1, 1)

        self.groupBox_23 = QGroupBox(self.frame_85)
        self.groupBox_23.setObjectName(u"groupBox_23")
        self.groupBox_23.setMinimumSize(QSize(276, 151))
        self.gridLayout_37 = QGridLayout(self.groupBox_23)
        self.gridLayout_37.setObjectName(u"gridLayout_37")
        self.label_60 = QLabel(self.groupBox_23)
        self.label_60.setObjectName(u"label_60")
        self.label_60.setMinimumSize(QSize(0, 0))
        self.label_60.setFont(font4)
        self.label_60.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_37.addWidget(self.label_60, 0, 0, 1, 1)


        self.gridLayout_39.addWidget(self.groupBox_23, 0, 2, 1, 1)

        self.groupBox_24 = QGroupBox(self.frame_85)
        self.groupBox_24.setObjectName(u"groupBox_24")
        self.groupBox_24.setMinimumSize(QSize(261, 151))
        self.gridLayout_38 = QGridLayout(self.groupBox_24)
        self.gridLayout_38.setObjectName(u"gridLayout_38")
        self.label_61 = QLabel(self.groupBox_24)
        self.label_61.setObjectName(u"label_61")
        self.label_61.setMinimumSize(QSize(0, 0))
        self.label_61.setFont(font4)
        self.label_61.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_38.addWidget(self.label_61, 0, 0, 1, 1)


        self.gridLayout_39.addWidget(self.groupBox_24, 0, 3, 1, 2)

        self.groupBox_21 = QGroupBox(self.frame_85)
        self.groupBox_21.setObjectName(u"groupBox_21")
        self.groupBox_21.setMinimumSize(QSize(1121, 411))
        self.gridLayout_34 = QGridLayout(self.groupBox_21)
        self.gridLayout_34.setObjectName(u"gridLayout_34")
        self.tableWidget_4 = QTableWidget(self.groupBox_21)
        if (self.tableWidget_4.columnCount() < 4):
            self.tableWidget_4.setColumnCount(4)
        font5 = QFont()
        font5.setBold(True)
        __qtablewidgetitem22 = QTableWidgetItem()
        __qtablewidgetitem22.setFont(font5);
        self.tableWidget_4.setHorizontalHeaderItem(0, __qtablewidgetitem22)
        __qtablewidgetitem23 = QTableWidgetItem()
        __qtablewidgetitem23.setFont(font5);
        self.tableWidget_4.setHorizontalHeaderItem(1, __qtablewidgetitem23)
        __qtablewidgetitem24 = QTableWidgetItem()
        __qtablewidgetitem24.setFont(font5);
        self.tableWidget_4.setHorizontalHeaderItem(2, __qtablewidgetitem24)
        __qtablewidgetitem25 = QTableWidgetItem()
        __qtablewidgetitem25.setFont(font5);
        self.tableWidget_4.setHorizontalHeaderItem(3, __qtablewidgetitem25)
        if (self.tableWidget_4.rowCount() < 23):
            self.tableWidget_4.setRowCount(23)
        __qtablewidgetitem26 = QTableWidgetItem()
        self.tableWidget_4.setVerticalHeaderItem(0, __qtablewidgetitem26)
        __qtablewidgetitem27 = QTableWidgetItem()
        self.tableWidget_4.setVerticalHeaderItem(1, __qtablewidgetitem27)
        __qtablewidgetitem28 = QTableWidgetItem()
        self.tableWidget_4.setVerticalHeaderItem(2, __qtablewidgetitem28)
        __qtablewidgetitem29 = QTableWidgetItem()
        self.tableWidget_4.setVerticalHeaderItem(3, __qtablewidgetitem29)
        __qtablewidgetitem30 = QTableWidgetItem()
        self.tableWidget_4.setVerticalHeaderItem(4, __qtablewidgetitem30)
        __qtablewidgetitem31 = QTableWidgetItem()
        self.tableWidget_4.setVerticalHeaderItem(5, __qtablewidgetitem31)
        __qtablewidgetitem32 = QTableWidgetItem()
        self.tableWidget_4.setVerticalHeaderItem(6, __qtablewidgetitem32)
        __qtablewidgetitem33 = QTableWidgetItem()
        self.tableWidget_4.setVerticalHeaderItem(7, __qtablewidgetitem33)
        __qtablewidgetitem34 = QTableWidgetItem()
        self.tableWidget_4.setVerticalHeaderItem(8, __qtablewidgetitem34)
        __qtablewidgetitem35 = QTableWidgetItem()
        self.tableWidget_4.setVerticalHeaderItem(9, __qtablewidgetitem35)
        __qtablewidgetitem36 = QTableWidgetItem()
        self.tableWidget_4.setVerticalHeaderItem(10, __qtablewidgetitem36)
        __qtablewidgetitem37 = QTableWidgetItem()
        self.tableWidget_4.setVerticalHeaderItem(11, __qtablewidgetitem37)
        __qtablewidgetitem38 = QTableWidgetItem()
        self.tableWidget_4.setVerticalHeaderItem(12, __qtablewidgetitem38)
        __qtablewidgetitem39 = QTableWidgetItem()
        self.tableWidget_4.setVerticalHeaderItem(13, __qtablewidgetitem39)
        __qtablewidgetitem40 = QTableWidgetItem()
        self.tableWidget_4.setVerticalHeaderItem(14, __qtablewidgetitem40)
        __qtablewidgetitem41 = QTableWidgetItem()
        self.tableWidget_4.setVerticalHeaderItem(15, __qtablewidgetitem41)
        __qtablewidgetitem42 = QTableWidgetItem()
        self.tableWidget_4.setVerticalHeaderItem(16, __qtablewidgetitem42)
        __qtablewidgetitem43 = QTableWidgetItem()
        self.tableWidget_4.setVerticalHeaderItem(17, __qtablewidgetitem43)
        __qtablewidgetitem44 = QTableWidgetItem()
        self.tableWidget_4.setVerticalHeaderItem(18, __qtablewidgetitem44)
        __qtablewidgetitem45 = QTableWidgetItem()
        self.tableWidget_4.setVerticalHeaderItem(19, __qtablewidgetitem45)
        __qtablewidgetitem46 = QTableWidgetItem()
        self.tableWidget_4.setVerticalHeaderItem(20, __qtablewidgetitem46)
        __qtablewidgetitem47 = QTableWidgetItem()
        self.tableWidget_4.setVerticalHeaderItem(21, __qtablewidgetitem47)
        __qtablewidgetitem48 = QTableWidgetItem()
        self.tableWidget_4.setVerticalHeaderItem(22, __qtablewidgetitem48)
        self.tableWidget_4.setObjectName(u"tableWidget_4")
        self.tableWidget_4.horizontalHeader().setDefaultSectionSize(250)
        self.tableWidget_4.horizontalHeader().setStretchLastSection(True)

        self.gridLayout_34.addWidget(self.tableWidget_4, 0, 0, 1, 1)

        self.line_63 = QFrame(self.groupBox_21)
        self.line_63.setObjectName(u"line_63")
        self.line_63.setMinimumSize(QSize(0, 0))
        self.line_63.setFrameShape(QFrame.Shape.HLine)
        self.line_63.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_34.addWidget(self.line_63, 1, 0, 1, 1)

        self.label_79 = QLabel(self.groupBox_21)
        self.label_79.setObjectName(u"label_79")
        self.label_79.setMinimumSize(QSize(0, 0))

        self.gridLayout_34.addWidget(self.label_79, 2, 0, 1, 1)


        self.gridLayout_39.addWidget(self.groupBox_21, 1, 0, 1, 5)

        self.frame_59 = QFrame(self.frame_85)
        self.frame_59.setObjectName(u"frame_59")
        self.frame_59.setStyleSheet(u"background-color: transparent;\n"
"border: None;")
        self.frame_59.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_59.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_39.addWidget(self.frame_59, 2, 0, 1, 4)

        self.home_logout_btn = QPushButton(self.frame_85)
        self.home_logout_btn.setObjectName(u"home_logout_btn")
        self.home_logout_btn.setMinimumSize(QSize(101, 51))
        self.home_logout_btn.setMaximumSize(QSize(16777215, 16777215))
        self.home_logout_btn.setStyleSheet(u"background-color: rgb(204, 204, 204);")

        self.gridLayout_39.addWidget(self.home_logout_btn, 2, 4, 1, 1)


        self.gridLayout_33.addWidget(self.frame_85, 0, 2, 6, 1)

        self.line_51 = QFrame(self.admin_home_page)
        self.line_51.setObjectName(u"line_51")
        self.line_51.setFrameShape(QFrame.Shape.HLine)
        self.line_51.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_33.addWidget(self.line_51, 1, 0, 1, 1)

        self.home_employee_btn = QPushButton(self.admin_home_page)
        self.home_employee_btn.setObjectName(u"home_employee_btn")
        self.home_employee_btn.setMinimumSize(QSize(71, 71))
        self.home_employee_btn.setMaximumSize(QSize(71, 71))

        self.gridLayout_33.addWidget(self.home_employee_btn, 2, 0, 1, 1)

        self.line_47 = QFrame(self.admin_home_page)
        self.line_47.setObjectName(u"line_47")
        self.line_47.setFrameShape(QFrame.Shape.HLine)
        self.line_47.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_33.addWidget(self.line_47, 3, 0, 1, 1)

        self.home_settings_btn = QPushButton(self.admin_home_page)
        self.home_settings_btn.setObjectName(u"home_settings_btn")
        self.home_settings_btn.setMinimumSize(QSize(71, 71))
        self.home_settings_btn.setMaximumSize(QSize(71, 71))

        self.gridLayout_33.addWidget(self.home_settings_btn, 4, 0, 1, 1)

        self.frame_96 = QFrame(self.admin_home_page)
        self.frame_96.setObjectName(u"frame_96")
        self.frame_96.setStyleSheet(u"background-color: transparent;\n"
"border: none;")
        self.frame_96.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_96.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_33.addWidget(self.frame_96, 5, 0, 1, 1)

        self.stackedWidget.addWidget(self.admin_home_page)
        self.hr_home_page = QWidget()
        self.hr_home_page.setObjectName(u"hr_home_page")
        self.gridLayout_58 = QGridLayout(self.hr_home_page)
        self.gridLayout_58.setObjectName(u"gridLayout_58")
        self.line_52 = QFrame(self.hr_home_page)
        self.line_52.setObjectName(u"line_52")
        self.line_52.setFrameShape(QFrame.Shape.HLine)
        self.line_52.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_58.addWidget(self.line_52, 1, 0, 1, 1)

        self.frame_97 = QFrame(self.hr_home_page)
        self.frame_97.setObjectName(u"frame_97")
        self.frame_97.setStyleSheet(u"background-color: transparent;\n"
"border: none;")
        self.frame_97.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_97.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_58.addWidget(self.frame_97, 4, 0, 1, 1)

        self.line_49 = QFrame(self.hr_home_page)
        self.line_49.setObjectName(u"line_49")
        self.line_49.setStyleSheet(u"border: 0px;\n"
"")
        self.line_49.setFrameShape(QFrame.Shape.VLine)
        self.line_49.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_58.addWidget(self.line_49, 0, 1, 5, 1)

        self.frame_86 = QFrame(self.hr_home_page)
        self.frame_86.setObjectName(u"frame_86")
        self.frame_86.setMinimumSize(QSize(1148, 684))
        self.frame_86.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_86.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_40 = QGridLayout(self.frame_86)
        self.gridLayout_40.setObjectName(u"gridLayout_40")
        self.groupBox_25 = QGroupBox(self.frame_86)
        self.groupBox_25.setObjectName(u"groupBox_25")
        self.groupBox_25.setMinimumSize(QSize(261, 151))
        self.gridLayout_41 = QGridLayout(self.groupBox_25)
        self.gridLayout_41.setObjectName(u"gridLayout_41")
        self.label_62 = QLabel(self.groupBox_25)
        self.label_62.setObjectName(u"label_62")
        self.label_62.setMinimumSize(QSize(249, 0))
        self.label_62.setFont(font4)
        self.label_62.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_41.addWidget(self.label_62, 0, 0, 1, 1)


        self.gridLayout_40.addWidget(self.groupBox_25, 0, 0, 1, 1)

        self.groupBox_26 = QGroupBox(self.frame_86)
        self.groupBox_26.setObjectName(u"groupBox_26")
        self.groupBox_26.setMinimumSize(QSize(277, 151))
        self.gridLayout_53 = QGridLayout(self.groupBox_26)
        self.gridLayout_53.setObjectName(u"gridLayout_53")
        self.label_63 = QLabel(self.groupBox_26)
        self.label_63.setObjectName(u"label_63")
        self.label_63.setMinimumSize(QSize(6, 0))
        self.label_63.setFont(font4)
        self.label_63.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_53.addWidget(self.label_63, 0, 0, 1, 1)


        self.gridLayout_40.addWidget(self.groupBox_26, 0, 1, 1, 1)

        self.groupBox_27 = QGroupBox(self.frame_86)
        self.groupBox_27.setObjectName(u"groupBox_27")
        self.groupBox_27.setMinimumSize(QSize(281, 151))
        self.gridLayout_54 = QGridLayout(self.groupBox_27)
        self.gridLayout_54.setObjectName(u"gridLayout_54")
        self.label_64 = QLabel(self.groupBox_27)
        self.label_64.setObjectName(u"label_64")
        self.label_64.setMinimumSize(QSize(0, 0))
        self.label_64.setFont(font4)
        self.label_64.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_54.addWidget(self.label_64, 0, 0, 1, 1)


        self.gridLayout_40.addWidget(self.groupBox_27, 0, 2, 1, 1)

        self.groupBox_28 = QGroupBox(self.frame_86)
        self.groupBox_28.setObjectName(u"groupBox_28")
        self.groupBox_28.setMinimumSize(QSize(259, 151))
        self.gridLayout_56 = QGridLayout(self.groupBox_28)
        self.gridLayout_56.setObjectName(u"gridLayout_56")
        self.label_65 = QLabel(self.groupBox_28)
        self.label_65.setObjectName(u"label_65")
        self.label_65.setMinimumSize(QSize(0, 0))
        self.label_65.setFont(font4)
        self.label_65.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_56.addWidget(self.label_65, 0, 0, 1, 1)


        self.gridLayout_40.addWidget(self.groupBox_28, 0, 3, 1, 3)

        self.groupBox_29 = QGroupBox(self.frame_86)
        self.groupBox_29.setObjectName(u"groupBox_29")
        self.groupBox_29.setMinimumSize(QSize(1121, 411))
        self.gridLayout_57 = QGridLayout(self.groupBox_29)
        self.gridLayout_57.setObjectName(u"gridLayout_57")
        self.tableWidget_9 = QTableWidget(self.groupBox_29)
        if (self.tableWidget_9.columnCount() < 4):
            self.tableWidget_9.setColumnCount(4)
        __qtablewidgetitem49 = QTableWidgetItem()
        self.tableWidget_9.setHorizontalHeaderItem(0, __qtablewidgetitem49)
        __qtablewidgetitem50 = QTableWidgetItem()
        self.tableWidget_9.setHorizontalHeaderItem(1, __qtablewidgetitem50)
        __qtablewidgetitem51 = QTableWidgetItem()
        self.tableWidget_9.setHorizontalHeaderItem(2, __qtablewidgetitem51)
        __qtablewidgetitem52 = QTableWidgetItem()
        self.tableWidget_9.setHorizontalHeaderItem(3, __qtablewidgetitem52)
        self.tableWidget_9.setObjectName(u"tableWidget_9")
        self.tableWidget_9.horizontalHeader().setDefaultSectionSize(250)
        self.tableWidget_9.horizontalHeader().setStretchLastSection(True)

        self.gridLayout_57.addWidget(self.tableWidget_9, 0, 0, 1, 1)


        self.gridLayout_40.addWidget(self.groupBox_29, 1, 0, 1, 6)

        self.frame_60 = QFrame(self.frame_86)
        self.frame_60.setObjectName(u"frame_60")
        self.frame_60.setStyleSheet(u"background-color: transparent;\n"
"border: None;")
        self.frame_60.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_60.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_40.addWidget(self.frame_60, 2, 0, 1, 4)

        self.hr_create_feedback_btn = QPushButton(self.frame_86)
        self.hr_create_feedback_btn.setObjectName(u"hr_create_feedback_btn")
        self.hr_create_feedback_btn.setMinimumSize(QSize(101, 51))
        self.hr_create_feedback_btn.setMaximumSize(QSize(16777215, 16777215))
        self.hr_create_feedback_btn.setStyleSheet(u"background-color: rgb(204, 204, 204);")

        self.gridLayout_40.addWidget(self.hr_create_feedback_btn, 2, 4, 1, 1)

        self.hr_logout_btn = QPushButton(self.frame_86)
        self.hr_logout_btn.setObjectName(u"hr_logout_btn")
        self.hr_logout_btn.setMinimumSize(QSize(101, 51))
        self.hr_logout_btn.setMaximumSize(QSize(16777215, 16777215))
        self.hr_logout_btn.setStyleSheet(u"background-color: rgb(204, 204, 204);")

        self.gridLayout_40.addWidget(self.hr_logout_btn, 2, 5, 1, 1)


        self.gridLayout_58.addWidget(self.frame_86, 0, 2, 5, 1)

        self.hr_employee_btn = QPushButton(self.hr_home_page)
        self.hr_employee_btn.setObjectName(u"hr_employee_btn")
        self.hr_employee_btn.setMinimumSize(QSize(71, 71))
        self.hr_employee_btn.setMaximumSize(QSize(71, 71))

        self.gridLayout_58.addWidget(self.hr_employee_btn, 2, 0, 1, 1)

        self.line_50 = QFrame(self.hr_home_page)
        self.line_50.setObjectName(u"line_50")
        self.line_50.setFrameShape(QFrame.Shape.HLine)
        self.line_50.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_58.addWidget(self.line_50, 3, 0, 1, 1)

        self.hr_home_btn = QPushButton(self.hr_home_page)
        self.hr_home_btn.setObjectName(u"hr_home_btn")
        self.hr_home_btn.setMinimumSize(QSize(71, 71))
        self.hr_home_btn.setMaximumSize(QSize(71, 71))

        self.gridLayout_58.addWidget(self.hr_home_btn, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.hr_home_page)
        self.hr_employee_page = QWidget()
        self.hr_employee_page.setObjectName(u"hr_employee_page")
        self.gridLayout_69 = QGridLayout(self.hr_employee_page)
        self.gridLayout_69.setObjectName(u"gridLayout_69")
        self.hr_employee_employee_btn = QPushButton(self.hr_employee_page)
        self.hr_employee_employee_btn.setObjectName(u"hr_employee_employee_btn")
        self.hr_employee_employee_btn.setMinimumSize(QSize(71, 71))
        self.hr_employee_employee_btn.setMaximumSize(QSize(71, 71))

        self.gridLayout_69.addWidget(self.hr_employee_employee_btn, 2, 0, 1, 1)

        self.hr_employee_home_btn = QPushButton(self.hr_employee_page)
        self.hr_employee_home_btn.setObjectName(u"hr_employee_home_btn")
        self.hr_employee_home_btn.setMinimumSize(QSize(71, 71))
        self.hr_employee_home_btn.setMaximumSize(QSize(71, 71))

        self.gridLayout_69.addWidget(self.hr_employee_home_btn, 0, 0, 1, 1)

        self.frame_95 = QFrame(self.hr_employee_page)
        self.frame_95.setObjectName(u"frame_95")
        self.frame_95.setStyleSheet(u"background-color: transparent;\n"
"border: none;")
        self.frame_95.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_95.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_69.addWidget(self.frame_95, 4, 0, 1, 1)

        self.frame_87 = QFrame(self.hr_employee_page)
        self.frame_87.setObjectName(u"frame_87")
        self.frame_87.setMinimumSize(QSize(1148, 684))
        self.frame_87.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_87.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_66 = QGridLayout(self.frame_87)
        self.gridLayout_66.setObjectName(u"gridLayout_66")
        self.groupBox_35 = QGroupBox(self.frame_87)
        self.groupBox_35.setObjectName(u"groupBox_35")
        self.groupBox_35.setMinimumSize(QSize(631, 311))
        self.gridLayout_67 = QGridLayout(self.groupBox_35)
        self.gridLayout_67.setObjectName(u"gridLayout_67")
        self.tableWidget_11 = QTableWidget(self.groupBox_35)
        if (self.tableWidget_11.columnCount() < 3):
            self.tableWidget_11.setColumnCount(3)
        __qtablewidgetitem53 = QTableWidgetItem()
        self.tableWidget_11.setHorizontalHeaderItem(0, __qtablewidgetitem53)
        __qtablewidgetitem54 = QTableWidgetItem()
        self.tableWidget_11.setHorizontalHeaderItem(1, __qtablewidgetitem54)
        __qtablewidgetitem55 = QTableWidgetItem()
        self.tableWidget_11.setHorizontalHeaderItem(2, __qtablewidgetitem55)
        self.tableWidget_11.setObjectName(u"tableWidget_11")
        self.tableWidget_11.horizontalHeader().setDefaultSectionSize(180)
        self.tableWidget_11.horizontalHeader().setStretchLastSection(True)

        self.gridLayout_67.addWidget(self.tableWidget_11, 0, 0, 1, 1)


        self.gridLayout_66.addWidget(self.groupBox_35, 0, 0, 1, 2)

        self.frame_62 = QFrame(self.frame_87)
        self.frame_62.setObjectName(u"frame_62")
        self.frame_62.setMinimumSize(QSize(950, 0))
        self.frame_62.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_62.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_66.addWidget(self.frame_62, 1, 0, 1, 1)

        self.hr_employee_view_btn = QPushButton(self.frame_87)
        self.hr_employee_view_btn.setObjectName(u"hr_employee_view_btn")
        self.hr_employee_view_btn.setMinimumSize(QSize(101, 51))
        self.hr_employee_view_btn.setMaximumSize(QSize(16777215, 16777215))
        self.hr_employee_view_btn.setStyleSheet(u"background-color: rgb(204, 204, 204);")

        self.gridLayout_66.addWidget(self.hr_employee_view_btn, 1, 1, 1, 1)


        self.gridLayout_69.addWidget(self.frame_87, 0, 2, 5, 1)

        self.line_54 = QFrame(self.hr_employee_page)
        self.line_54.setObjectName(u"line_54")
        self.line_54.setFrameShape(QFrame.Shape.HLine)
        self.line_54.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_69.addWidget(self.line_54, 1, 0, 1, 1)

        self.line_55 = QFrame(self.hr_employee_page)
        self.line_55.setObjectName(u"line_55")
        self.line_55.setFrameShape(QFrame.Shape.HLine)
        self.line_55.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_69.addWidget(self.line_55, 3, 0, 1, 1)

        self.line_53 = QFrame(self.hr_employee_page)
        self.line_53.setObjectName(u"line_53")
        self.line_53.setStyleSheet(u"border: 0px;\n"
"")
        self.line_53.setFrameShape(QFrame.Shape.VLine)
        self.line_53.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_69.addWidget(self.line_53, 0, 1, 5, 1)

        self.stackedWidget.addWidget(self.hr_employee_page)

        self.gridLayout.addWidget(self.stackedWidget, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter you number", None))
        self.lineEdit_2.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter your passowrd", None))
        self.pushButton.setText("")
        self.login_btn.setText(QCoreApplication.translate("MainWindow", u"Login", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Image", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"I.D Number", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Password", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Enter Credentials", None))
        self.lineEdit_3.setText("")
        self.lineEdit_3.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter you password", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Password", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Please change your password!", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Note: You have an option to skip for now, but this notification will comeback later after you log in again.", None))
        self.change_pass_btn.setText(QCoreApplication.translate("MainWindow", u"Change", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Image", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Biometric Image", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"Profile Picture", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"Name  / Position", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"Shift", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"1/2", None))
        self.label_14.setText("")
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"Place your finger on the fingerprint sensor to confirm your identity.", None))
        self.label_15.setText("")
        self.veri1_cancel_btn.setText(QCoreApplication.translate("MainWindow", u"Cancel", None))
        self.label_21.setText(QCoreApplication.translate("MainWindow", u"Webcam Live Picture", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"1/2", None))
        self.label_19.setText("")
        self.label_26.setText(QCoreApplication.translate("MainWindow", u"Ensure your face is fully visible in the frame.", None))
        self.label_25.setText("")
        self.veri2_cancel_btn.setText(QCoreApplication.translate("MainWindow", u"Cancel", None))
        self.label_40.setText(QCoreApplication.translate("MainWindow", u"Image", None))
        self.label_38.setText(QCoreApplication.translate("MainWindow", u"Goodbye!", None))
        self.label_39.setText(QCoreApplication.translate("MainWindow", u"You work 2 hours extra from your schedule hours!", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"Your Attedance Logs :", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Date:", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Time", None));
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Remarks:", None));
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Profile Picture", None))
        self.label_30.setText(QCoreApplication.translate("MainWindow", u"Image", None))
        self.pushButton_7.setText(QCoreApplication.translate("MainWindow", u"Add", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Employee Log-In Credentials", None))
        self.label_22.setText(QCoreApplication.translate("MainWindow", u"I.D Number", None))
        self.lineEdit_4.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter the I.D number.", None))
        self.label_23.setText(QCoreApplication.translate("MainWindow", u"Password", None))
        self.lineEdit_5.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter the password.", None))
        self.label_24.setText(QCoreApplication.translate("MainWindow", u"Shift Schdule:", None))
        self.radioButton.setText(QCoreApplication.translate("MainWindow", u"Shift 3", None))
        self.radioButton_2.setText(QCoreApplication.translate("MainWindow", u"Shift 2", None))
        self.radioButton_3.setText(QCoreApplication.translate("MainWindow", u"Shift 1", None))
        self.enroll_employee_btn.setText(QCoreApplication.translate("MainWindow", u"Enroll Biometrics", None))
        self.add_employee_btn.setText(QCoreApplication.translate("MainWindow", u"Add", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Employee Log-In Credentials", None))
        self.label_28.setText(QCoreApplication.translate("MainWindow", u"Full Name", None))
        self.lineEdit_6.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter the employee full name.", None))
        self.label_27.setText(QCoreApplication.translate("MainWindow", u"Department", None))
        self.lineEdit_7.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter department.", None))
        self.label_29.setText(QCoreApplication.translate("MainWindow", u"Position", None))
        self.lineEdit_8.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter the position.", None))
        self.enroll_employee_btn_2.setText(QCoreApplication.translate("MainWindow", u"Cancel", None))
        self.groupBox_10.setTitle(QCoreApplication.translate("MainWindow", u"Edit Profile Picture", None))
        self.label_51.setText(QCoreApplication.translate("MainWindow", u"Image", None))
        self.edit_pfp_btn.setText(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.groupBox_11.setTitle(QCoreApplication.translate("MainWindow", u"Edit Employee Log-In Credentials", None))
        self.label_52.setText(QCoreApplication.translate("MainWindow", u"I.D Number", None))
        self.lineEdit_9.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter you number", None))
        self.label_53.setText(QCoreApplication.translate("MainWindow", u"Password", None))
        self.lineEdit_10.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter you number", None))
        self.label_54.setText(QCoreApplication.translate("MainWindow", u"Shift Schdule:", None))
        self.radioButton_13.setText(QCoreApplication.translate("MainWindow", u"Shift 3", None))
        self.radioButton_14.setText(QCoreApplication.translate("MainWindow", u"Shift 2", None))
        self.radioButton_15.setText(QCoreApplication.translate("MainWindow", u"Shift 1", None))
        self.groupBox_12.setTitle(QCoreApplication.translate("MainWindow", u"Edit Employee Details", None))
        self.label_55.setText(QCoreApplication.translate("MainWindow", u"Full Name", None))
        self.lineEdit_11.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter the name", None))
        self.label_56.setText(QCoreApplication.translate("MainWindow", u"Department", None))
        self.lineEdit_12.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter the department", None))
        self.label_57.setText(QCoreApplication.translate("MainWindow", u"Position", None))
        self.lineEdit_13.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter the position", None))
        self.archive_employee_btn.setText(QCoreApplication.translate("MainWindow", u"Deactivate", None))
        self.save_employee_btn.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.edit_employee_back_btn.setText(QCoreApplication.translate("MainWindow", u"Back", None))
        self.label_35.setText(QCoreApplication.translate("MainWindow", u"Live Face Image", None))
        self.label_37.setText(QCoreApplication.translate("MainWindow", u"3.. 2.. 1..", None))
        self.label_36.setText(QCoreApplication.translate("MainWindow", u"Face Enrollment", None))
        self.label_34.setText(QCoreApplication.translate("MainWindow", u"Note: Ensure your face is fully visible in the frame.", None))
        self.face_cancel_btn.setText(QCoreApplication.translate("MainWindow", u"Cancel", None))
        self.groupBox_13.setTitle(QCoreApplication.translate("MainWindow", u"Prioritation:", None))
        self.radioButton_7.setText(QCoreApplication.translate("MainWindow", u"Critical", None))
        self.radioButton_8.setText(QCoreApplication.translate("MainWindow", u"Medium", None))
        self.radioButton_9.setText(QCoreApplication.translate("MainWindow", u"Low", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("MainWindow", u"Employe List:", None))
        ___qtablewidgetitem3 = self.tableWidget_2.horizontalHeaderItem(0)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Name:", None));
        ___qtablewidgetitem4 = self.tableWidget_2.horizontalHeaderItem(1)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"Department / Position:", None));
        ___qtablewidgetitem5 = self.tableWidget_2.horizontalHeaderItem(2)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"Schedule", None));
        self.groupBox_6.setTitle(QCoreApplication.translate("MainWindow", u"Problem or Concerns:", None))
        self.label_81.setText(QCoreApplication.translate("MainWindow", u"Note: Please select involve employee on the table if none ignore.", None))
        self.send_feedback_btn.setText(QCoreApplication.translate("MainWindow", u"Send Feedback", None))
        self.cancel_feedback_btn.setText(QCoreApplication.translate("MainWindow", u"Cancel", None))
        self.employee_settings_btn.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.employee_employee_btn.setText(QCoreApplication.translate("MainWindow", u"Employees/\n"
"HR", None))
        self.employee_home_btn.setText(QCoreApplication.translate("MainWindow", u"Home", None))
        self.groupBox_7.setTitle(QCoreApplication.translate("MainWindow", u"HR NOTICE:", None))
        self.label_41.setText(QCoreApplication.translate("MainWindow", u"Concern:", None))
        self.label_80.setText(QCoreApplication.translate("MainWindow", u"Note: Select the arrow button to navigate notice.", None))
        self.employee_edit_btn.setText(QCoreApplication.translate("MainWindow", u"EDIT", None))
        self.employee_add_btn.setText(QCoreApplication.translate("MainWindow", u"ADD", None))
        self.employee_view_btn.setText(QCoreApplication.translate("MainWindow", u"VIEW", None))
        self.groupBox_20.setTitle(QCoreApplication.translate("MainWindow", u"Employee List:", None))
        ___qtablewidgetitem6 = self.tableWidget_7.horizontalHeaderItem(0)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"Name:", None));
        ___qtablewidgetitem7 = self.tableWidget_7.horizontalHeaderItem(1)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("MainWindow", u"Department / Position:", None));
        ___qtablewidgetitem8 = self.tableWidget_7.horizontalHeaderItem(2)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("MainWindow", u"Schedule:", None));
        self.label_66.setText(QCoreApplication.translate("MainWindow", u"Note: Select employee then pressed the buttons on the left side to edit, view.", None))
        self.manage_hr_btn.setText(QCoreApplication.translate("MainWindow", u"Manage HR Accounts", None))
        self.groupBox_31.setTitle(QCoreApplication.translate("MainWindow", u"HR Access Logs", None))
        ___qtablewidgetitem9 = self.tableWidget_12.horizontalHeaderItem(0)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("MainWindow", u"Names:", None));
        ___qtablewidgetitem10 = self.tableWidget_12.horizontalHeaderItem(1)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("MainWindow", u"Date:", None));
        ___qtablewidgetitem11 = self.tableWidget_12.horizontalHeaderItem(2)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("MainWindow", u"Time:", None));
        self.groupBox_32.setTitle(QCoreApplication.translate("MainWindow", u"Account Pane:", None))
        self.label_74.setText(QCoreApplication.translate("MainWindow", u"I.D Number", None))
        self.lineEdit_19.setText("")
        self.lineEdit_19.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter the name", None))
        self.label_68.setText(QCoreApplication.translate("MainWindow", u"I.D Number", None))
        self.lineEdit_15.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter the number", None))
        self.label_69.setText(QCoreApplication.translate("MainWindow", u"Password", None))
        self.lineEdit_14.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter the password", None))
        self.label_70.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Note: This pane is fpr adding accounts and when select accounts <br/>for edit the box will fill up of information.</p></body></html>", None))
        self.manage_hr_add_btn.setText(QCoreApplication.translate("MainWindow", u"ADD", None))
        self.groupBox_30.setTitle(QCoreApplication.translate("MainWindow", u"HR Accounts List:", None))
        ___qtablewidgetitem12 = self.tableWidget_10.horizontalHeaderItem(0)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("MainWindow", u"Name:", None));
        ___qtablewidgetitem13 = self.tableWidget_10.horizontalHeaderItem(1)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("MainWindow", u"Status:", None));
        ___qtablewidgetitem14 = self.tableWidget_10.horizontalHeaderItem(2)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("MainWindow", u"Logs:", None));
        self.label_67.setText(QCoreApplication.translate("MainWindow", u"Note: Select employee then pressed the buttons on the left side to edit and deactivate account.", None))
        self.manage_edit_btn.setText(QCoreApplication.translate("MainWindow", u"EDIT", None))
        self.manage_deactivate_btn.setText(QCoreApplication.translate("MainWindow", u"DEACTIVATE", None))
        self.manager_hr_back_btn.setText(QCoreApplication.translate("MainWindow", u"Back", None))
        self.label_33.setText(QCoreApplication.translate("MainWindow", u"Note: Place your finger on the fingerprint sensor to confirm your identity.", None))
        self.label_31.setText(QCoreApplication.translate("MainWindow", u"Biometrics", None))
        self.bio_cancel_btn.setText(QCoreApplication.translate("MainWindow", u"Cancel", None))
        self.label_32.setText(QCoreApplication.translate("MainWindow", u"Fingerprint Enrollment", None))
        self.settings_home_btn.setText(QCoreApplication.translate("MainWindow", u"Home", None))
        self.groupBox_14.setTitle(QCoreApplication.translate("MainWindow", u"Backup Logs", None))
        ___qtablewidgetitem15 = self.tableWidget_5.horizontalHeaderItem(0)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("MainWindow", u"Name", None));
        ___qtablewidgetitem16 = self.tableWidget_5.horizontalHeaderItem(1)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("MainWindow", u"Date:", None));
        self.label_77.setText(QCoreApplication.translate("MainWindow", u"Note: This is the listed backup logs.", None))
        self.groupBox_17.setTitle(QCoreApplication.translate("MainWindow", u"Restore Configuration:", None))
        self.label_87.setText(QCoreApplication.translate("MainWindow", u"To:", None))
        self.label_86.setText(QCoreApplication.translate("MainWindow", u"From:", None))
        self.restore_btn.setText(QCoreApplication.translate("MainWindow", u"Restore", None))
        self.groupBox_15.setTitle(QCoreApplication.translate("MainWindow", u"Database  Saving Logs", None))
        ___qtablewidgetitem17 = self.tableWidget_6.horizontalHeaderItem(0)
        ___qtablewidgetitem17.setText(QCoreApplication.translate("MainWindow", u"Date:", None));
        self.label_78.setText(QCoreApplication.translate("MainWindow", u"Note: This is logs every time data savs files from the database.", None))
        self.groupBox_18.setTitle(QCoreApplication.translate("MainWindow", u"Retention Configuration:", None))
        self.label_88.setText(QCoreApplication.translate("MainWindow", u"Archive Below:", None))
        self.archive_btn.setText(QCoreApplication.translate("MainWindow", u"Archive", None))
        self.groupBox_16.setTitle(QCoreApplication.translate("MainWindow", u"Backup Configuration:", None))
        self.label_85.setText(QCoreApplication.translate("MainWindow", u"Manual Backup:", None))
        self.lineEdit_17.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter the backup name.", None))
        self.label_84.setText(QCoreApplication.translate("MainWindow", u"From:", None))
        self.label_83.setText(QCoreApplication.translate("MainWindow", u"To:", None))
        self.manual_backup_btn.setText(QCoreApplication.translate("MainWindow", u"Backup", None))
        self.label_82.setText(QCoreApplication.translate("MainWindow", u"Automatic:", None))
        self.radioButton_10.setText(QCoreApplication.translate("MainWindow", u"1 year", None))
        self.radioButton_11.setText(QCoreApplication.translate("MainWindow", u"6 months", None))
        self.radioButton_12.setText(QCoreApplication.translate("MainWindow", u"3 months", None))
        self.automatic_backup_btn.setText(QCoreApplication.translate("MainWindow", u"Backup", None))
        self.label_76.setText(QCoreApplication.translate("MainWindow", u"Note: You have to two configuration backup & automatick backup.", None))
        self.settings_employee_btn.setText(QCoreApplication.translate("MainWindow", u"Employees", None))
        self.settings_settings_btn.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.groupBox_8.setTitle(QCoreApplication.translate("MainWindow", u"Employee:", None))
        self.label_46.setText(QCoreApplication.translate("MainWindow", u"Image", None))
        self.label_44.setText(QCoreApplication.translate("MainWindow", u"Name:", None))
        self.label_48.setText(QCoreApplication.translate("MainWindow", u"Text", None))
        self.label_43.setText(QCoreApplication.translate("MainWindow", u"Department:", None))
        self.label_49.setText(QCoreApplication.translate("MainWindow", u"Text", None))
        self.label_47.setText(QCoreApplication.translate("MainWindow", u"Position:", None))
        self.label_50.setText(QCoreApplication.translate("MainWindow", u"Text", None))
        self.label_45.setText(QCoreApplication.translate("MainWindow", u"Shift Schdule:", None))
        self.radioButton_4.setText(QCoreApplication.translate("MainWindow", u"Shift 3", None))
        self.radioButton_5.setText(QCoreApplication.translate("MainWindow", u"Shift 2", None))
        self.radioButton_6.setText(QCoreApplication.translate("MainWindow", u"Shift 1", None))
        self.groupBox_9.setTitle(QCoreApplication.translate("MainWindow", u"Attendace Logs:", None))
        ___qtablewidgetitem18 = self.tableWidget_3.horizontalHeaderItem(0)
        ___qtablewidgetitem18.setText(QCoreApplication.translate("MainWindow", u"Date:", None));
        ___qtablewidgetitem19 = self.tableWidget_3.horizontalHeaderItem(1)
        ___qtablewidgetitem19.setText(QCoreApplication.translate("MainWindow", u"Time:", None));
        ___qtablewidgetitem20 = self.tableWidget_3.horizontalHeaderItem(2)
        ___qtablewidgetitem20.setText(QCoreApplication.translate("MainWindow", u"Attempts No:", None));
        ___qtablewidgetitem21 = self.tableWidget_3.horizontalHeaderItem(3)
        ___qtablewidgetitem21.setText(QCoreApplication.translate("MainWindow", u"Remarks:", None));
        self.view_employee_back_btn.setText(QCoreApplication.translate("MainWindow", u"Back", None))
        self.home_home_btn.setText(QCoreApplication.translate("MainWindow", u"Home", None))
        self.groupBox_19.setTitle(QCoreApplication.translate("MainWindow", u"Total Number of Employees", None))
        self.label_58.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.groupBox_22.setTitle(QCoreApplication.translate("MainWindow", u"Logged Today:", None))
        self.label_59.setText(QCoreApplication.translate("MainWindow", u"0/10", None))
        self.groupBox_23.setTitle(QCoreApplication.translate("MainWindow", u"Late:", None))
        self.label_60.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.groupBox_24.setTitle(QCoreApplication.translate("MainWindow", u"Absents:", None))
        self.label_61.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.groupBox_21.setTitle(QCoreApplication.translate("MainWindow", u"Reatime System Logs:", None))
        ___qtablewidgetitem22 = self.tableWidget_4.horizontalHeaderItem(0)
        ___qtablewidgetitem22.setText(QCoreApplication.translate("MainWindow", u"Date / Time:", None));
        ___qtablewidgetitem23 = self.tableWidget_4.horizontalHeaderItem(1)
        ___qtablewidgetitem23.setText(QCoreApplication.translate("MainWindow", u"Name:", None));
        ___qtablewidgetitem24 = self.tableWidget_4.horizontalHeaderItem(2)
        ___qtablewidgetitem24.setText(QCoreApplication.translate("MainWindow", u"Department / Position:", None));
        ___qtablewidgetitem25 = self.tableWidget_4.horizontalHeaderItem(3)
        ___qtablewidgetitem25.setText(QCoreApplication.translate("MainWindow", u"Remarks:", None));
        ___qtablewidgetitem26 = self.tableWidget_4.verticalHeaderItem(0)
        ___qtablewidgetitem26.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem27 = self.tableWidget_4.verticalHeaderItem(1)
        ___qtablewidgetitem27.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem28 = self.tableWidget_4.verticalHeaderItem(2)
        ___qtablewidgetitem28.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem29 = self.tableWidget_4.verticalHeaderItem(3)
        ___qtablewidgetitem29.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem30 = self.tableWidget_4.verticalHeaderItem(4)
        ___qtablewidgetitem30.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem31 = self.tableWidget_4.verticalHeaderItem(5)
        ___qtablewidgetitem31.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem32 = self.tableWidget_4.verticalHeaderItem(6)
        ___qtablewidgetitem32.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem33 = self.tableWidget_4.verticalHeaderItem(7)
        ___qtablewidgetitem33.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem34 = self.tableWidget_4.verticalHeaderItem(8)
        ___qtablewidgetitem34.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem35 = self.tableWidget_4.verticalHeaderItem(9)
        ___qtablewidgetitem35.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem36 = self.tableWidget_4.verticalHeaderItem(10)
        ___qtablewidgetitem36.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem37 = self.tableWidget_4.verticalHeaderItem(11)
        ___qtablewidgetitem37.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem38 = self.tableWidget_4.verticalHeaderItem(12)
        ___qtablewidgetitem38.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem39 = self.tableWidget_4.verticalHeaderItem(13)
        ___qtablewidgetitem39.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem40 = self.tableWidget_4.verticalHeaderItem(14)
        ___qtablewidgetitem40.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem41 = self.tableWidget_4.verticalHeaderItem(15)
        ___qtablewidgetitem41.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem42 = self.tableWidget_4.verticalHeaderItem(16)
        ___qtablewidgetitem42.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem43 = self.tableWidget_4.verticalHeaderItem(17)
        ___qtablewidgetitem43.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem44 = self.tableWidget_4.verticalHeaderItem(18)
        ___qtablewidgetitem44.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem45 = self.tableWidget_4.verticalHeaderItem(19)
        ___qtablewidgetitem45.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem46 = self.tableWidget_4.verticalHeaderItem(20)
        ___qtablewidgetitem46.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem47 = self.tableWidget_4.verticalHeaderItem(21)
        ___qtablewidgetitem47.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem48 = self.tableWidget_4.verticalHeaderItem(22)
        ___qtablewidgetitem48.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        self.label_79.setText(QCoreApplication.translate("MainWindow", u"Note: This is the realtime authentication logs", None))
        self.home_logout_btn.setText(QCoreApplication.translate("MainWindow", u"Log Out", None))
        self.home_employee_btn.setText(QCoreApplication.translate("MainWindow", u"Employees", None))
        self.home_settings_btn.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.groupBox_25.setTitle(QCoreApplication.translate("MainWindow", u"Employee No:", None))
        self.label_62.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.groupBox_26.setTitle(QCoreApplication.translate("MainWindow", u"Logged Today:", None))
        self.label_63.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.groupBox_27.setTitle(QCoreApplication.translate("MainWindow", u"Late:", None))
        self.label_64.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.groupBox_28.setTitle(QCoreApplication.translate("MainWindow", u"Absents", None))
        self.label_65.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.groupBox_29.setTitle(QCoreApplication.translate("MainWindow", u"Reatime System Logs:", None))
        ___qtablewidgetitem49 = self.tableWidget_9.horizontalHeaderItem(0)
        ___qtablewidgetitem49.setText(QCoreApplication.translate("MainWindow", u"Date / Time:", None));
        ___qtablewidgetitem50 = self.tableWidget_9.horizontalHeaderItem(1)
        ___qtablewidgetitem50.setText(QCoreApplication.translate("MainWindow", u"Name:", None));
        ___qtablewidgetitem51 = self.tableWidget_9.horizontalHeaderItem(2)
        ___qtablewidgetitem51.setText(QCoreApplication.translate("MainWindow", u"Department / Position:", None));
        ___qtablewidgetitem52 = self.tableWidget_9.horizontalHeaderItem(3)
        ___qtablewidgetitem52.setText(QCoreApplication.translate("MainWindow", u"Remarks:", None));
        self.hr_create_feedback_btn.setText(QCoreApplication.translate("MainWindow", u"Send Feedback", None))
        self.hr_logout_btn.setText(QCoreApplication.translate("MainWindow", u"Log Out", None))
        self.hr_employee_btn.setText(QCoreApplication.translate("MainWindow", u"Employees", None))
        self.hr_home_btn.setText(QCoreApplication.translate("MainWindow", u"Home", None))
        self.hr_employee_employee_btn.setText(QCoreApplication.translate("MainWindow", u"Employees", None))
        self.hr_employee_home_btn.setText(QCoreApplication.translate("MainWindow", u"Home", None))
        self.groupBox_35.setTitle(QCoreApplication.translate("MainWindow", u"Employee List:", None))
        ___qtablewidgetitem53 = self.tableWidget_11.horizontalHeaderItem(0)
        ___qtablewidgetitem53.setText(QCoreApplication.translate("MainWindow", u"Name:", None));
        ___qtablewidgetitem54 = self.tableWidget_11.horizontalHeaderItem(1)
        ___qtablewidgetitem54.setText(QCoreApplication.translate("MainWindow", u"Department / Position:", None));
        ___qtablewidgetitem55 = self.tableWidget_11.horizontalHeaderItem(2)
        ___qtablewidgetitem55.setText(QCoreApplication.translate("MainWindow", u"Schedule:", None));
        self.hr_employee_view_btn.setText(QCoreApplication.translate("MainWindow", u"VIEW", None))
    # retranslateUi

