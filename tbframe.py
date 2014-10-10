# -*- coding:utf-8 -*- 
import wx
import random,time
from modules import *
class TaoBaoFrame(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self,None,-1,u'淘宝工具--健宜专用版')
		self.ntpanel=wx.Notebook(self,-1)
		self.drawnotebook(self.ntpanel)
		
		statusBar = wx.StatusBar(self, -1)
		statusBar.SetFieldsCount(2) 
		statusBar.SetStatusWidths([-1,50])
		statusBar.SetStatusText(u"运行中。。。", 0)
		statusBar.SetStatusText("By Lailaiji", 1)
		self.SetStatusBar(statusBar)

	def drawnotebook(self,ntpanel):
		ntpages=[{'name':'买家昵称','id':2001},{'name':'图片下载','id':2002},{'name':'图片合成','id':2003}]
		for page in ntpages:
			showpage=wx.NotebookPage(ntpanel,page['id'])
			showpage.SetBackgroundColour('white')
			ntpanel.AddPage(showpage,page['name'].decode('utf-8'))
			self.On_DrawOnePage(page['id'],showpage)

	#一次性绘制
	def On_DrawOnePage(self,pageid,panel):
		if(pageid==2001):
			buyer_nick.Create(panel);
		elif(pageid==2002):
			downpic.Create(panel);
		else:
			statictext=wx.StaticText(panel,-1,u'暂时尚未支持',pos=(random.randint(1,300),random.randint(1,300)))

if __name__=='__main__':
	print 'please startup main.py'