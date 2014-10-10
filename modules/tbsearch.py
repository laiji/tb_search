# -*- coding:utf-8 -*- 
import urllib2,urllib,json,re,time
class TbSearch():
	def __init__(self,msg,statusbar):
		self.msg=msg
		self.statusbar=statusbar
	def getShopid(self,nid):
		time.sleep(1)
		try:
			shopid=0
			url="http://item.taobao.com/item.htm?id=%d"%nid
			_data=self.getData(url)
			getdata=_data.get('data',None)
			if getdata==None:
				raise ValueError('0')
			s=getdata.decode('gbk').encode('utf-8')
			pattern = re.compile('userId: \'(.*?)\'')
			k= pattern.findall(s)
			if len(k)!=0:
				return k[0]
			else:#万一是天猫呢
				pattern = re.compile('sellerId:\"(.*?)\"')
				k= pattern.findall(s)
				if len(k)!=0:
					return k[0]

		except Exception, e:
			return 0
		else:
			return shopid
	def getNickname(self,nid):
		try:
			time.sleep(1)
			maxpage=3
			page=1
			url="http://rate.taobao.com/feedRateList.htm"
			nicks=[]
			shopid=self.getShopid(nid)
			if shopid==0:
				raise ValueError('No')
			for page in xrange(1,maxpage):
				if page>maxpage:
					break
				query={"auctionNumId":nid,"pageSize":100,"currentPageNum":page,"userNumId":shopid}
				query=urllib.urlencode(query)
				_data=self.getData(url+'?'+query)
				getdata=_data.get('data')
				if getdata==None or getdata=='':
					break
				s=getdata.decode('gbk','ignore').encode('utf-8')
				s=s.replace('\r\n\r\n(','')
				s=s.replace(')\r\n','')
				_json=json.loads(s)
				if _json==None or _json=='':
					continue
				maxpage=_json.get('maxPage',None)
				if maxpage==None:
					continue
				maxpage=int(maxpage)
				comments=_json.get('comments',None)
				if comments==None:
					break
				for comment in comments:
					userinfo=comment.get('user',None)
					if userinfo==None:
						continue
					anyony=userinfo.get('anony',None)
					if anyony!=False:
						continue
					nick=userinfo.get('nick',None)
					rank=userinfo.get('rank',None)
					nicks.append({'nick':nick.encode('utf-8'),'rank':rank})
		except Exception, e:
			time.sleep(1)
			return {'nicks':nicks}
		else:
			return {'nicks':nicks}

	def getNids(self,keywords,datafrom,page=1):
		try:
			time.sleep(1)
			nids=[]
			keywords=keywords.encode('utf-8');
			url="http://s.m.taobao.com/search?"
			query={'q':keywords,'event_submit_do_new_search_auction':1,'n':20,'_input_charset':'utf-8','topSearch':1,'atype':'b','searchfrom':1,'action':'home%3Aredirect_app_action','buying':'buyitnow','m':'api4h5','wlsort':'1','page':page}
			query=urllib.urlencode(query)
			_data=self.getData(url+'?'+query)
			if(_data.get('error')):
				return {'error':_data['error']}
			__data=json.loads(_data['data']);
			items=__data.get('listItem')
			if(items==None or items==''):
				raise ValueError('Data is None')
			for item in items:
				nid=item.get('itemNumId')
				if(nid==None or nid==''):
					continue
				nids.append(int(nid))
			self.statusbar.SetStatusText(u'获取到%d个宝贝的ID'%(len(nids)),0)
		except Exception, e:
			return {'error':u'getNids：未知错误'}
		else:
			return {'nids':nids}
	def getData(self,url):
		data=''
		_ret={}
		try:
			time.sleep(1)
			self.statusbar.SetStatusText(u'请求URL:%s'%url,0)
			opener = urllib2.build_opener()
			opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.1')]
			raw=opener.open(url,timeout=3)
			data=raw.read()
			opener.close()
		except Exception, e:
			_ret['error']=u'请求错误：'+url+'\n'
		else:
			_ret['data']=data
		finally:
			return _ret