# -*- coding:utf-8 -*- 
import urllib2,urllib,json,re,time
def getData(url):
	data=''
	_ret={}
	try:
		opener = urllib2.build_opener()
		opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.1')]
		raw=opener.open(url,timeout=3)
		data=raw.read()
	except Exception, e:
		_ret['error']=u'请求错误：'+url
	else:
		_ret['data']=data
	finally:
		return _ret
url='http://rate.taobao.com/feedRateList.htm?callback=jsonp_reviews_list&currentPageNum=8&userNumId=570958094&auctionNumId=40860019504'

data=getData(url)
s=data.get('data')
s=s.decode('gbk','ignore').encode('utf-8')
print repr(s)








exit()
s=s.decode('gbk').encode('utf-8')
#s=re.replace("/userId: '(.*?)'/ims",'$1')
pattern = re.compile('userId: \'(.*?)\'')
k= pattern.findall(s) 
print k[0]
exit()
s=s.replace('\r\n\r\n(','')
s=s.replace(')\r\n','')
_json=json.loads(s)

comments=_json.get('comments',None)
print comments
'''
for comment in comments:
	userinfo=comment.get('user')
	print userinfo
	'''