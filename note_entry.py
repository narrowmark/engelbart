import time
import wx
import xapian

class NoteEntry(wx.Frame):
  def __init__(self, parent, title):
    super(NoteEntry, self).__init__(parent, title=title, size=(300, 250))
    self.InitUI()
    self.Show()

  def InitUI(self):
    panel = wx.Panel(self)

    # General GUI layout
    hbox = wx.BoxSizer(wx.HORIZONTAL)

    sizer = wx.FlexGridSizer(3, 2, 9, 25)

    subject = wx.StaticText(panel, label='Subject')
    note = wx.StaticText(panel, label='Note')

    self.subject_text = wx.TextCtrl(panel)
    self.note_text = wx.TextCtrl(panel, style=wx.TE_MULTILINE)

    sizer.AddMany([(subject), (self.subject_text, 1, wx.EXPAND),
                   (note), (self.note_text, 1, wx.EXPAND)])
    sizer.AddGrowableRow(1, 1)
    sizer.AddGrowableCol(1, 1)

    hbox.Add(sizer, proportion=1, flag=wx.ALL|wx.EXPAND, border=15)
    panel.SetSizer(hbox)

    # Accelerator features
    save = wx.NewId()
    open = wx.NewId()

    self.Bind(wx.EVT_MENU, self.onCtrlS, id=save)
    self.Bind(wx.EVT_MENU, self.onCtrlO, id=open)

    self.accel = wx.AcceleratorTable(
        [(wx.ACCEL_CTRL, ord('S'), save),
         (wx.ACCEL_CTRL, ord('O'), open)])
    self.SetAcceleratorTable(self.accel)

  def onCtrlS(self, e):
    self.index('test_db')

  def onCtrlO(self, e):
    pass

  def index(self, db_path="default_db"):
    subject = self.subject_text.GetValue()
    note = self.note_text.GetValue()
    now = time.ctime()

    db = xapian.WritableDatabase(db_path, xapian.DB_CREATE_OR_OPEN)

    indexer = xapian.TermGenerator()
    stemmer = xapian.Stem("english")
    indexer.set_stemmer(stemmer)

    doc = xapian.Document()
    doc.set_data(note)

    indexer.set_document(doc)
    indexer.index_text(subject)
    indexer.index_text(note)
    indexer.index_text(now)

    db.add_document(doc)

    self.note_text.Clear()

if __name__ == '__main__':
  app = wx.App()
  NoteEntry(None, title="Note Entry")
  app.MainLoop()
