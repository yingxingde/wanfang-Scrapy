# coding:utf8
import random
import base64
import requests
# from settings import PROXIES

class ProxyMiddleware(object):
	# def process_request(self, request, spider):
	# 	#获取之前验证一下ip是否可用
	# 	# proxy = ''
	# 	# while(True):
	# 	# 	proxy = PROXIES[random.randint(0, len(PROXIES))-1]
	# 	# 	if self.test_useful(proxy):
	# 	# 		break
	# 	# request.meta['proxy'] = "http://" +proxy
    #
	# 	proxy = PROXIES[random.randint(0, len(PROXIES))-1]
	# 	request.meta['proxy'] = "http://"+proxy



	def test_useful(self, proxy):
		print '[INFO] Testing proxy ', proxy
		try:
			proxies = {'http': proxy}
			requests.get('http://www.baidu.com', proxies=proxies, timeout=20)
			print 'IP OK!'
			return True
		except Exception, e:
			print e
			return False
