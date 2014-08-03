from Tkinter import Tk, Button, Frame, Label, Message, Menu, Text, BOTH, W, N, E, S
from ttk import Style, Entry

import tkFileDialog

import json
import sys
import xapian

import time

class Note_Entry(Frame):
  def __init__(self, parent):
    # Initialize UI elements.
    self.initFrame(parent)
    self.initUI()

    # Configuration elements.
    # Refine this implementation later.

  def initFrame(self, parent):
    Frame.__init__(self, parent)
    self.parent = parent

  def initUI(self):
    # Keyboard interface elements
    self.parent.bind("<Return>", self.quick_save)

    # Menu bar
    menu_bar = Menu(self.parent)
    self.parent.config(menu=menu_bar)

    file_menu = Menu(menu_bar)
    file_menu.add_command(label="Open", command=self.open_db)
    file_menu.add_command(label="New", command=self.new_db)
    file_menu.add_command(label="Exit", command=self.quit())
    menu_bar.add_cascade(label="File", menu=file_menu)

    # Note entry elements
    self.parent.title("Note Entry")
    self.pack(fill=BOTH, expand=1)

    subject_label = Label(self, text="Subject:")
    subject_label.grid(row=0, column=0, padx=5, pady=3, sticky=W)

    self.subject_box = Entry(self)
    self.subject_box.grid(row=1, column=0, padx=5, sticky=W+E)

    note_label = Label(self, text="Note:")
    note_label.grid(row=2, column=0, padx=5, sticky=W)

    self.note_box = Text(self)
    self.note_box.grid(row=3, column=0, padx=5, pady=5, sticky=E+W+S+N)

  def quick_save(self, parent):
    try:
      self.index(self.db_path)
    except AttributeError:
      self.db_path = "defualt_db"
      self.index(self.db_path)

  def open_db(self):
    # Opens the database to be written.
    """
    dlg = tkFileDialog.Open(self)
    self.db_file = dlg.show()
    """
    self.db_path = tkFileDialog.askdirectory()
    print self.db_path

    # Create a new file if open fails.
    """
    if self.fl == '':
      self.new_db()
    """

  def new_db(self):
    dlg = tkFileDialog.asksaveasfile(mode='w')

  def index(self, db_path):
    # Data elements
    note = self.note_box.get(1.0, 4096.0)
    note = note.strip()
    self.note_box.delete(1.0, 4096.0)

    subject = self.subject_box.get()
    cur_time = time.ctime()

    # Database elements
    db = xapian.WritableDatabase(db_path, xapian.DB_CREATE_OR_OPEN)

    indexer = xapian.TermGenerator()
    stemmer = xapian.Stem("english")
    indexer.set_stemmer(stemmer)

    doc = xapian.Document()
    doc.set_data(note)

    indexer.set_document(doc)
    indexer.index_text(subject)
    indexer.index_text(note)
    indexer.index_text(cur_time)

    db.add_document(doc)

def main():
  root = Tk()
  app = Note_Entry(root)
  root.mainloop()

if __name__ == '__main__':
  main()
