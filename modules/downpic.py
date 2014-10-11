# -*- coding:utf-8 -*-
import wx,time,threading,os
import urllib2,re
from urlparse import urlparse
from tbsearch import TbSearch
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
class Create():
	def __init__(self,panel):
		self.topframe=panel.GetGrandParent()
		self.draw_Boxsizer(panel)

	def Run(self,evt):
		val=self.searchText.GetValue()
		if val=='' or val==None:
			dlg=wx.MessageDialog(None,message=u'亲,你还没有输入下载地址呢，我跑不起来呀!',caption=u'提示',style=wx.OK)
			return dlg.ShowModal()
		if val.find('http://')==-1:
			val='http://'+val
		urlinfo=urlparse(val)
		netloc=urlinfo.netloc
		self.datahandle='ali'
		if netloc.find('1688')==-1 and netloc.find('taobao.com')==-1  :
			dlg=wx.MessageDialog(None,message=u'亲,该地址暂时未能支持呀！',caption=u'提示',style=wx.OK)
			return dlg.ShowModal()
		if netloc.find('taobao.com')!=-1:
			self.datahandle='taobao'
		self.searchText.SetValue(val)
		self.opButton.Disable()
		self.msgbox.Clear()
		self.msgbox.AppendText(u'开始准备启动啦！。。。\n')
		t = threading.Thread(target=self.ThreadRun,name='tb_thread_downpic')
		t.start()
		self.msgbox.AppendText(u'系统准备就绪，下载地址:%s 正在运行！。。。\n'%val)
	
	def OpenBtn(self,evt):
		pass
	def ThreadRun(self):
		try:
			url=self.searchText.GetValue()
			self.statusbar=self.topframe.GetStatusBar()
			self.directory=time.strftime('%Y%m%d_%H%M%S',time.localtime())
			os.mkdir(self.directory)
			self.msgbox.AppendText(u'成功创建%s文件夹！。。。\n'%self.directory)
			self.openButton.Enable()
			_TbSearch=TbSearch(self.msgbox,self.statusbar)
			curldata=_TbSearch.getData(url)
			error=curldata.get('error',None)
			if error!=None:
				return self.msgbox.AppendText(u'获取不到内容：%s\n'%error)
			data=curldata.get('data',None)
			if data==None:
				return self.msgbox.AppendText(u'该请求地址的内容数据为空')
			data=data.decode('gbk').encode('utf-8')#GBK TO UTF-8
			if self.datahandle=='taobao':
				self.TaobaoHandle(_TbSearch,data)
			elif self.datahandle=='ali':
				self.AliHandle(_TbSearch,data)

		except  OSError ,e:
			self.msgbox.AppendText(u'%s文件夹创建失败！。。。\n'%self.directory)
		except Exception , e:
			print e
			self.msgbox.AppendText(u'%s,失败！。。。\n'%e)
		else:
			self.msgbox.AppendText(u'成功下载完成！。。。\n')
		finally:
			self.msgbox.AppendText(u'运行结束\n')
			self.opButton.Enable()
	#淘宝图片下载
	def TaobaoHandle(self,_TbSearch,buff):
		pics={}
		pics['Colours']=pics['Thumbs']=pics['Conts']=None
		getColours=re.compile(r'<dl class="J_Prop tb-prop tb-clearfix">.*?<dd>(.*?)</dd></dl>',re.M|re.S)
		getThumb=re.compile(r'<ul id="J_UlThumb" class="tb-thumb tb-clearfix">(.*?)</ul>',re.M|re.S)
		getCont=re.compile(r'g_config.dynamicScript\("(.*?)"\)',re.M|re.S)
		result=getColours.search(buff)
		#颜色图片下载
		if result!=None:
			html=result.group(1)
			partern=re.compile(r'<a href="#" style="background:url\((.*?)\).*?">.*?<span>(.*?)</span>',re.M|re.S)
			pics['Colours']=partern.findall(html)
		#thumb
		result=getThumb.search(buff)
		if result!=None:
			html=result.group(1)
			partern=re.compile(r'<img data-src="(.*?)".*?>',re.M|re.S)
			pics['Thumbs']=partern.findall(html)
		#contents
		result=getCont.search(buff)
		if result!=None:
			conturl=result.group(1)
			data=_TbSearch.getData(conturl)
			html=data.get('data',None)
			if(html!=None):
				partern=re.compile(r'<img.*? src="(.*?)".*?>',re.M|re.S)
				pics['Conts']=partern.findall(html)
		for item in pics:
			if pics[item]==None:
				continue
			_name=u'详情'
			if item=='Colours':
				_name=u'多色'
			elif item=='Thumbs':
				_name=u'缩略图'
			_dirs=u'./%s/%s'%(self.directory,_name)
			os.mkdir(_dirs)
			i=0
			for _item in pics[item]:
				if isinstance(_item, tuple) :
					picurl=_item[0]
					name=_item[1]
				elif isinstance(_item, str) :
					name=str(i)
					picurl=_item
				_picurl=re.sub(r'_\d+x\d+\.(.*)','',picurl)
				data=_TbSearch.getData(_picurl)
				stream=data.get('data',None)
				if stream==None:
					continue
				extion=_picurl.split('.')[-1]
				_file=_dirs+u'/%s.%s'%(name.decode('utf-8'),extion)
				_fp=open(_file,'wb')
				_fp.write(stream)
				_fp.close()
				i+=1





	def draw_Boxsizer(self,panel):
		#basic control
		panel=wx.Panel(panel,-1)
		searchLabel = wx.StaticText(panel, -1, u"下载地址:")  
		searchText = wx.TextCtrl(panel, -1)
		opLabel = wx.StaticText(panel, -1, u"操作选项:")  
		opButton = wx.Button(panel, -1,u"运行",size=(50,25))
		openButton = wx.Button(panel, -1,u"打开文件夹",size=(100,25))
		messagebox= wx.TextCtrl(panel, -1, u'目前仅支持淘宝及阿里巴巴！', 
			style=(wx.TE_MULTILINE | wx.TE_RICH2 | wx.TE_DONTWRAP))

		#Show panel
		inputsizer = wx.BoxSizer() 
		inputsizer.Add(searchLabel,0,wx.TOP,3)
		inputsizer.Add(searchText,1,wx.EXPAND)
		inputsizer2 = wx.BoxSizer() 
		inputsizer2.Add(opLabel,0,wx.TOP,3)
		inputsizer2.Add(opButton,0,wx.ALL)
		inputsizer2.Add(openButton,0,wx.ALL)
		sizer=wx.BoxSizer(wx.VERTICAL)
		sizer.Add(inputsizer,0,wx.EXPAND|wx.ALL,5)
		sizer.Add(inputsizer2,0,wx.EXPAND|wx.ALL,5)
		sizer.Add(messagebox,1,wx.EXPAND|wx.ALL,5)
		panel.SetSizer(sizer)

		#Bind Events
		opButton.Bind(wx.EVT_BUTTON,self.Run)
		openButton.Bind(wx.EVT_BUTTON,self.OpenBtn)

		#change to self
		self.opButton=opButton
		self.openButton=openButton
		self.msgbox=messagebox
		self.searchText=searchText
		self.statusbar=self.topframe.GetStatusBar()

		openButton.Disable();
