#coding=utf-8
import requests, re
import Image
from pytesseract import *


def get_verification_code(url):
	src = s.get(url).content
	open('temp_pic',"wb").write(src)
	pic=Image.open(r'./temp_pic')
	return image_to_string(pic)

login_url = 'http://www.pss-system.gov.cn/sipopublicsearch/wee/platform/wee_security_check'
host_url = 'http://www.pss-system.gov.cn/sipopublicsearch/portal/index.shtml'
pic_url = 'http://www.pss-system.gov.cn/sipopublicsearch/portal/login-showPic.shtml'
pic_mask = 'http://www.pss-system.gov.cn/sipopublicsearch/search/validateCode-showPic.shtml?params=2595D550022F3AC2E5D76ED4CAFD4D8E'
search_url = 'http://www.pss-system.gov.cn/sipopublicsearch/search/smartSearch-executeSmartSearch.shtml'
show_page = 'http://www.pss-system.gov.cn/sipopublicsearch/search/showSearchResult-startWa.shtml'
show_list = 'http://www.pss-system.gov.cn/sipopublicsearch/search/search/showViewList.shtml'
mask_check_url = 'http://www.pss-system.gov.cn/sipopublicsearch/search/validateMask.shtml'
download_url = 'http://www.pss-system.gov.cn/sipopublicsearch/search/downloadLitera.do'

down_head = {
	'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	'Accept-Encoding':'gzip, deflate',
	'Accept-Language':'en-US,en;q=0.8',
	'Cache-Control':'max-age=0',
	'Connection':'keep-alive',
	'Content-Type':'application/x-www-form-urlencoded',
	'Origin':'http://www.pss-system.gov.cn',
	'Referer':'http://www.pss-system.gov.cn/sipopublicsearch/search/search/showViewList.shtml',
	'Upgrade-Insecure-Requests':'1',
	'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36'
}


s = requests.session()
cookies = dict(cookies_are='working')
s.get(host_url)

vcode = get_verification_code(pic_url)
login_data = {
	'j_validation_code':vcode,
	'j_loginsuccess_url':'http://www.pss-system.gov.cn/sipopublicsearch/portal/index.shtml',
	'j_username':'emhhbmdzYW4xMjM=',
	'j_password':'emhhbmdzYW4xMjM='
}

s.post(login_url,data=login_data,cookies=cookies)
print "login!!\n-------------------"

keywords = raw_input("please input keywords: ")
cnt = 0

search_data = {
	'searchCondition.searchExp':keywords,
	'searchCondition.dbId':'VDB',
	'searchCondition.searchType':'Sino_foreign',
	'wee.bizlog.modulelevel':'0200101'
}


result = s.post(search_url,data=search_data,cookies=cookies).content
total = int(re.search(r'&nbsp;共.*?页&nbsp;(.*?)条数据',result,re.S).group(1))
print "total:",total
all_result = re.findall('javascript:viewLitera_search\(\'.*?\',\'(.*?)\',\'single\'\)',result,re.S)

executableSearchExp = "VDB:(TBI=" + "'" + keywords + "')"
literatureSF = "复合文本=(" + keywords + ")"

while cnt <= total:
	cnt += 10
	for cur in all_result:
		real_id = cur
		if 'CN' in cur :
			real_id = cur[:14] + '.' + cur[14:]

		condition = r"VDB:(ID='" + real_id + r"')"
		cnName = '检索式:复合文本=' + '(' + keywords + ')'
		srcEnName = 'SearchStatement:复合文本=' + '(' + keywords + ')'


		print real_id

		data_cur = {
			'viewQC.viewLiteraQCList[0].srcCnName':cnName,
			'viewQC.viewLiteraQCList[0].srcEnName':srcEnName,
			'viewQC.viewLiteraQCList[0].searchStrategy':'',
			'viewQC.viewLiteraQCList[0].searchCondition.executableSearchExp':condition,
			'viewQC.viewLiteraQCList[0].searchCondition.sortFields':'-APD,+PD',
			'viewQC.needSearch':'true',
			'viewQC.type':'SEARCH',
			'wee.bizlog.modulelevel':'0200604'
		}


		show = s.post(show_list,data = data_cur,cookies=cookies).content

		tmp = re.search('literaList\[0\] = \{(.*?)\};',show,re.S)
		if tmp == None:
			break;

		idlist = re.findall('"(.*?)"',tmp.group(1).replace(' ',''),re.S)

		# 解析验证码
		vcode = get_verification_code(pic_mask)
		print vcode

		# 获取加密后的mask
		mask_data = {
			'':'',
			'wee.bizlog.modulelevel':'02016',
			'mask':vcode
		}
		kao = s.post(mask_check_url,data=mask_data,cookies=cookies).content
		#{"downloadCount":2,"downloadItems":null,"mask":"1a75026a-5138-4460-a35e-5ef60258d1d0","pass":true,"sid":null}
		mask_jm = re.search(r'"mask":"(.*?)"',kao,re.S).group(1)
		#print mask_jm

		data_down = {
			'wee.bizlog.modulelevel':'02016',
			'checkItems':'abstractCheck',
			'__checkbox_checkItems':'abstractCheck',
			'checkItems':'TIVIEW',
			'checkItems':'APO',
			'checkItems':'APD',
			'checkItems':'PN',
			'checkItems':'PD',
			'checkItems':'ICST',
			'checkItems':'PAVIEW',
			'checkItems':'INVIEW',
			'checkItems':'PR',
			'checkItems':'ABVIEW',
			'checkItems':'ABSIMG',
			'idList[0].id':idlist[0],
			'idList[0].pn':idlist[3],
			'idList[0].an':idlist[2],
			'idList[0].lang':idlist[4],
			'checkItems':'fullTextCheck',
			'__checkbox_checkItems':'fullTextCheck',
			'checkItems':'fullImageCheck',
			'__checkbox_checkItems':'fullImageCheck',
			'mask':mask_jm
		}


		down_page = s.post(download_url,data=data_down,headers=down_head,cookies=cookies).content

		open( cur + ".zip" ,"wb").write(down_page)

	kao_data = {
		"resultPagination.limit":"10",
		"resultPagination.sumLimit":"10",
		"resultPagination.start":cnt,
		"resultPagination.totalCount":total,
		"searchCondition.searchType":"Sino_foreign",
		"searchCondition.dbId":"",
		"searchCondition.extendInfo['MODE']":"MODE_GENERAL",
		"searchCondition.searchExp":keywords,
		"wee.bizlog.modulelevel":"0200101",
		"searchCondition.executableSearchExp":executableSearchExp,
		"searchCondition.literatureSF":literatureSF,
		"searchCondition.strategy":"",
		"searchCondition.searchKeywords":"",
		"searchCondition.searchKeywords":keywords
	}
	result = s.post(show_page,data=kao_data,cookies=cookies).content
	print "next page"
	all_result = re.findall('javascript:viewLitera_search\(\'.*?\',\'(.*?)\',\'single\'\)',result,re.S)
