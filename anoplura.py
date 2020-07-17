#!/usr/bin/env python3

"""Run the GUI."""

import sys

import pandas as pd
from PySide2 import QtWidgets
from PySide2.QtWidgets import QApplication, QFileDialog

import src.pylib.db as db
from src.gui.data_frame_model import DataFrameModel
from src.gui.main_window import Ui_MainWindow
from src.pylib.pdf import import_files

OK = 0
ERROR = 1


# TODO: Break this into smaller more manageable modules
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    """Main page of the app."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        self.doc_id = ''

        # Import tab controls
        self.pdf_to_text_btn.clicked.connect(self.pdf_to_text)
        self.import_text_btn.clicked.connect(self.import_text)
        self.db_backup_btn.clicked.connect(
            lambda: self.event_status(db.backup_database))
        self.db_rebuild_btn.clicked.connect(self.reset_db)

        df = self.load_dataframe(db.select_docs)
        self.docs_model = DataFrameModel(df)
        self.docs_tbl.setModel(self.docs_model)
        self.docs_tbl.resizeColumnsToContents()

        # Edit tab controls
        self.edit_doc_combobox_items()
        self.edit_doc_cbox.currentTextChanged.connect(
            self.edit_doc_combobox_select)
        # self.edit_doc_cbox.
        self.doc_edit_text.setPlainText('')
        self.doc_edits_save_btn.clicked.connect(self.save_edits)
        self.doc_edits_cancel_btn.clicked.connect(self.cancel_edits)
        self.doc_edits_reset_btn.clicked.connect(self.reset_edits)

    def pdf_to_text(self):
        """Attach open PDFs dialog."""
        files, _ = QFileDialog.getOpenFileNames(
            parent=self,
            caption='Load PDF files into Database',
            filter='All Files (*);;PDF Files (*.pdf)')
        if files:
            import_files(files, type_='pdf')
            self.update_doc_table()

    def import_text(self):
        """Import a text file."""
        files, _ = QFileDialog.getOpenFileNames(
            parent=self,
            caption='Load text files into Database',
            filter='All Files (*);;Text Files (*.txt)')
        if files:
            import_files(files, type_='txt')
            self.update_doc_table()

    def update_doc_table(self):
        """Update the doc table to add data and resize columns."""
        self.docs_model.dataframe = db.select_docs()
        self.docs_tbl.resizeColumnsToContents()
        self.edit_doc_combobox_items()
        self.set_status('Files loaded.')

    def reset_db(self):
        """Reset the database."""
        self.event_status(db.create)
        df = self.load_dataframe(db.select_docs)
        self.docs_model.dataframe = df

    def edit_doc_combobox_items(self):
        """Update the document to edit's combobox items."""
        self.edit_doc_cbox.clear()
        items = [''] + self.docs_model.dataframe['doc_id'].tolist()
        self.edit_doc_cbox.addItems(items)

    def edit_doc_combobox_select(self, doc_id):
        """Show the document for editing."""
        self.doc_id = doc_id
        text = self.get_doc_edits(db.select_doc, doc_id) if doc_id else ''
        self.doc_edit_text.setPlainText(text)

    def load_dataframe(self, func, *args, **kwargs):
        """Load a data frame from the database."""
        try:
            df = func(*args, **kwargs)
            return df
        except Exception as err:
            self.set_status(err, status=ERROR)
            return pd.DataFrame()

    def save_edits(self):
        """Accept changes to the doc."""
        edits = self.doc_edit.toPlainText()
        db.update_doc(self.doc_id, edits)
        self.doc_edit.setPlainText(edits)

    def cancel_edits(self):
        """Cancel changes to the doc."""
        edits = self.get_doc_edits(db.select_doc, self.doc_id)
        db.update_doc(self.doc_id, edits)
        self.doc_edit.setPlainText(edits)

    def reset_edits(self):
        """Rest the doc back to its original form."""
        db.reset_doc(self.doc_id)
        edits = self.get_doc_edits(db.select_doc, self.doc_id)
        self.doc_edit.setPlainText(edits)

    def get_doc_edits(self, func, *args, **kwargs):
        """Get the current state of the doc from the database."""
        result = ''
        try:
            result = func(*args, **kwargs)
        except Exception as err:
            self.set_status(err, status=ERROR)
        return result

    def event_status(self, func, msg=''):
        """Wrap action so that we can display results."""
        result = None
        try:
            result = func()
            self.set_status(msg)
        except Exception as err:
            self.set_status(err, status=ERROR)
        return result

    def set_status(self, msg, status=OK):
        """Display the status."""
        msg = ' '.join(str(msg).split())
        color = 'rgb(0,0,0)' if status == OK else 'rgb(255,0,0)'
        self.statusBar().setStyleSheet(f'color: {color};')
        self.statusBar().showMessage(msg)


def main():
    """Do it."""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
