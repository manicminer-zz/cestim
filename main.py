import wx
import pymysql

class MyApp(wx.App):
	
	def OnInit(self):
		
		self.frame = MyMainFrame(None, title = "Service Auto: New Look Design")
		self.SetTopWindow(self.frame)
		self.frame.Show()
		
		return True
		
class MyMainFrame(wx.Frame):
	
	def __init__(self, parent, id=wx.ID_ANY, title = "",
				 pos = wx.DefaultPosition, size = wx.DefaultSize,
				 style = wx.DEFAULT_FRAME_STYLE,
				 name = "MyMainFrame"):
					 
		super(MyMainFrame, self).__init__(parent, id, title, pos, size, style, name)
		
		self.panel = wx.Panel(self)
		
		buttonAddComm = wx.Button(self.panel, label = "Comanda Noua", pos = (50, 50), size = (100,40))
		
		buttonSrcComm = wx.Button(self.panel, label = "Cauta Comanda", pos = (50, 100), size = (100,40))

		txtSrcComm = wx.TextCtrl(self.panel, pos = (160,120), value = '')
		lblSrcComm = wx.StaticText(self.panel, label = "Introdu Nr. Auto:", pos = (160, 100))
		self.txtSrcCommId = txtSrcComm.GetId()

		
		buttonAbout = wx.Button(self.panel, label = "Despre", pos = (50, 150), size = (100,40))
		
		buttonExit = wx.Button(self.panel, label = "Iesire", pos = (50, 200), size = (100,40))
		
		self.Bind(wx.EVT_BUTTON, self.OnAddCommButton, buttonAddComm)

		self.Bind(wx.EVT_BUTTON, self.OnSrcCommButton, buttonSrcComm)

		self.Bind(wx.EVT_BUTTON, self.OnAboutButton, buttonAbout)
		
		self.Bind(wx.EVT_BUTTON, self.OnExitButton, buttonExit)

	def OnAddCommButton(self, event):
		
		self.addeditframe = MyAddEditFrame(None, title = "Adaugare Comanda")
		self.addeditframe.Show()

	def OnSrcCommButton(self, event):

		nrinmatriculare = self.panel.FindWindowById(self.txtSrcCommId)		
		self.srccommframe = MyCommListFrame(None, title = nrinmatriculare.GetValue())
		self.srccommframe.Show()

	def OnAboutButton(self, event):
		
		wx.MessageBox("Programu' lui Pompieru", "Despre")
		return True

	def OnExitButton(self, event):
		
		self.Close()
	
class MyCommListFrame(wx.Frame):

	def __init__(self, parent, id=wx.ID_ANY, title = "",
				 pos = wx.DefaultPosition, size = wx.DefaultSize,
				 style = wx.DEFAULT_FRAME_STYLE,
				 name = "MyCommListFrame"):
					 
		super(MyCommListFrame, self).__init__(parent, id, title, pos, size, style, name)
		
		MyAutoNumber = self.GetTitle()

		self.commlistpanel = wx.Panel(self)
		
		conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='blessed', db='newlook') 
		cur = conn.cursor()
		cur.execute("SELECT id_comanda, data_comanda, beneficiar FROM comenzi WHERE nr_inmatriculare = '" + MyAutoNumber +"'")

		self.mycommlist = wx.ListCtrl(self, style = wx.LC_REPORT)
		self.mycommlist.InsertColumn(0, "Nr. Comanda")
		self.mycommlist.InsertColumn(1, "Data Comanda")
		self.mycommlist.InsertColumn(2, "Beneficiar")
		
		for r in cur.fetchall():
			myitem = []
			myitem.append(r[0])
			myitem.append(r[1])
			myitem.append(r[2])
			self.mycommlist.Append(myitem)
			
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.mycommlist, 1, wx.EXPAND)
		self.SetSizer(sizer)
		
		self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemSelected)
		
	def OnItemSelected(self, event):
		
		selected_row = event.GetIndex()
		no_comm = self.mycommlist.GetItem(selected_row,0)
		
		self.addeditframe = MyAddEditFrame(None, title = no_comm.GetText())
		self.addeditframe.Show()
		

