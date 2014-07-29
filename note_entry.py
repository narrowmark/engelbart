from Tkinter import Tk, Button, Frame, Label, Message, Text, BOTH, W, N, E, S
from ttk import Style, Entry

import json
import sys
import xapian

import time

class Note_Entry(Frame):
  def __init__(self, parent):
    self.initFrame(parent)
    self.initUI()

  def initFrame(self, parent):
    Frame.__init__(self, parent)
    self.parent = parent

  def initUI(self):
    # Keyboard interface elements
    self.parent.bind("<Return>", self.quick_save)

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
    # Testing information exchange
    # Replace with proper save functionality later.
    note = self.note_box.get(1.0, 4096.0)
    note = note.strip()
    self.note_box.delete(1.0, 4096.0)

    entry = self.subject_box.get()
    cur_time = time.ctime()

    print note
    print entry
    print cur_time

def main():
  root = Tk()
  app = Note_Entry(root)
  root.mainloop()

if __name__ == '__main__':
  main()
