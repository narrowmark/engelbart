from Tkinter import Tk, Button, Frame, Label, Text, BOTH, W, N, E, S
from ttk import Style

class UI(Frame):
  def __init__(self, parent):
    Frame.__init__(self, parent)
    self.parent = parent
    self.init()

  def init(self):
    self.parent.title("Engelbart - UEG Interface")
    self.style = Style()
    self.style.theme_use("default")
    self.pack(fill=BOTH, expand=1)

    self.columnconfigure(1, weight=1)
    self.columnconfigure(3, weight=1)

    # Text area in which notes are entered.
    entry_area = Text(self)
    entry_area.grid(row=1, column=0, columnspan=2, rowspan=4,
                    padx=10, stick=E+W+S+N)

    # Text area in which search results are displayed.
    search_area = Text(self)
    search_area.grid(row=1, column=3, columnspan=2, rowspan=4,
                     padx=10, stick=E+W+S+N)

def main():
  root = Tk()
  root.geometry("750x300+300+300")
  app = UI(root)
  root.mainloop()

if __name__ == "__main__":
  main()
