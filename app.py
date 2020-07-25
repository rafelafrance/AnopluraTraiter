#!/usr/bin/env python3

"""Run the GUI."""

import pipes
import tempfile
import tkinter as tk
import tkinter.ttk as ttk
from os.path import basename, dirname, splitext
from shutil import copy
from signal import SIGPIPE, SIG_DFL, signal
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText

from ttkthemes import ThemedTk

import src.pylib.db as db
import src.pylib.doc as doc
import src.pylib.command as pipe

OK = 0
ERROR = 1
MEMORY = ':memory:'

signal(SIGPIPE, SIG_DFL)


class App:
    """Build the app."""

    def __init__(self):
        win = ThemedTk(theme='radiance')
        self.win = win
        self.dirty = False
        self.path = MEMORY
        self.doc_id = ''

        self.cxn = db.connect(self.path)
        self.curr_dir = '.'

        db.create(self.cxn, self.path)

        win.title(self.get_title())
        win.geometry('1200x800')

        menu = tk.Menu(win)

        file_menu = tk.Menu(menu, tearoff=False)
        file_menu.add_command(label='Open', underline=0, command=self.open_db)
        file_menu.add_command(label='New', underline=0, command=self.new_db)
        file_menu.add_command(
            label='Save...', underline=0,
            command=self.save_as_db,
            state=tk.DISABLED)
        file_menu.add_command(
            label='Save as...', underline=5, command=self.save_as_db)
        file_menu.add_separator()
        file_menu.add_command(
            label='Quit', underline=0, command=self.safe_quit)

        menu.add_cascade(label='File', underline=0, menu=file_menu)
        win.config(menu=menu)

        self.notebook = ttk.Notebook(win)
        self.notebook.pack(expand=True, fill="both")

        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text='Import')

        tab_frame = ttk.Frame(tab)
        tab_frame.pack(expand=True, fill='both')

        top_frame = ttk.Frame(tab_frame)
        top_frame.pack(expand=False, fill='x', pady=(24, 24))
        bottom_frame = ttk.Frame(tab_frame)
        bottom_frame.pack(expand=True, fill='both')

        button = ttk.Button(
            top_frame, text='PDF to Text...', command=self.pdf_to_text)
        button.pack(side=tk.LEFT, padx=(8, 8))

        button = ttk.Button(
            top_frame, text='Import Text...', command=self.import_text)
        button.pack(side=tk.LEFT, padx=(8, 8))

        button = ttk.Button(
            top_frame, text='OCR PDF...', state=tk.DISABLED,
            command=self.ocr_pdf)
        button.pack(side=tk.LEFT, padx=(8, 8))

        self.docs = doc.select_docs(self.cxn)
        self.docs.set_index('doc_id', inplace=True)
        self.doc_tree = ttk.Treeview(bottom_frame)
        self.doc_tree.bind('<Double-Button-1>', self.select_doc)
        self.doc_tree['columns'] = list(self.docs.columns)
        self.doc_tree.column('#0', stretch=True)
        self.doc_tree.heading('#0', text='document')
        for col in self.docs.columns:
            self.doc_tree.column(col, stretch=True)
            self.doc_tree.heading(col, text=col)
        vsb = ttk.Scrollbar(
            bottom_frame, orient='vertical', command=self.doc_tree.yview)
        vsb.pack(side='right', fill='y')
        self.doc_tree.configure(yscrollcommand=vsb.set)
        self.doc_tree.pack(expand=True, fill='both')

        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text='Transform')

        tab_frame = ttk.Frame(tab)
        tab_frame.pack(expand=True, fill='both')

        top_frame = ttk.Frame(tab_frame)
        top_frame.pack(expand=False, fill='x', pady=(24, 24))
        middle_frame = ttk.Frame(tab_frame)
        middle_frame.pack(expand=True, fill='both')
        bottom_frame = ttk.Frame(tab_frame)
        bottom_frame.pack(expand=False, fill='x', pady=(24, 24))

        self.doc_sel = ttk.Combobox(top_frame)
        self.doc_sel.pack(side=tk.LEFT, padx=(8, 8))
        self.doc_sel.bind('<<ComboboxSelected>>', self.doc_selected)

        self.edits = ScrolledText(middle_frame)
        self.edits.pack(fill="both", expand=True)
        self.edits.insert(tk.INSERT, '')

        self.pipe_sel = ttk.Combobox(bottom_frame)
        self.pipe_sel.pack(side=tk.LEFT, padx=(8, 0))
        button = ttk.Button(
            bottom_frame, text='+', command=self.add_pipe, width=1)
        button.pack(side=tk.LEFT, padx=(0, 8))
        button = ttk.Button(
            bottom_frame, text='Run Pipe', command=self.run_pipe)
        button.pack(side=tk.LEFT, padx=(8, 8))
        button = ttk.Button(
            bottom_frame, text='Reset', command=self.reset_edits)
        button.pack(side=tk.RIGHT, padx=(8, 8))
        button = ttk.Button(
            bottom_frame, text='Cancel', command=self.cancel_edits)
        button.pack(side=tk.RIGHT, padx=(8, 8))
        button = ttk.Button(
            bottom_frame, text='Save', command=self.save_edits)
        button.pack(side=tk.RIGHT, padx=(8, 8))

        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text='Pipes')

        tab_frame = ttk.Frame(tab)
        tab_frame.pack(expand=True, fill='both')

        top_frame = ttk.Frame(tab_frame)
        top_frame.pack(expand=True, fill='both')
        bottom_frame = ttk.Frame(tab_frame)
        bottom_frame.pack(expand=False, fill='x', pady=(24, 24))

        self.commands = pipe.select_cmds(self.cxn)
        self.commands.set_index('command_id', inplace=True)
        self.cmd_tree = ttk.Treeview(top_frame)
        self.cmd_tree['columns'] = list(self.commands.columns)
        self.cmd_tree.column('#0', stretch=True)
        self.cmd_tree.heading('#0', text='')
        for col in self.commands.columns:
            self.cmd_tree.column(col, stretch=True)
            self.cmd_tree.heading(col, text=col)
        vsb = ttk.Scrollbar(
            top_frame, orient='vertical', command=self.cmd_tree.yview)
        vsb.pack(side='right', fill='y')
        self.cmd_tree.configure(yscrollcommand=vsb.set)
        self.cmd_tree.pack(expand=True, fill='both')

        button = ttk.Button(
            bottom_frame, text='Reset', command=self.reset_edits)
        button.pack(side=tk.RIGHT, padx=(8, 8))
        button = ttk.Button(
            bottom_frame, text='Cancel', command=self.cancel_edits)
        button.pack(side=tk.RIGHT, padx=(8, 8))
        button = ttk.Button(
            bottom_frame, text='Save', command=self.save_edits)
        button.pack(side=tk.RIGHT, padx=(8, 8))

    def open_db(self):
        """Open a database and fill the fields with its data."""
        path = filedialog.askopenfile(
            initialdir=self.curr_dir, title='Open a Traiter Database',
            filetypes=(('db files', '*.db'), ('all files', '*.*')))
        if not path:
            return
        self.curr_dir = dirname(path.name)
        self.path = path.name
        self.cxn = db.connect(self.path)
        self.repopulate()

    def new_db(self):
        """Open a database and fill the fields with its data."""
        path = filedialog.asksaveasfilename(
            initialdir=self.curr_dir, title='Create a New Traiter Database',
            filetypes=(('db files', '*.db'), ('all files', '*.*')))
        if not path:
            return
        self.curr_dir = dirname(path)
        self.path = path
        self.cxn = db.create(self.cxn, path)
        self.repopulate()

    def save_as_db(self):
        """Open a database and fill the fields with its data."""
        path = filedialog.asksaveasfilename(
            initialdir=self.curr_dir, title='Save the Database',
            filetypes=(('db files', '*.db'), ('all files', '*.*')))
        if not path:
            return
        copy(self.path, path)
        self.curr_dir = dirname(path)
        self.path = path
        self.cxn = db.connect(path)
        self.repopulate()

    def safe_quit(self):
        """Prompt to save changes before quitting."""
        if self.path == MEMORY and self.dirty:
            yes = messagebox.askyesno(
                self.get_title(),
                'Are you sure you want to exit before saving?')
            if not yes:
                return
        self.win.quit()

    def pdf_to_text(self):
        """Import PDFs into the database."""
        paths = filedialog.askopenfilenames(
            initialdir=self.curr_dir, title='Import PDF Files', multiple=True,
            filetypes=(('pdf files', '*.pdf'), ('all files', '*.*')))
        if paths:
            self.dirty = True
            self.curr_dir = dirname(paths[0])
            doc.import_files(self.cxn, paths, type_='pdf')
            self.repopulate()

    def import_text(self):
        """Import PDFs into the database."""
        self.dirty = True
        print('import_text')

    def ocr_pdf(self):
        """Import PDFs into the database."""
        self.dirty = True
        print('ocr_pdf')

    def repopulate(self):
        """Repopulate the controls from new data."""
        self.win.title(self.get_title())
        self.docs = doc.select_docs(self.cxn)
        self.docs.set_index('doc_id', inplace=True)

        self.doc_tree.delete(*self.doc_tree.get_children())
        for doc_id, row in self.docs.iterrows():
            self.doc_tree.insert('', tk.END, text=doc_id, values=list(row))
        self.doc_tree.column('#0', stretch=True)
        self.doc_tree.heading('#0', text='document')

        for col in self.docs.columns:
            self.doc_tree.column(col, stretch=True)
            self.doc_tree.heading(col, text=col)

        doc_ids = self.docs.index.tolist()
        if not doc_ids:
            self.doc_sel['values'] = ['']
            return

        self.doc_sel['values'] = [''] + doc_ids
        self.doc_sel['width'] = max(len(i) for i in doc_ids)
        self.doc_sel.current(0)

    def select_doc(self, _):
        """Select the doc and prepare to edit it."""
        selected = self.doc_tree.selection()
        if not selected:
            return
        self.doc_id = self.doc_tree.item(selected[0])['text']
        self.doc_sel.set(self.doc_id)
        self.doc_selected()
        self.notebook.select(1)

    def doc_selected(self, _=None):
        """Update the doc edit text box when selected."""
        self.doc_id = self.doc_sel.get()
        text = doc.select_doc_edits(self.cxn, self.doc_id)
        self.edits.delete('1.0', tk.END)
        self.edits.insert(tk.INSERT, text)

    def add_pipe(self):
        """Add a pipe to the select list."""
        self.dirty = True
        cmd = self.pipe_sel.get()
        if self.pipe_sel['values']:
            self.pipe_sel['values'] += (cmd,)
        else:
            self.pipe_sel['values'] = [cmd]

    def run_pipe(self):
        """Run the pipe on the text."""
        self.dirty = True
        cmd = self.pipe_sel.get()
        pipe_ = pipes.Template()
        pipe_.append(cmd, '--')
        with tempfile.NamedTemporaryFile('r') as temp_file:
            with pipe_.open(temp_file.name, 'w') as stream:
                try:
                    text = self.edits.get('1.0', tk.END)
                    stream.write(text)
                except Exception as err:
                    print(err)
                temp_file.seek(0)
            text = temp_file.read()
        self.edits.delete('1.0', tk.END)
        self.edits.insert(tk.INSERT, text)

    def save_edits(self):
        """Save edits to the database."""
        text = self.edits.get('1.0', tk.END)
        doc.update_doc(self.cxn, self.doc_id, text)

    def cancel_edits(self):
        """Cancel edits back to the last saved point."""
        text = doc.select_doc_edits(self.cxn, self.doc_id)
        self.edits.delete('1.0', tk.END)
        self.edits.insert(tk.INSERT, text)

    def reset_edits(self):
        """Reset edits back to the original data."""
        text = doc.select_doc_raw(self.cxn, self.doc_id)
        self.edits.delete('1.0', tk.END)
        self.edits.insert(tk.INSERT, text)

    def save_cmds(self):
        """Save edits to the database."""

    def cancel_cmds(self):
        """Cancel edits back to the last saved point."""

    def reset_cmds(self):
        """Reset edits back to the original data."""

    def get_title(self):
        """Build the window title."""
        title = splitext(basename(self.path))[0]
        return f'Traiter ({title})'


if __name__ == '__main__':
    APP = App()
    APP.win.mainloop()
