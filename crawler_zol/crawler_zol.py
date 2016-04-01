# *-* coding: UTF-8 *-*
__author__ = 'BG'
import urllib2
import os
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class ZOLPIC:

	# 初始化ZOLPIC类
	# 默认的base地址为ZOL壁纸首页
	# 通过手动读入想要下载的图片分类地址
	# 创建文件夹
	def __init__(self):
		self.base_html = "http://desk.zol.com.cn"
		print "请输入想要下载的图片分类的网址："
		self.cla_html = raw_input()
		if not os.path.exists('./PIC'):
			os.mkdir(r'./PIC')

	# 获取某个页面的内容
	def getHtml(self,url):	
		try:
			html = urllib2.urlopen(url)
			html = html.read().decode('gbk').encode('utf-8') 	
			return html
		except:
			return None

	# 下载图片
	# 通过正则表达式对图片地址进行匹配
	# 创建文件并写入数据
	def downloadPic(self,url,ml):
		src_html = re.compile(r'<img src="(.*?)">').findall(url)[0]
		pic_name = re.compile(r'http.*/(.*[jpg|png])').findall(src_html)[0]
		file_name = r'./PIC/'+ ml + r'/' + pic_name
		if os.path.exists(file_name):							#已经抓取过
			print '图片已经存在 %s' % pic_name
			return
		picsrc = urllib2.urlopen(src_html).read()
		# print picsrc
		print '正在下载图片 %s' % pic_name
		open( file_name,"w").write(picsrc)

	def startCrawler(self):
		html = self.getHtml(self.cla_html)
		while True:
			reg = re.compile(r'<ul class="pic-list2  clearfix">.*</ins></li>		</ul>',re.DOTALL)
			page = reg.findall(html)
			#print page
			regpic = re.compile(r'href="(/bizhi/.*?html)"',re.DOTALL)
			pic = regpic.findall(page[0])
			for p in pic:
				cur_page = self.getHtml(self.base_html+p)
				num = re.compile(r'picTotal 		: ([0-9]+)')
				picTotal = int(num.findall(cur_page)[0])
				ml_name = re.compile(r'nowGroupName 	: "(.*?)"').findall(cur_page)[0]
				print '\n\n当前组图名: %s , 共有 %d 张 '%(ml_name,picTotal)
				print '-------------------------------------------'
				if not os.path.exists(r'./PIC/'+str(ml_name)):
					os.mkdir(r'./PIC/'+str(ml_name))
				while picTotal > 0 :
					ori_screen	=  re.compile(r'oriScreen.*: "(.*?)"').findall(cur_page)[0]
					# print ori_screen
					if  ori_screen:
						full_pic = re.compile(r'href="(/showpic/%s.*?.html)' %ori_screen).findall(cur_page)[0]
						# print full_pic
						next_page = cur_page
						cur_page = self.getHtml(self.base_html+full_pic)
						# print cur_page
						self.downloadPic(cur_page,ml_name)
						cur_page = self.base_html + re.compile(r'nextPic.*: "(/bizhi/.*?html)"').findall(next_page)[0]
						cur_page = self.getHtml(cur_page)
					picTotal = picTotal - 1
					print '-------------------------------------------'
			pat = re.compile(r'<a id="pageNext" href="(.*)" class="next".*?>')
			nextPage = pat.findall(html)
			html = self.getHtml(self.base_html + nextPage[0]) 
			if not html:
				return 

if __name__ == '__main__':
	spider = ZOLPIC()
	spider.startCrawler()
