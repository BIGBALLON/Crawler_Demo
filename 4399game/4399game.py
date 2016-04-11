#coding=utf-8
#爬取4399所有好玩的游戏
import re
import os
import requests

# 基础url
host_url = 'http://www.4399.com'
swfbase_url = 'http://szhong.4399.com/4399swf'	
hw_url = 'http://www.4399.com/flash/gamehw.htm'

if not os.path.exists('./swf'):
	os.mkdir(r'./swf')

# 需要的正则表达式
tmp_pat = re.compile(r'<ul class="tm_list">(.*?)</ul>',re.S)
game_pat = re.compile( r'<li><a href="(/flash.*?)"><img alt=.*?src=".*?"><b>(.*?)</b></a><em><a href="/flash_fl/.*?">.*?</li>', re.S )
swf_pat = re.compile(r'_strGamePath="(.*?swf)"',re.S)

game_html = requests.get(hw_url)
game_html.encoding = 'gb2312'

tt = tmp_pat.search(game_html.text,re.S).group(1)

game_list = game_pat.findall(tt)

for l in game_list:
	# print l[0], l[1]
	
	game_page = requests.get(host_url + l[0]).text
	src_url = swf_pat.search(game_page)
	if src_url == None:
		continue;
	src = requests.get( swfbase_url + src_url.group(1) ).content
	print "正在保存游戏:" , l[1] 
	open( "./swf/"+ l[1] + ".swf", "wb" ).write( src )


