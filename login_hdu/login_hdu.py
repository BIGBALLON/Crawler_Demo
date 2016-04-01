#coding=utf-8
'''
urllib——用于表单数据的生成
urllib2——必要的库，不再赘述
cookielib——提供可存储cookie的对象，以便于与urllib2模块配合使用来访问Internet资源
re——用于正则表达式
HTMLParser——用于处理html代码的转义字符
'''
import urllib2, urllib, cookielib
import re, HTMLParser

host_url = 'http://acm.hdu.edu.cn/'
post_url = 'http://acm.hdu.edu.cn/userloginex.php?action=login'

# 伪装成浏览器
headers = {
    'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
}
# 生成请求，这里访问hdu的主页，而不是登陆url，这里只是为了获取cookie
# 因为hdu做了反爬虫，所有必须加入headers才能访问
req_host = urllib2.Request(
    url = host_url,
    headers = headers
)
# 获取cookie
cookie_support= urllib2.HTTPCookieProcessor(cookielib.CookieJar())
opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
urllib2.install_opener(opener)
content = urllib2.urlopen(req_host).read()
# 生成post请求所需要的表单数据
# 账号密码换成你自己的
postdata=urllib.urlencode({
	'username':'China_Lee',
	'userpass':'xxxxx',
	'login':'Sign In'
})

# 生成post所需的请求
req_post = urllib2.Request(
	url = post_url,
    data = postdata,
    headers = headers
)
# 发送请求，登陆成功
result = urllib2.urlopen(req_post).read()

# 声明一个HTMLParser实例
html_parser = HTMLParser.HTMLParser()

# 制定某一个代码页面
# 注意，这个页面是我自己找到，是我自己的AC代码，如果你使用这个页面，是没有权限的，请换一个你所AC的代码所在的URL
req_code = urllib2.Request(
    url = 'http://acm.hdu.edu.cn/viewcode.php?rid=14880688',
    headers = headers
)
# 读取页面内容
down_html = urllib2.urlopen(req_code).read()

# 分析页面后得到正则表达式
pattern = re.compile('<textarea id=usercode style="display:none;text-align:left;">(.+?)</textarea>',re.S)
# 使用正则表达式匹配code
down_code = pattern.findall(down_html)[0]
# 使用unescape处理html中的转义字符
code = html_parser.unescape(down_code)
# 使用replace处理\r\n,windows下和linux下并不相同
code = code.replace('\r\n','\n')
# 将代码存储为test.cpp
open('test.cpp',"w").write(code)

