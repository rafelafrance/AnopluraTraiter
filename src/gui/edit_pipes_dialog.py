# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'edit_pipes_dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *


class Ui_edit_pipes_dlg(object):
    def setupUi(self, edit_pipes_dlg):
        if not edit_pipes_dlg.objectName():
            edit_pipes_dlg.setObjectName(u"edit_pipes_dlg")
        edit_pipes_dlg.resize(923, 313)
        self.pipes_tbl = QTableView(edit_pipes_dlg)
        self.pipes_tbl.setObjectName(u"pipes_tbl")
        self.pipes_tbl.setGeometry(QRect(10, 10, 901, 221))

        self.retranslateUi(edit_pipes_dlg)

        QMetaObject.connectSlotsByName(edit_pipes_dlg)
    # setupUi

    def retranslateUi(self, edit_pipes_dlg):
        edit_pipes_dlg.setWindowTitle(QCoreApplication.translate("edit_pipes_dlg", u"Edit Pipes", None))
    # retranslateUi

