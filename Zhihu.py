# coding:utf8
from __future__ import print_function
from zhihu_oauth import *
import requests
import re
from pymongo import MongoClient
import sys
import json
import threading
import time
from lxml import etree


def getTopics(t):
	# print("saveTopic")
	try:
		if db.Topics.find_one({"id" : str(t.id)}):
			return t.id
		else:
			tpc = {
				"id" : t.id,
				"name" : t.name
			}
			db.Topics.insert(tpc)
			print("S : add Topic "+ t.name)
			#map(savePeople,list(p.followers)) # loop?
	except Exception as e:
		print("Error in saveTopic")
		print(e)
	return t.id

def getName(o):
	if o:
		# rtn = json.dumps(o)
		# print(o)
		return o.name
	else: 
		return ""

def getEduSchool(o):
	if o:
		rtn = []
		for education in o : 
			# print("getEduSchool")
			# print(o[0])
			if 'school' in education:
				rtn.append(education.school.name)
		return rtn
	else: 
		return ""
 
def getEduMajor(o):
	if o:
		rtn = []
		for education in o : 
			# print("getEduMajor")
			# print(o[0])
			if 'major' in education:
				rtn.append(education.major.name)
		return rtn
	else: 
		return ""

def getBusiName(o):
	if o:
		# rtn = []
		# if "people" in o:
		rtn = o.name
		return rtn
	else: 
		return ""

def getEmpJob(o):
	if o:
		rtn = []
		for employment in o : 
			# print("getEmpJob")
			# print(o[0])
			if 'job' in employment:
				rtn.append(employment.job.name)
		return rtn
	else: 
		return ""

def getEmpComp(o):
	if o:
		rtn = []
		for employment in o : 
			# print("getEmpComp")
			# print(o[0])
			if 'company' in employment:
				rtn.append(employment.company.name)
		return rtn
	else: 
		return ""

def getLoca(o):
	if o:
		rtn = []
		for location in o : 
			# print("getLoca")
			# print(o[0])
			rtn.append(location.name)
		return rtn
	else: 
		return ""

def getFoId(p):
	savePeople(p)
	return p.id

def saveQuestion(q):
	try:
		if db.Questions.find_one({"id" : str(q.id)}):
			return q.id
		else:
			qst = {
				"id" : q.id,
				"title" : q.title,
				"followers" : list(map(savePeople,list(q.followers))),
				"topics" : list(map(getTopics,list(q.topics))),
			}
			print("S : add Question "+ q.title)
			db.Questions.insert(qst)
	except Exception as e:
		print("Error in saveQuestion")
		print(e)
	return q.id


def savePeople(p):
	try:
		if db.People.find_one({"id" : str(p.id)}):
			return p.id
		elif p is ANONYMOUS:
			return p.id
		elif p.over:
			print("get User Over : " + p.over_reason)
			return ""
		else:
			ppl = {
				"id" : p.id,
				"name" : p.name,
				"description" : p.description,
				"email" : p.email,
				"educations_school" : getEduSchool(p.educations),
				"educations_major" : getEduMajor(p.educations),
				"business" : getBusiName(p.business),
				"employments_job" : getEmpJob(p.employments),
				"employments_company" : getEmpComp(p.employments),
				"gender" : p.gender,
				"locations" : getLoca(p.locations),
				"questions" : list(map(saveQuestion,list(p.questions))),
				"followings" : list(map(getFoId,list(p.followings))),
				"following_topics" : list(map(getTopics,list(p.following_topics))),
			}
			db.People.insert(ppl)
			print("S : add People "+ p.name)
			#map(savePeople,list(p.followers)) # loop?
	except Exception as e:
		print("Error in savePeople")
		print(e)
	return p.id

def main():
	req = requests.Session()
	index_url = 'https://www.zhihu.com/explore'
	while True:
		try:
			# index_html = req.get(index_url, headers=headers, timeout=35)
			index_html = req.get('https://www.zhihu.com/explore/recommendations', headers=headers, timeout=35)
			# xsrf = etree.HTML(index_html.text).xpath("/html/body/input[@name='_xsrf']")[0].attrib['value']
			# rcmd = req.post('https://www.zhihu.com/node/ExploreRecommendListV2', headers=headers, timeout=35, params={'method':'next','params':{"limit":20,"offset":40}}, cookies=req.cookies)
			# rst=re.findall("/question/([0-9]+)/answer/[0-9]+",index_html.text)
			# rst=re.findall("question\\/([0-9]+)\\/answer\\/[0-9]+", rcmd.text)
			# print(rst)
			# xsrf = etree.HTML(index_html.text).xpath("//input[@name='_xsrf']")[0].attrib['value']
			# print(xsrf)
			# headers['X-Xsrftoken'] = xsrf
			# rcmd = req.post('http://www.zhihu.com/node/ExploreRecommendListV2', headers=headers, timeout=35, params={'method':'next','params':"%7B%22limit%22%3A20%2C%22offset%22%3A40%7D"})
			rst=re.findall("question/([0-9]+)/answer/[0-9]+", index_html.text)
			break
		except Exception as err:
			# 出现异常重试
			print("获取页面失败，正在重试......")
			print(err)
			time.sleep(5)
	i = 0
	thd = []
	for questionid in rst:
		i = i + 1
		q = client.question(int(questionid))
		# saveQuestion(q)
		# thread.start_new_thread(saveQuestion, (q,))
		t = threading.Thread(target=saveQuestion,args=(q,))
		thd.append(t)
		# print(q.answers.author)
		# print(q.answers.)
	return thd


if __name__ == '__main__':
	# reload(sys)
	# sys.setdefaultencoding('utf8')  
	client = ZhihuClient()

	headers = {
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
		"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
		"Upgrade-Insecure-Requests": "1",
		"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
		"Pragma": "no-cache",
		"Accept-Encoding": "gzip, deflate, br",
		"Connection":"keep-alive"
	}

	un = raw_input("UN:")
	pw = raw_input("PW:")
	try:
		print(client.login(un, pw))
	except NeedCaptchaException:
		# 保存验证码并提示输入，重新登录
		with open('a.gif', 'wb') as f:
			f.write(client.get_captcha())
		captcha = raw_input('please input captcha:')
		print(client.login(un, pw, captcha))

	try :
		mongo = MongoClient('localhost', 27017)
		db = mongo.Zhihu
	except Exception as e:
		print(e)
		print("Error in Mongo connection")
		exit()

	maxthreads=400
	n = 0
	# while True:
	# 	try:
	# 		threadsList = main()
	# 		if threading.activeCount() < maxthreads:
	# 			for t in threadsList:
	# 				t.setDaemon(True)
	# 				t.start()
	# 				n = n+1
	# 				print("Start Thread " + str(n))
	# 	except Exception as e:
	# 		print("Error in Thread")
	# 		print(e)
	# 	pass
	threadsList = main()
	for t in threadsList:
		t.setDaemon(True)
		t.start()
		n = n+1
		print("Start Thread " + str(n))
	while True:
		time.sleep(5)