class MyAddEditFrame(wx.Frame):

	def __init__(self, parent, id=wx.ID_ANY, title = "",
				 pos = wx.DefaultPosition, size = wx.DefaultSize,
				 style = wx.DEFAULT_FRAME_STYLE,
				 name = "MyAddEditFrame"):
					 
		super(MyAddEditFrame, self).__init__(parent, id, title, pos, size, style, name)
				
		if self.GetTitle() == "Adaugare Comanda":
		
			AddMode = True
			EdtMode = False

			r = []

			#wx.MessageBox("Adaug Comanda", "Despre")

			
		else:
			
			AddMode = False
			EdtMode = True
			
			conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='blessed', db='newlook') 
			cur = conn.cursor()
			cur.execute("SELECT beneficiar, adresa_1, adresa_2 \
						 FROM comenzi WHERE id_comanda = 101") 

			r = cur.fetchall()
			
			#wx.MessageBox("Editez Comanda", "Despre")
		
		self.addeditnotebook = wx.Notebook(self)
		
		# Tabulator cu date de identificare Comanda
		self.dateidentificare = wx.Panel(self.addeditnotebook)
		
		h = 25; i = 0; MyValue = ("" if AddMode else r[0][0])
		lblNumeBeneficiar = wx.StaticText(self.dateidentificare, label = "Beneficiar:", pos = (50, h))
		txtNumeBeneficiar = wx.TextCtrl(self.dateidentificare, pos = (150,h), value = MyValue)

		h +=25; i += 1; MyValue = ("" if AddMode else r[0][i])
		lblAdresa1 = wx.StaticText(self.dateidentificare, label = "Adresa:", pos = (50, h))
		txtAdresa1 = wx.TextCtrl(self.dateidentificare, pos = (150,h), value = MyValue)

		h +=25
		lblAdresa2 = wx.StaticText(self.dateidentificare, label = "", pos = (50, h))
		txtAdresa2 = wx.TextCtrl(self.dateidentificare, pos = (150,h))

		h +=25
		lblTelefon = wx.StaticText(self.dateidentificare, label = "Telefon:", pos = (50, h))
		txtTelefon = wx.TextCtrl(self.dateidentificare, pos = (150,h))

		h +=25
		lblFax = wx.StaticText(self.dateidentificare, label = "Fax:", pos = (50, h))
		txtFax = wx.TextCtrl(self.dateidentificare, pos = (150, h))
		
		h +=25
		lblNrInmatriculareAuto = wx.StaticText(self.dateidentificare, label = "Nr.Inmatriculare:", pos = (50, h))
		txtNrInmatriculareAuto = wx.TextCtrl(self.dateidentificare, pos = (150,h))

		h +=25
		lblProducatorAuto = wx.StaticText(self.dateidentificare, label = "Producator Auto:", pos = (50, h))
		txtProducatorAuto = wx.TextCtrl(self.dateidentificare, pos = (150, h))

		h +=25
		lblTipAuto = wx.StaticText(self.dateidentificare, label = "Tip Auto:", pos = (50, h))
		txtTipAuto = wx.TextCtrl(self.dateidentificare, pos = (150, h))

		h +=25
		lblAnFabrAuto = wx.StaticText(self.dateidentificare, label = "An Fabricatie:", pos = (50, h))
		txtAnFabrAuto = wx.TextCtrl(self.dateidentificare, pos = (150, h))

		h +=25
		lblTipMotorAuto = wx.StaticText(self.dateidentificare, label = "TipMotor:", pos = (50, h))
		txtTipMotorAuto = wx.TextCtrl(self.dateidentificare, pos = (150, h))
		
		h +=25
		lblKwAuto = wx.StaticText(self.dateidentificare, label = "Kw:", pos = (50, h))
		txtKwAuto = wx.TextCtrl(self.dateidentificare, pos = (150, h))

		h +=25
		lblCilindreeAuto = wx.StaticText(self.dateidentificare, label = "Cilindree:", pos = (50, h))
		txtCilindreeAuto = wx.TextCtrl(self.dateidentificare, pos = (150, h))

		h +=25
		lblVINAuto = wx.StaticText(self.dateidentificare, label = "Serie Sasiu:", pos = (50, h))
		txtVINAuto = wx.TextCtrl(self.dateidentificare, pos = (150, h))

		# Tabulator cu Constatare
		self.constatare = wx.Panel(self.addeditnotebook)

		self.constatarelist = wx.ListCtrl(self.constatare, style = wx.LC_REPORT)
		self.constatarelist.InsertColumn(0, "Crt")
		self.constatarelist.InsertColumn(1, "Denumire")
		self.constatarelist.InsertColumn(2, "Cant")
		
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.constatarelist, 1, wx.EXPAND)
		self.constatare.SetSizer(sizer)


		# Tabulator Cu Deviz Antecalculatie
		self.devizantecalcul = wx.Panel(self.addeditnotebook)

		self.devizantecalcullist = wx.ListCtrl(self.devizantecalcul, style = wx.LC_REPORT)
		self.devizantecalcullist.InsertColumn(0, "Crt")
		self.devizantecalcullist.InsertColumn(1, "Denumire")
		self.devizantecalcullist.InsertColumn(2, "Cant")
		self.devizantecalcullist.InsertColumn(3, "P.U.")
		self.devizantecalcullist.InsertColumn(4, "Total")
		self.devizantecalcullist.InsertColumn(5, "Obs")
		
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.devizantecalcullist, 1, wx.EXPAND)
		self.devizantecalcul.SetSizer(sizer)
		
		# Tabulator Cu Deviz Reparatie
		self.devizreparare = wx.Panel(self.addeditnotebook)

		self.devizrepararelist = wx.ListCtrl(self.devizreparare, style = wx.LC_REPORT)
		self.devizrepararelist.InsertColumn(0, "Crt")
		self.devizrepararelist.InsertColumn(1, "Denumire")
		self.devizrepararelist.InsertColumn(2, "Cant")
		self.devizrepararelist.InsertColumn(3, "P.U.")
		self.devizrepararelist.InsertColumn(4, "Total")
		self.devizrepararelist.InsertColumn(5, "Obs")
		
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.devizrepararelist, 1, wx.EXPAND)
		self.devizreparare.SetSizer(sizer)

		# Se adauga Paginile la NoteBook
		self.addeditnotebook.AddPage(self.dateidentificare, "Identificare")
		self.addeditnotebook.AddPage(self.constatare, "Constatare")
		self.addeditnotebook.AddPage(self.devizantecalcul, "Deviz Antecalcul")
		self.addeditnotebook.AddPage(self.devizreparare, "Deviz Reparare")


if __name__ == "__main__":
	
	app = MyApp(False)
	app.MainLoop()
	
