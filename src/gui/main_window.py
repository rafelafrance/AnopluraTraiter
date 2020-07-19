# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
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


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1230, 697)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(10, 0, 1211, 641))
        self.tabWidget.setAcceptDrops(True)
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.horizontalLayoutWidget_2 = QWidget(self.tab)
        self.horizontalLayoutWidget_2.setObjectName(u"horizontalLayoutWidget_2")
        self.horizontalLayoutWidget_2.setGeometry(QRect(930, 20, 267, 31))
        self.horizontalLayout_4 = QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.db_backup_btn = QPushButton(self.horizontalLayoutWidget_2)
        self.db_backup_btn.setObjectName(u"db_backup_btn")

        self.horizontalLayout_4.addWidget(self.db_backup_btn)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_4)

        self.db_rebuild_btn = QPushButton(self.horizontalLayoutWidget_2)
        self.db_rebuild_btn.setObjectName(u"db_rebuild_btn")

        self.horizontalLayout_4.addWidget(self.db_rebuild_btn)

        self.label = QLabel(self.tab)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 70, 171, 17))
        self.docs_tbl = QTableView(self.tab)
        self.docs_tbl.setObjectName(u"docs_tbl")
        self.docs_tbl.setGeometry(QRect(10, 90, 1191, 421))
        self.docs_tbl.setSortingEnabled(True)
        self.horizontalLayoutWidget = QWidget(self.tab)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(10, 20, 321, 31))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.pdf_to_text_btn = QPushButton(self.horizontalLayoutWidget)
        self.pdf_to_text_btn.setObjectName(u"pdf_to_text_btn")

        self.horizontalLayout.addWidget(self.pdf_to_text_btn)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_5)

        self.import_text_btn = QPushButton(self.horizontalLayoutWidget)
        self.import_text_btn.setObjectName(u"import_text_btn")

        self.horizontalLayout.addWidget(self.import_text_btn)

        self.horizontalSpacer = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.ocr_pdf_btn = QPushButton(self.horizontalLayoutWidget)
        self.ocr_pdf_btn.setObjectName(u"ocr_pdf_btn")
        self.ocr_pdf_btn.setEnabled(False)

        self.horizontalLayout.addWidget(self.ocr_pdf_btn)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.doc_edit_text = QTextEdit(self.tab_2)
        self.doc_edit_text.setObjectName(u"doc_edit_text")
        self.doc_edit_text.setGeometry(QRect(10, 80, 1191, 431))
        self.doc_edit_text.setLineWrapMode(QTextEdit.NoWrap)
        self.horizontalLayoutWidget_3 = QWidget(self.tab_2)
        self.horizontalLayoutWidget_3.setObjectName(u"horizontalLayoutWidget_3")
        self.horizontalLayoutWidget_3.setGeometry(QRect(870, 570, 331, 31))
        self.horizontalLayout_2 = QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.doc_edits_save_btn = QPushButton(self.horizontalLayoutWidget_3)
        self.doc_edits_save_btn.setObjectName(u"doc_edits_save_btn")
        self.doc_edits_save_btn.setEnabled(False)

        self.horizontalLayout_2.addWidget(self.doc_edits_save_btn)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.doc_edits_cancel_btn = QPushButton(self.horizontalLayoutWidget_3)
        self.doc_edits_cancel_btn.setObjectName(u"doc_edits_cancel_btn")
        self.doc_edits_cancel_btn.setEnabled(False)

        self.horizontalLayout_2.addWidget(self.doc_edits_cancel_btn)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)

        self.doc_edits_reset_btn = QPushButton(self.horizontalLayoutWidget_3)
        self.doc_edits_reset_btn.setObjectName(u"doc_edits_reset_btn")
        self.doc_edits_reset_btn.setEnabled(False)

        self.horizontalLayout_2.addWidget(self.doc_edits_reset_btn)

        self.edit_doc_cbox = QComboBox(self.tab_2)
        self.edit_doc_cbox.setObjectName(u"edit_doc_cbox")
        self.edit_doc_cbox.setGeometry(QRect(20, 30, 421, 25))
        self.label_4 = QLabel(self.tab_2)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(20, 10, 121, 17))
        self.run_pipe_btn = QPushButton(self.tab_2)
        self.run_pipe_btn.setObjectName(u"run_pipe_btn")
        self.run_pipe_btn.setEnabled(False)
        self.run_pipe_btn.setGeometry(QRect(600, 540, 81, 25))
        self.select_pipe_cbox = QComboBox(self.tab_2)
        self.select_pipe_cbox.setObjectName(u"select_pipe_cbox")
        self.select_pipe_cbox.setGeometry(QRect(20, 540, 541, 25))
        self.select_pipe_cbox.setEditable(True)
        self.select_pipe_cbox.setMaxVisibleItems(20)
        self.select_pipe_cbox.setSizeAdjustPolicy(QComboBox.AdjustToMinimumContentsLength)
        self.edit_pipes_btn = QPushButton(self.tab_2)
        self.edit_pipes_btn.setObjectName(u"edit_pipes_btn")
        self.edit_pipes_btn.setEnabled(False)
        self.edit_pipes_btn.setGeometry(QRect(710, 540, 81, 25))
        self.label_2 = QLabel(self.tab_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(20, 520, 41, 17))
        self.add_pipe_btn = QPushButton(self.tab_2)
        self.add_pipe_btn.setObjectName(u"add_pipe_btn")
        self.add_pipe_btn.setGeometry(QRect(560, 540, 21, 25))
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.tabWidget.addTab(self.tab_4, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1230, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
#if QT_CONFIG(shortcut)
        self.label.setBuddy(self.docs_tbl)
#endif // QT_CONFIG(shortcut)
        QWidget.setTabOrder(self.tabWidget, self.pdf_to_text_btn)
        QWidget.setTabOrder(self.pdf_to_text_btn, self.import_text_btn)
        QWidget.setTabOrder(self.import_text_btn, self.ocr_pdf_btn)
        QWidget.setTabOrder(self.ocr_pdf_btn, self.docs_tbl)
        QWidget.setTabOrder(self.docs_tbl, self.db_backup_btn)
        QWidget.setTabOrder(self.db_backup_btn, self.db_rebuild_btn)
        QWidget.setTabOrder(self.db_rebuild_btn, self.edit_doc_cbox)
        QWidget.setTabOrder(self.edit_doc_cbox, self.doc_edit_text)
        QWidget.setTabOrder(self.doc_edit_text, self.select_pipe_cbox)
        QWidget.setTabOrder(self.select_pipe_cbox, self.add_pipe_btn)
        QWidget.setTabOrder(self.add_pipe_btn, self.run_pipe_btn)
        QWidget.setTabOrder(self.run_pipe_btn, self.edit_pipes_btn)
        QWidget.setTabOrder(self.edit_pipes_btn, self.doc_edits_save_btn)
        QWidget.setTabOrder(self.doc_edits_save_btn, self.doc_edits_cancel_btn)
        QWidget.setTabOrder(self.doc_edits_cancel_btn, self.doc_edits_reset_btn)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Traiter (Anoplura)", None))
#if QT_CONFIG(tooltip)
        MainWindow.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.tabWidget.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.db_backup_btn.setToolTip(QCoreApplication.translate("MainWindow", u"Create a copy of the database", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.db_backup_btn.setStatusTip(QCoreApplication.translate("MainWindow", u"Save a copy fo the database", None))
#endif // QT_CONFIG(statustip)
        self.db_backup_btn.setText(QCoreApplication.translate("MainWindow", u"Backup Database", None))
#if QT_CONFIG(tooltip)
        self.db_rebuild_btn.setToolTip(QCoreApplication.translate("MainWindow", u"Delete all data and rebuild the database", None))
#endif // QT_CONFIG(tooltip)
        self.db_rebuild_btn.setText(QCoreApplication.translate("MainWindow", u"Rebuild Database", None))
#if QT_CONFIG(shortcut)
        self.db_rebuild_btn.setShortcut(QCoreApplication.translate("MainWindow", u"Del", None))
#endif // QT_CONFIG(shortcut)
        self.label.setText(QCoreApplication.translate("MainWindow", u"Documents in Database", None))
#if QT_CONFIG(tooltip)
        self.pdf_to_text_btn.setToolTip(QCoreApplication.translate("MainWindow", u"Read text from a PDF file and import it into the database", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.pdf_to_text_btn.setStatusTip(QCoreApplication.translate("MainWindow", u"Convert a PDF file to text and import it into the database", None))
#endif // QT_CONFIG(statustip)
        self.pdf_to_text_btn.setText(QCoreApplication.translate("MainWindow", u"PDF to Text", None))
#if QT_CONFIG(tooltip)
        self.import_text_btn.setToolTip(QCoreApplication.translate("MainWindow", u"Import a text file into the database", None))
#endif // QT_CONFIG(tooltip)
        self.import_text_btn.setText(QCoreApplication.translate("MainWindow", u"Import Text", None))
#if QT_CONFIG(tooltip)
        self.ocr_pdf_btn.setToolTip(QCoreApplication.translate("MainWindow", u"OCR text in PDF images and import them into the database ", None))
#endif // QT_CONFIG(tooltip)
        self.ocr_pdf_btn.setText(QCoreApplication.translate("MainWindow", u"OCR PDF", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Import", None))
#if QT_CONFIG(tooltip)
        self.tabWidget.setTabToolTip(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Import files into the database", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.doc_edits_save_btn.setToolTip(QCoreApplication.translate("MainWindow", u"Save your edits", None))
#endif // QT_CONFIG(tooltip)
        self.doc_edits_save_btn.setText(QCoreApplication.translate("MainWindow", u"Save", None))
#if QT_CONFIG(tooltip)
        self.doc_edits_cancel_btn.setToolTip(QCoreApplication.translate("MainWindow", u"Undo all edits back to the last save", None))
#endif // QT_CONFIG(tooltip)
        self.doc_edits_cancel_btn.setText(QCoreApplication.translate("MainWindow", u"Cancel", None))
#if QT_CONFIG(tooltip)
        self.doc_edits_reset_btn.setToolTip(QCoreApplication.translate("MainWindow", u"Reset text all the way back to its imported state", None))
#endif // QT_CONFIG(tooltip)
        self.doc_edits_reset_btn.setText(QCoreApplication.translate("MainWindow", u"Reset Text", None))
#if QT_CONFIG(tooltip)
        self.edit_doc_cbox.setToolTip(QCoreApplication.translate("MainWindow", u"Choose a file to edit. The text will be shown below", None))
#endif // QT_CONFIG(tooltip)
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Document to Edit", None))
        self.run_pipe_btn.setText(QCoreApplication.translate("MainWindow", u"Run Pipe", None))
        self.edit_pipes_btn.setText(QCoreApplication.translate("MainWindow", u"Edit Pipes", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Pipe", None))
#if QT_CONFIG(tooltip)
        self.add_pipe_btn.setToolTip(QCoreApplication.translate("MainWindow", u"Add the current pipe to the list of pipes", None))
#endif // QT_CONFIG(tooltip)
        self.add_pipe_btn.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Edit", None))
#if QT_CONFIG(tooltip)
        self.tabWidget.setTabToolTip(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Edit files to prepare for further processing", None))
#endif // QT_CONFIG(tooltip)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"Recognize", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QCoreApplication.translate("MainWindow", u"Link", None))
    # retranslateUi

