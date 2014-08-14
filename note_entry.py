import time
import wx
import xapian
from threading import Thread

class NoteEntryFrame(wx.Frame):
  def __init__(self, parent):
    wx.Frame.__init__(self, None, title="Note Entry", size=(300, 300))
    self.db_path = "default_db"
    self.InitUI()

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

    self.Show()
    self.ueg()

  def onCtrlS(self, e):
    self.index(self.db_path)

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

  def ueg(self):
    p_search = PassiveSearchThread(self)

class PassiveSearchFrame(wx.Frame):
  def __init__(self, parent):
    wx.Frame.__init__(self, parent, title="Passive Search", size=(300,300))
    self.parent = parent

    self.InitUI()

    self.timer = wx.Timer(self)
    self.Bind(wx.EVT_TIMER, self.search, self.timer)
    self.timer.Start(1500)

  def InitUI(self):
    panel = wx.Panel(self)

    # General GUI layout
    hbox = wx.BoxSizer(wx.HORIZONTAL)

    sizer = wx.FlexGridSizer(2, 3, 9, 25)

    result = wx.StaticText(panel, label='Result')
    self.result_text = wx.TextCtrl(panel, style=wx.TE_MULTILINE)

    sizer.Add(result, 1, wx.EXPAND)
    sizer.Add(self.result_text, 1, wx.EXPAND)

    sizer.AddGrowableRow(0, 2)
    sizer.AddGrowableCol(1, 2)

    hbox.Add(sizer, proportion=1, flag=wx.ALL|wx.EXPAND, border=10)
    panel.SetSizer(hbox)

    self.Show()

  def search(self, db_path="default_db"):
    database = xapian.Database(self.parent.db_path)

    enquire = xapian.Enquire(database)

    query_string = self.parent.note_text.GetValue()

    qp = xapian.QueryParser()
    stemmer = xapian.Stem("english")
    qp.set_stemmer(stemmer)
    qp.set_database(database)
    qp.set_stemming_strategy(xapian.QueryParser.STEM_SOME)
    query = qp.parse_query(query_string)

    enquire.set_query(query)
    matches = enquire.get_mset(0, 10)
    final = ''
    for m in matches:
      final = final + m.document.get_data() + "\n"
    self.result_text.SetValue(final)

class PassiveSearchThread(wx.Frame, Thread):
  def __init__(self, parent):
    Thread.__init__(self)
    self.parent = parent

    self.run()

  def run(self):
    p_search = PassiveSearchFrame(self.parent)

if __name__ == '__main__':
  app = wx.App()
  NoteEntryFrame(None)
  app.MainLoop()
