#coding=utf-8

# 导入需要用到的模块
import urllib2
import re
import os
import sys
import threading
import HTMLParser

# 抓取网页内容
def get_html(url):
	t=5
	while t>0:
		try:
			return urllib2.urlopen(url).read()
		except:
			t-=1
	print "open url failed:%s"%url

# 编译正则表达式
def allre(reg):
	return re.compile(reg,re.DOTALL)

# 下载页面资源
def down_src(html,title):
	src=allre(r'src="(.*?)"').findall(html)
	id = 1
	for s in src:
		nsrc='src/'+title + str(id)
		nsrc = nsrc.replace('#','').replace('(','').replace(')','').replace('.','').replace(' ','')
		nsrc = nsrc + '.png'
		open(workdir+nsrc,"w").write(get_html(s))
		html=html.replace(s,'../'+nsrc)
	return html

# 获取contest内容
def get_contest(c):
	html=get_html("http://codeforces.com/contest/%d/problems"%c)
	p=allre('class="caption">(.*?)</div>').findall(html)
	if len(p)==0:
		return None
	title=HTMLParser.HTMLParser().unescape(p[0]) # 获取标题

	html_path = workdir + 'html/[%d]%s.html'%(c,title.replace('/','_'))
	flag = False
	if os.path.exists(html_path):
		flag = True
	else:
		html=allre('(<div style="text-align: center;.*)').findall(html)[0] # 获取比赛页面内容
		html=down_src(html,title) #下载页面所需要的src
	return (c,title,html_path,html,flag)

# 存储contest内容
def save_contest(contest):
	html_path=contest[2]
	html=contest[3]
	open(html_path,'w').write(header+html)

# ---------------------------------------------------------------
# 多线程类
class crawl_contest(threading.Thread):
    def __init__(this):
        threading.Thread.__init__(this)
    def run(this):
    	global begin
    	while begin<=end:
	    	lock.acquire()
	    	curid=begin
	    	begin+=1
	    	lock.release()
	    	contest=get_contest(curid)
	    	lock.acquire()
	    	# 三种情况，1- 没有获取到页面 2 - 页面已经下载过了 3 - 正常爬取页面
	    	if contest==None:
	    		print "cannot crawl contest %d"%curid
	    	elif contest[4]:
	    		print "existed:[%d]%s"%(contest[0],contest[1])
	    	else:
	    		save_contest(contest)
	    		print "crawled:[%d]%s"%(contest[0],contest[1])
	    	lock.release()
# ---------------------------------------------------------------



# ---------------------------------------------------------------
# 从控制台获取参数 python xx.py 200 300 20 xxxx  ----- 5
#                         0      1   2   3  4
# argv[1] -> begin
# argv[2] -> end
# argv[3] -> thread number
# argv[4] -> workdir 默认为当前目录

arglen=len(sys.argv)
if arglen<4 or arglen>5:
	print "Usage:\n\t%s begin end threads [workdir]"%sys.argv[0]
	exit()
if arglen==5:
	workdir=sys.argv[4]
else:
	workdir="./"

begin=int(sys.argv[1])
end=int(sys.argv[2])
threads=int(sys.argv[3])

# 创建src与html目录
for d in ['src','html']:
	d = workdir + d
	if not os.path.exists(d):
		print "makedirs:%s"%d
		os.makedirs(d)
# ---------------------------------------------------------------



# 初始化线程lock
lock = threading.RLock()

#读取html头
header=open("header.html").read()

# 开始工作
print "crawl contest %d to %d\n%d threads used,save in %s"%(begin,end,threads,workdir)
for i in range(threads):
	crawl_contest().start()