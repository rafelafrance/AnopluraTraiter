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
        MainWindow.resize(1238, 887)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(10, 0, 1211, 831))
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
        self.label.setGeometry(QRect(10, 80, 171, 17))
        self.docs_tbl = QTableView(self.tab)
        self.docs_tbl.setObjectName(u"docs_tbl")
        self.docs_tbl.setGeometry(QRect(10, 100, 1191, 691))
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
        self.horizontalLayoutWidget_3.setGeometry(QRect(870, 760, 331, 31))
        self.horizontalLayout_2 = QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.doc_edits_save_btn = QPushButton(self.horizontalLayoutWidget_3)
        self.doc_edits_save_btn.setObjectName(u"doc_edits_save_btn")

        self.horizontalLayout_2.addWidget(self.doc_edits_save_btn)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.doc_edits_cancel_btn = QPushButton(self.horizontalLayoutWidget_3)
        self.doc_edits_cancel_btn.setObjectName(u"doc_edits_cancel_btn")

        self.horizontalLayout_2.addWidget(self.doc_edits_cancel_btn)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)

        self.doc_edits_reset_btn = QPushButton(self.horizontalLayoutWidget_3)
        self.doc_edits_reset_btn.setObjectName(u"doc_edits_reset_btn")

        self.horizontalLayout_2.addWidget(self.doc_edits_reset_btn)

        self.horizontalLayoutWidget_4 = QWidget(self.tab_2)
        self.horizontalLayoutWidget_4.setObjectName(u"horizontalLayoutWidget_4")
        self.horizontalLayoutWidget_4.setGeometry(QRect(10, 640, 221, 31))
        self.horizontalLayout_3 = QHBoxLayout(self.horizontalLayoutWidget_4)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.doc_replace_btn = QPushButton(self.horizontalLayoutWidget_4)
        self.doc_replace_btn.setObjectName(u"doc_replace_btn")

        self.horizontalLayout_3.addWidget(self.doc_replace_btn)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_6)

        self.doc_replace_all_btn = QPushButton(self.horizontalLayoutWidget_4)
        self.doc_replace_all_btn.setObjectName(u"doc_replace_all_btn")

        self.horizontalLayout_3.addWidget(self.doc_replace_all_btn)

        self.horizontalLayoutWidget_5 = QWidget(self.tab_2)
        self.horizontalLayoutWidget_5.setObjectName(u"horizontalLayoutWidget_5")
        self.horizontalLayoutWidget_5.setGeometry(QRect(300, 600, 401, 31))
        self.horizontalLayout_5 = QHBoxLayout(self.horizontalLayoutWidget_5)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.doc_case_sensitive_chk = QCheckBox(self.horizontalLayoutWidget_5)
        self.doc_case_sensitive_chk.setObjectName(u"doc_case_sensitive_chk")

        self.horizontalLayout_5.addWidget(self.doc_case_sensitive_chk)

        self.doc_whole_words_chk = QCheckBox(self.horizontalLayoutWidget_5)
        self.doc_whole_words_chk.setObjectName(u"doc_whole_words_chk")

        self.horizontalLayout_5.addWidget(self.doc_whole_words_chk)

        self.doc_regex_chk = QCheckBox(self.horizontalLayoutWidget_5)
        self.doc_regex_chk.setObjectName(u"doc_regex_chk")

        self.horizontalLayout_5.addWidget(self.doc_regex_chk)

        self.horizontalLayoutWidget_6 = QWidget(self.tab_2)
        self.horizontalLayoutWidget_6.setObjectName(u"horizontalLayoutWidget_6")
        self.horizontalLayoutWidget_6.setGeometry(QRect(10, 600, 221, 31))
        self.horizontalLayout_6 = QHBoxLayout(self.horizontalLayoutWidget_6)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.doc_find_next_btn = QPushButton(self.horizontalLayoutWidget_6)
        self.doc_find_next_btn.setObjectName(u"doc_find_next_btn")

        self.horizontalLayout_6.addWidget(self.doc_find_next_btn)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_7)

        self.doc_find_previous_btn = QPushButton(self.horizontalLayoutWidget_6)
        self.doc_find_previous_btn.setObjectName(u"doc_find_previous_btn")

        self.horizontalLayout_6.addWidget(self.doc_find_previous_btn)

        self.formLayoutWidget = QWidget(self.tab_2)
        self.formLayoutWidget.setObjectName(u"formLayoutWidget")
        self.formLayoutWidget.setGeometry(QRect(10, 530, 691, 71))
        self.formLayout = QFormLayout(self.formLayoutWidget)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.formLayoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_2)

        self.label_3 = QLabel(self.formLayoutWidget)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_3)

        self.doc_find_cbx = QComboBox(self.formLayoutWidget)
        self.doc_find_cbx.setObjectName(u"doc_find_cbx")
        self.doc_find_cbx.setEditable(True)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.doc_find_cbx)

        self.doc_replace_cbx = QComboBox(self.formLayoutWidget)
        self.doc_replace_cbx.setObjectName(u"doc_replace_cbx")
        self.doc_replace_cbx.setEditable(True)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.doc_replace_cbx)

        self.edit_doc_cbox = QComboBox(self.tab_2)
        self.edit_doc_cbox.setObjectName(u"edit_doc_cbox")
        self.edit_doc_cbox.setGeometry(QRect(140, 30, 421, 25))
        self.label_4 = QLabel(self.tab_2)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(20, 30, 121, 17))
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
        self.menubar.setGeometry(QRect(0, 0, 1238, 22))
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

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Traiter (Anoplura)", None))
#if QT_CONFIG(tooltip)
        MainWindow.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.db_backup_btn.setText(QCoreApplication.translate("MainWindow", u"Backup Database", None))
        self.db_rebuild_btn.setText(QCoreApplication.translate("MainWindow", u"Rebuild Database", None))
#if QT_CONFIG(shortcut)
        self.db_rebuild_btn.setShortcut(QCoreApplication.translate("MainWindow", u"Del", None))
#endif // QT_CONFIG(shortcut)
        self.label.setText(QCoreApplication.translate("MainWindow", u"Documents in Database", None))
        self.pdf_to_text_btn.setText(QCoreApplication.translate("MainWindow", u"PDF to Text", None))
        self.import_text_btn.setText(QCoreApplication.translate("MainWindow", u"Import Text", None))
        self.ocr_pdf_btn.setText(QCoreApplication.translate("MainWindow", u"OCR PDF", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Import", None))
        self.doc_edits_save_btn.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.doc_edits_cancel_btn.setText(QCoreApplication.translate("MainWindow", u"Cancel", None))
        self.doc_edits_reset_btn.setText(QCoreApplication.translate("MainWindow", u"Reset Text", None))
        self.doc_replace_btn.setText(QCoreApplication.translate("MainWindow", u"Replace", None))
        self.doc_replace_all_btn.setText(QCoreApplication.translate("MainWindow", u"Replace All", None))
        self.doc_case_sensitive_chk.setText(QCoreApplication.translate("MainWindow", u"Case Sensitive", None))
        self.doc_whole_words_chk.setText(QCoreApplication.translate("MainWindow", u"Whole Words", None))
        self.doc_regex_chk.setText(QCoreApplication.translate("MainWindow", u"Regular Expression", None))
        self.doc_find_next_btn.setText(QCoreApplication.translate("MainWindow", u"Findn Next", None))
        self.doc_find_previous_btn.setText(QCoreApplication.translate("MainWindow", u"Find Previous", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Find", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Replace", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Document to Edit", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Edit", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"Recognize", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QCoreApplication.translate("MainWindow", u"Link", None))
    # retranslateUi

