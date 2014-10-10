# -*- coding:utf-8 -*- 
import wx,time,threading
from tbsearch import TbSearch
#创建PANEL控件
class Create():
	def __init__(self,panel):
		self.panel = wx.Panel(panel, -1)
		self.draw_Boxsizer(self.panel)
		self.topframe=panel.GetGrandParent()

	def Run(self,evt):
		val=self.keywords.GetValue()
		if val=='' or val==None:
			dlg=wx.MessageDialog(None,message=u'亲,你还没有输入关键字，我跑不起来呀!',caption=u'提示',style=wx.OK)
			dlg.ShowModal()
			return False
		self.SearchBtn.Disable()
		self.CanelBtn.Show()
		self.statusbar=self.topframe.GetStatusBar()
		self.msgbox.Clear()
		self.msgbox.AppendText(u'开始准备启动啦！。。。\n')
		t = threading.Thread(target=self.ThreadRun,name='tb_thread')
		t.start()
		self.msgbox.AppendText(u'准备就绪，关键词:%s 正在运行！。。。\n'%val)
	
	def CanelRun(self,evt):
		if self.SearchBtn.IsEnabled() :
			return False
		self.CanelBtn.Disable()
	def ThreadRun(self):
		val=self.keywords.GetValue()
		_file=open(val.replace(" ", "")+'.csv','w+')
		_file.write(u"昵称,积分\n".encode('gbk'))
		try:
			datafrom=self.datafrom
			_TbSearch=TbSearch(self.msgbox,self.statusbar)
			allnids=[]
			for page in xrange(1,10):
				data=_TbSearch.getNids(val,datafrom,page)
				error=data.get('error')
				if error!=None and error!='':
					self.msgbox.AppendText(u'获取失败，第%d页宝贝,原因：%s'%(page,error))
					continue
				nids=data.get('nids')
				if nids==None or nids=='':
					self.msgbox.AppendText(u'获取失败，第%d页宝贝'%page)
					continue
				self.msgbox.AppendText(u'获取第%d页宝贝，共%d个\n'%(page,len(nids)))
				for nid in nids:
					if self.CanelBtn.IsEnabled()==False:
						raise ValueError('canel')
						break
					data=_TbSearch.getNickname(nid)
					error=data.get('error',None)
					if error!=None:
						self.msgbox.AppendText(u'宝贝：%d，运行错误：%s\n'%(nid,error))
						continue
					data=data.get('nicks',None)
					self.msgbox.AppendText(u'宝贝：%d，获取了%d个用户\n'%(nid,len(data)))

					#write data
					for item in data:
						nick=item['nick'].decode('utf-8').encode('gbk')
						rank=item['rank']
						_str=str(nick)+','+str(rank)+'\n'
						_file.write(_str)
		except ValueError,e:
			if 'canel'==str(e):
				self.msgbox.AppendText(u'郁闷，你自己给取消了\n')
			else:
				self.msgbox.AppendText(u'未知\n')
		except Exception, e:
			raise
		finally:
			_file.close()
			self.msgbox.AppendText(u'运行结束，退出！。。。\n')
			self.SearchBtn.Enable()
			if self.CanelBtn.IsEnabled() ==False:
				self.CanelBtn.Enable()

	def draw_Boxsizer(self,panel):
		#basic control
		keywordsLabel = wx.StaticText(panel, -1, u"关键词:")  
		keywordsText = wx.TextCtrl(panel, -1)
		fromLabel = wx.StaticText(panel, -1, u"搜索源:")  
		fromText = wx.RadioButton(panel, -1,u'淘宝',style=wx.RB_GROUP,name='taobao')
		fromText2 = wx.RadioButton(panel, -1,u'天猫',name='tmall')
		SearchBtn=wx.Button(panel,-1,u'搜索',size=(50,25))
		CanelBtn=wx.Button(panel,-1,u'取消',size=(50,25))
		messagebox= wx.TextCtrl(panel, -1, u'点击搜索进行拼命抓取吧！', 
			style=(wx.TE_MULTILINE | wx.TE_RICH2 | wx.TE_DONTWRAP))

		#Show panel
		inputsizer = wx.BoxSizer() 
		inputsizer.Add(keywordsLabel,0,wx.TOP,3)
		inputsizer.Add(keywordsText,1,wx.EXPAND)
		inputsizer2 = wx.BoxSizer() 
		inputsizer2.Add(fromLabel,0)
		inputsizer2.Add(fromText,0,wx.LEFT,5)
		inputsizer2.Add(fromText2,0,wx.LEFT,5)
		inputsizer2.Add(SearchBtn,0,wx.LEFT,5)
		inputsizer2.Add(CanelBtn,0,wx.LEFT,5)
		sizer=wx.BoxSizer(wx.VERTICAL)
		sizer.Add(inputsizer,0,wx.EXPAND|wx.ALL,5)
		sizer.Add(inputsizer2,0,wx.EXPAND|wx.ALL,5)
		sizer.Add(messagebox,1,wx.EXPAND|wx.ALL,5)
		panel.SetSizer(sizer)

		#Bind Events
		SearchBtn.Bind(wx.EVT_BUTTON,self.Run)
		CanelBtn.Bind(wx.EVT_BUTTON,self.CanelRun)
		fromText.Bind(wx.EVT_RADIOBUTTON,self.ChangeFrom)
		fromText2.Bind(wx.EVT_RADIOBUTTON,self.ChangeFrom)

		#change to self
		self.SearchBtn=SearchBtn
		self.CanelBtn=CanelBtn
		self.msgbox=messagebox
		self.keywords=keywordsText
		self.datafrom='taobao'

	def ChangeFrom(self,evt):
		_id=evt.GetId()
		win=self.panel.FindWindowById(_id)
		self.datafrom=win.GetName()