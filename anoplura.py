#!/usr/bin/env python3

"""Run the GUI."""

import pipes
import sys
import tempfile
import uuid
from signal import SIGPIPE, SIG_DFL, signal

import pandas as pd
from PySide2 import QtCore, QtWidgets
from PySide2.QtWidgets import QApplication, QFileDialog

import src.pylib.db as db
import src.pylib.doc as doc
from src.gui.data_frame_model import DataFrameModel
from src.gui.edit_pipes import EditPipes
from src.gui.main_window import Ui_MainWindow
from src.pylib.command import add_command, select_pipes

OK = 0
ERROR = 1
signal(SIGPIPE, SIG_DFL)


# TODO: Break this into smaller more manageable modules
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    """Main page of the app."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        self.doc_id = ''

        # edit pipes dialog
        pipes_df = self.load_dataframe(select_pipes)
        # pipes_df2 = pipes_df.loc[:, ['pipe_id', 'pipe']]
        self.pipes_model = DataFrameModel(pipes_df)
        # self.select_pipe_model = DataFrameModel(pipes_df2)
        self.edit_pipes = EditPipes(self)

        # Import tab controls
        self.pdf_to_text_btn.clicked.connect(self.pdf_to_text_clicked)
        self.import_text_btn.clicked.connect(self.import_text_clicked)
        self.db_backup_btn.clicked.connect(
            lambda: self.event_status(db.backup_database))
        self.db_rebuild_btn.clicked.connect(self.reset_db_clicked)

        docs = self.load_dataframe(doc.select_docs)
        self.docs_model = DataFrameModel(docs)
        self.docs_tbl.setModel(self.docs_model)
        self.docs_tbl.resizeColumnsToContents()

        # Edit tab controls
        self.edit_doc_combobox_items()
        self.edit_doc_cbox.currentTextChanged.connect(
            self.edit_doc_combobox_selected)
        self.doc_edit_text.setPlainText('')
        self.select_pipe_cbox.setAutoCompletionCaseSensitivity(
            QtCore.Qt.CaseSensitive)
        self.add_pipe_btn.clicked.connect(self.add_pipe_clicked)
        self.run_pipe_btn.clicked.connect(self.run_pipe_clicked)
        self.edit_pipes_btn.clicked.connect(self.edit_pipes_clicked)
        self.doc_edits_save_btn.clicked.connect(self.save_edits_clicked)
        self.doc_edits_cancel_btn.clicked.connect(self.cancel_edits_clicked)
        self.doc_edits_reset_btn.clicked.connect(self.reset_edits_clicked)

    def pdf_to_text_clicked(self):
        """Attach open PDFs dialog."""
        files, _ = QFileDialog.getOpenFileNames(
            parent=self,
            caption='Load PDF files into Database',
            filter='All Files (*);;PDF Files (*.pdf)')
        if files:
            doc.import_files(files, type_='pdf')
            self.update_doc_table()

    def import_text_clicked(self):
        """Import a text file."""
        files, _ = QFileDialog.getOpenFileNames(
            parent=self,
            caption='Load text files into Database',
            filter='All Files (*);;Text Files (*.txt)')
        if files:
            doc.import_files(files, type_='txt')
            self.update_doc_table()

    def update_doc_table(self):
        """Update the doc table to add data and resize columns."""
        self.docs_model.dataframe = doc.select_docs()
        self.docs_tbl.resizeColumnsToContents()
        self.edit_doc_combobox_items()
        self.set_status('Files loaded.')

    def reset_db_clicked(self):
        """Reset the database."""
        self.event_status(db.create)
        df = self.load_dataframe(doc.select_docs)
        self.docs_model.dataframe = df

    def edit_doc_combobox_items(self):
        """Update the document to edit's combobox items."""
        self.edit_doc_cbox.clear()
        items = [''] + self.docs_model.dataframe['doc_id'].tolist()
        self.edit_doc_cbox.addItems(items)

    def edit_doc_combobox_selected(self, doc_id):
        """Show the document for editing."""
        self.doc_id = doc_id
        if doc_id:
            text = self.get_doc_edits(doc.select_doc, doc_id) if doc_id else ''
            self.doc_edit_text.setPlainText(text)
            self.run_pipe_btn.setEnabled(True)
            self.doc_edits_save_btn.setEnabled(True)
            self.doc_edits_cancel_btn.setEnabled(True)
            self.doc_edits_reset_btn.setEnabled(True)
        else:
            self.doc_edit_text.setPlainText('')
            self.run_pipe_btn.setEnabled(False)
            self.doc_edits_save_btn.setEnabled(False)
            self.doc_edits_cancel_btn.setEnabled(False)
            self.doc_edits_reset_btn.setEnabled(False)

    def load_dataframe(self, func, *args, **kwargs):
        """Load a data frame from the database."""
        try:
            df = func(*args, **kwargs)
            return df
        except Exception as err:
            self.set_status(err, status=ERROR)
            return pd.DataFrame()

    def add_pipe_clicked(self):
        """Add the current text to the pipe combobox."""
        text = self.select_pipe_cbox.currentText()
        if text:
            parts = text.split('=', 1)
            if len(parts) == 1:
                pipe_id, pipe_ = uuid.uuid4(), parts[0]
            else:
                pipe_id, pipe_ = parts
            pipe_id, pipe_ = pipe_id.strip(), pipe_.strip()
            if not pipe_id or not pipe_:
                return
            add_command(pipe_id, pipe_)
            df = self.load_dataframe(select_pipes)
            for _, row in df.iterrows():
                pass

    def run_pipe_clicked(self):
        """Run the selected pipe."""
        pipe = pipes.Template()
        cmd = self.select_pipe_cbox.currentText()
        pipe.append(cmd, '--')
        # pipe.append('tr a-z A-Z', '--')
        with tempfile.NamedTemporaryFile('r') as temp_file:
            with pipe.open(temp_file.name, 'w') as stream:
                try:
                    input_text = self.doc_edit_text.toPlainText()
                    stream.write(input_text)
                except Exception as err:
                    self.set_status(err, status=ERROR)
                temp_file.seek(0)
            edits = temp_file.read()
        self.doc_edit_text.setPlainText(edits)

    def edit_pipes_clicked(self):
        """Open the edit pipes dialog."""
        self.edit_pipes_dlg.show()

    def save_edits_clicked(self):
        """Accept changes to the doc."""
        edits = self.doc_edit_text.toPlainText()
        doc.update_doc(self.doc_id, edits)
        self.doc_edit_text.setPlainText(edits)

    def cancel_edits_clicked(self):
        """Cancel changes to the doc."""
        edits = self.get_doc_edits(doc.select_doc, self.doc_id)
        doc.update_doc(self.doc_id, edits)
        self.doc_edit_text.setPlainText(edits)

    def reset_edits_clicked(self):
        """Rest the doc back to its original form."""
        doc.reset_doc(self.doc_id)
        edits = self.get_doc_edits(doc.select_doc, self.doc_id)
        self.doc_edit_text.setPlainText(edits)

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
