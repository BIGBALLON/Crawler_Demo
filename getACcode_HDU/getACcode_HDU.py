#coding=utf-8
import re, HTMLParser, requests, getpass, os

# 初始化会话对象 以及 cookies
s = requests.session()
cookies = dict(cookies_are='working')

# 一些基础的url
host_url = 'http://acm.hdu.edu.cn'
post_url = 'http://acm.hdu.edu.cn/userloginex.php?action=login'
status_url = 'http://acm.hdu.edu.cn/status.php?user='
codebase_url = 'http://acm.hdu.edu.cn/viewcode.php?rid='

# 正则表达式的匹配串
runid_pat = re.compile(r'<tr.*?align=center ><td height=22px>(.*?)</td>.*?</tr>',re.S)
code_pat = re.compile(r'<textarea id=usercode style="display:none;text-align:left;">(.+?)</textarea>',re.S)
lan_pat = re.compile(r'Language : (.*?)&nbsp;&nbsp',re.S)
problem_pat = re.compile(r'Problem : <a href=.*?target=_blank>(.*?) .*?</a>',re.S)
nextpage_pat = re.compile(r'Prev Page</a><a style="margin-right:20px" href="(.*?)">Next Page ></a>',re.S)

# 代码保存目录
if not os.path.exists('./ac_code'):
	os.mkdir(r'./ac_code')
base_path = r'./ac_code/'

# 登陆
def login(usr,psw):
	data = {'username':usr,'userpass':psw,'login':'Sign In'}	
	r = s.post(post_url,data=data,cookies=cookies)

# 代码语言判断	
def lan_judge(language):
	if language == 'G++':
		suffix = '.cpp'
	elif language == 'GCC':
		suffix = '.c'
	elif language == 'C++':
		suffix = '.cpp'
	elif language == 'C':
		suffix = '.c'
	elif language == 'Pascal':
		suffix = '.pas'
	elif language == 'Java':
		suffix = '.java'
	else:
		suffix = '.cpp'
	return suffix



if __name__ == '__main__':
	
	usr = raw_input('input your username:')
	psw = getpass.getpass('input your password:')
	
	login(usr,psw)
	
	# 用于处理html中的转义字符
	html_parser = HTMLParser.HTMLParser()

	# 遍历每一页，并下载其代码
	status_url = status_url  + usr + '&status=5'
	status_html = s.get(status_url,cookies=cookies).text
	flag = True
	while( flag ):
		runid_list = runid_pat.findall(status_html)

		for id in runid_list:
			code_url = codebase_url + id
			down_html = s.get(code_url,cookies=cookies).text

			down_code = code_pat.findall(down_html)[0]
			language = lan_pat.findall(down_html)[0]
			problemid = problem_pat.findall(down_html)[0]

			suffix = lan_judge(language)
			code = html_parser.unescape(down_code).encode('utf-8')
			code = code.replace('\r\n','\n')
			open( base_path + 'hdu' + problemid + '__' + id + suffix,"wb").write(code)
		
		nexturl = nextpage_pat.findall(status_html)
		# print nexturl[0]
		if nexturl == []:
			flag = False
		else:
			status_url = host_url + nexturl[0]
			status_html = s.get(status_url,cookies=cookies).text
	print "all of your ac codes were saved!"



