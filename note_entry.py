from Tkinter import Tk, Button, Frame, Label, Text, BOTH, W, N, E, S
from ttk import Style, Entry

class Note_Entry(Frame):
  def __init__(self, parent):
    Frame.__init__(self, parent)
    self.parent = parent
    self.initUI()

  def initUI(self):
    self.parent.title("Note Entry")
    self.pack(fill=BOTH, expand=1)

    subject_label = Label(self, text="Subject:")
    subject_label.grid(row=0, column=0, padx=5, pady=3, sticky=W)

    subject_box = Entry(self)
    subject_box.grid(row=1, column=0, padx=5, sticky=W+E)

    note_label = Label(self, text="Note:")
    note_label.grid(row=2, column=0, padx=5, sticky=W)

    note_box = Text(self)
    note_box.grid(row=3, column=0, padx=5, pady=5, sticky=E+W+S+N)

def main():
  root = Tk()
  app = Note_Entry(root)
  root.mainloop()

if __name__ == '__main__':
  main()
