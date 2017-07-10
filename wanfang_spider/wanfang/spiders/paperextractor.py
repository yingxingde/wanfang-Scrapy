# coding: utf-8

import scrapy
from time import sleep
import time
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from wanfang.settings import *
from wanfang.items import WanfangItem

def write_log(a,b):
	with open('log.txt', 'a') as filer:
		line = '{0}: {1} {2}\n'.format(time.asctime(), a, b)
		filer.write(line)

def write_url(url):
	with open('passed_url.txt', 'a') as filer:
		line = '{0}: {1}\n'.format(time.asctime(), url)
		filer.write(line)

# 如果网络波动,网断了则重连
def mysql_reconnect():
	while(True):
		try:
			if(db.ping(reconnect=True)==None):
				break
		except Exception, e:
			pass

class WanfangSpider(scrapy.Spider):
	url_used = list()
	url_crawled = list()
	name = 'wanfang'
	allowed_domains = [r'med.wanfangdata.com.cn']
	start_urls = [
		r'http://med.wanfangdata.com.cn/Periodical/Subject?class=R1'
	]
	service_args = ['--load-images=false', '--disk-cache=true']
	# service_args = ['--load-images=false', '--disk-cache=true', '--proxy=127.0.0.1:9050', '--proxy-type=socks5']
	driver = webdriver.PhantomJS(service_args= service_args)
	website_possible_httpstatus_list = [403]
	handle_httpstatus_list = [403]
	# driver = webdriver.Chrome()
	# rules = [
	# 	# Rule(LinkExtractor(allow=("http://med\.wanfangdata\.com\.cn/Periodical/Subject\?class=R\d")), follow=True),
	# 	Rule(LinkExtractor(allow=("http://med\.wanfangdata\.com\.cn/Periodical/.*")), follow=True),
	# 	Rule(LinkExtractor(allow=("http://med\.wanfangdata\.com\.cn/Paper/Detail/PeriodicalPaper_.*")), callback='parse_getss', follow=True)
	#
	# ]
	# wait_time = [10,8,12,9,10,10,15]
	wait_time = [5,6,5,5,7,6,5]
	waits_time = [1,2,1,0.5,1,0.5,2]
	begin_time = time.time()
	def parse(self, response):
		responseUrl = response.url
		# 这批url是需要点击之后还是在主节点A
		links = LinkExtractor(allow=("http://med\.wanfangdata\.com\.cn/Periodical/Subject\?class=\w*(($)|(&p=\d*$))"
									 )).extract_links(response)
		link_urls = [x.url for x in links]
		for url in link_urls:
			# 判断该网站是否已经爬过
			if url in self.url_used:
				# sleep(1)
				continue
			self.url_used.append(url)
			# sleep(1)
			yield  scrapy.Request(url=url, callback=self.parse_again)
		# 这批url点击之后进入期刊节点B
		links_next = LinkExtractor(allow=("http://med\.wanfangdata\.com\.cn/Periodical/\w*$"
									 )).extract_links(response)
		link_urls_next = [x.url for x in links_next]
		for url in link_urls_next:
			# 判断该网站是否已经爬过
			if url in self.url_used:
				# sleep(1)
				continue
			self.url_used.append(url)
			# sleep(1)
			yield  scrapy.Request(url=url, callback=self.parse_getss)

	# 主节点函数
	def parse_again(self, response):
		sleep(self.waits_time[np.random.randint(7)])
		responseUrl = response.url
		# 这批url是需要点击之后还是在主节点A
		links = LinkExtractor(allow=("http://med\.wanfangdata\.com\.cn/Periodical/Subject\?class=\w*(($)|(&p=\d*$))"
									 )).extract_links(response)
		link_urls = [x.url for x in links]
		for url in link_urls:
			# 判断该网站是否已经爬过
			if url in self.url_used:
				# sleep(1)
				continue
			self.url_used.append(url)
			# sleep(1)
			yield  scrapy.Request(url=url, callback=self.parse_again)
		# 这批url点击之后进入期刊节点B
		links_next = LinkExtractor(allow=("http://med\.wanfangdata\.com\.cn/Periodical/\w*$"
									 )).extract_links(response)
		link_urls_next = [x.url for x in links_next]
		for url in link_urls_next:
			# 判断该网站是否已经爬过
			if url in self.url_used:
				# sleep(1)
				continue
			self.url_used.append(url)
			# sleep(1)
			yield  scrapy.Request(url=url, callback=self.parse_getss)

	# 期刊节点函数
	def parse_getss(self, response):
		sleep(self.waits_time[np.random.randint(7)])
		responseUrl = response.url
		# 途径网站继续follow
		links = LinkExtractor(allow=("http://med\.wanfangdata\.com\.cn/Periodical/.*")).extract_links(response)
		link_urls = [x.url for x in links]
		for url in link_urls:
			# 判断该网站是否已经爬过
			if url in self.url_used:
				# sleep(1)
				continue
			self.url_used.append(url)
			# sleep(1)
			yield  scrapy.Request(url=url, callback=self.parse_getss)
		links_paper = LinkExtractor(allow=("http://med\.wanfangdata\.com\.cn/Paper/Detail/PeriodicalPaper_.*")).extract_links(response)
		link_urls_paper = [x.url for x in links_paper]
		for url in link_urls_paper:
			# 判断该paper是否爬过
			# sleep(1)
			if url in self.url_crawled:
				continue
			sql = "select * from wanfang where url='{0}' limit 1".format(url)
			sql_result = 0
			try:
				sql_result = cursor.execute(sql)
			except Exception ,e:
				mysql_reconnect()
				sql_result = cursor.execute(sql)
			if sql_result == 1:
				continue
			else:
				# sleep(1)
				self.url_crawled.append(url)
				yield scrapy.Request(url=url, callback=self.parse_paper)

	a = 0
	b = 0
	def parse_paper(self, response):
		if (time.time()-self.begin_time)>=2000:
			self.begin_time = time.time()
			try:
				self.driver.quit()
			except Exception, e:
				print e
			sleep(10)
			self.driver = webdriver.PhantomJS(service_args= self.service_args)
			sleep(3)
		pageurl = response.url
		self.driver.get(pageurl)
		xpaths = ["//h3/a[@id='AA1']", "//h3/a[@id='AA2']", "//h3/a[@id='AA5']",
				  "//h3/a[@id='AA6']", "//h3/a[@id='AA7']", "//h3/a[@id='AA8']"]
		# prexpaths = ['//ul[@id="Ul1"]/li|//ul[@id="Ul1"]/text()', '//ul[@id="Ul2"]/li|//ul[@id="Ul2"]/text()',
		# 			 '//ul[@id="Ul5"]/li|//ul[@id="Ul5"]/text()', '//ul[@id="Ul7"]/li|//ul[@id="Ul7"]/text()',
		# 			 '//ul[@id="Ul6"]/li|//ul[@id="Ul6"]/text()', '//ul[@id="Ul8"]/li|//ul[@id="Ul8"]/text()']
		prexpaths = [u'//ul[@id="Ul1"]/li | //ul[@id="Ul1" and contains(text(), "本文无")]',
					 u'//ul[@id="Ul2"]/li | //ul[@id="Ul2" and contains(text(), "本文无")]',
					 u'//ul[@id="Ul5"]/li | //ul[@id="Ul5" and contains(text(), "没有")]',
					 u'//ul[@id="Ul7"]/li | //ul[@id="Ul7" and contains(text(), "没有")]',
					 u'//ul[@id="Ul6"]/li | //ul[@id="Ul6" and contains(text(), "没有")]',
					 u'//ul[@id="Ul8"]/li | //ul[@id="Ul8" and contains(text(), "没有")]']
		# prexpaths = [u'//ul[@id="Ul1" | //ul[@id="Ul1" and text()=""]', u'//ul[@id="Ul2"]',
		# 			 u'//ul[@id="Ul5"]', u'//ul[@id="Ul7"]',
		# 			 u'//ul[@id="Ul6"]', u'//ul[@id="Ul8"]']
		# 点击
		for myxpath in xpaths:
			if len(response.xpath(myxpath)) != 0:
				self.driver.find_element_by_xpath(myxpath).click()
				sleep(1)
		# 等待显示
		sleep(self.wait_time[np.random.randint(7)])

		self.b += 1
		for i in xrange(len(xpaths)):
			if len(response.xpath(xpaths[i])) != 0:
				try:
					# # 再次点击
					# self.driver.find_element_by_xpath(xpaths[i]).click()
					# sleep(1)
					element = WebDriverWait(self.driver, 30).until(
						EC.presence_of_element_located((By.XPATH, prexpaths[i])))
				except Exception, e:
					self.a += 1
					write_log(self.a, self.b)
					print '还没加载完毕,无法正常显示'



		# 如果存在的xpath都没正常显示,证明被ban了,换个ip重新加载
		banIf = True
		passIf = False
		for i in xrange(len(xpaths)):
			if len(response.xpath(xpaths[i])) != 0:
				try:
					self.driver.find_element_by_xpath(prexpaths[i])
					banIf = False
				except Exception, e:
					passIf = True
				else:
					banIf = False

		if banIf:
			req = response.request
			req.meta["change_proxy"] = True
			return req
		if passIf and not banIf:
			write_url(pageurl)

		new_response = scrapy.Selector(text = self.driver.page_source)

		title = ''
		if len(new_response.xpath("//h4/text()")) != 0:
			title = ''+new_response.xpath("//h4/text()").extract()[0]
		click = ''
		if len(new_response.xpath("//span[@id='artcileClickCount']/text()")) != 0:
			click = (new_response.xpath("//span[@id='artcileClickCount']/text()").extract()[0]).split(':')[1]
		download = ''
		if len(new_response.xpath("//span[@id='artcileDownloadCount']/text()"))!= 0:
			download = (new_response.xpath("//span[@id='artcileDownloadCount']/text()").extract()[0]).split(':')[1]
		des = ''
		if len(new_response.xpath("//p[@class='prvTXT']/text()")) != 0:
			des = ''+new_response.xpath("//p[@class='prvTXT']/text()").extract()[0]
		zuozhe = ''
		if len(new_response.xpath(u'//th[text()="作 者"]')) != 0:
			zuozhe = ''.join([x.strip() for x in (new_response.xpath(u'//th[text()="作 者"]')).xpath('../td/a/text()').extract()])
			if len(zuozhe) == 0:
				zuozhe = ''.join([x.strip() for x in (new_response.xpath(u'//th[text()="作 者"]')).xpath('../td/text()').extract()])
		kanming = ''
		if len(new_response.xpath(u'//th[text()="刊 名"]')) != 0:
			kanming = ''.join([x.strip()+',' for x in (new_response.xpath(u'//th[text()="刊 名"]')).xpath("../td/a/text()").extract()])
		yingwenkanming = ''
		if len(new_response.xpath(u'//th[text()="英文期刊名"]')) != 0:
			yingwenkanming = "".join([x.strip() for x in (new_response.xpath(u'//th[text()="英文期刊名"]')).xpath('../td/text()').extract()])
		keyword = ''
		if len(new_response.xpath(u'//th[text()="关键词"]')) != 0:
			keyword = ''.join([x.strip()+',' for x in (new_response.xpath(u'//th[text()="关键词"]')).xpath('../td/a/text()').extract()])
		lanmuname = ''
		if len(new_response.xpath(u'//th[text()="栏目名称"]')) != 0:
			lanmuname = ''.join([x.strip() for x in (new_response.xpath(u'//th[text()="栏目名称"]')).xpath('../td/text()').extract()])
		doi = ''
		if len(new_response.xpath(u'//th[text()="DOI号"]')) != 0:
			doi = ''.join([x.strip() for x in (new_response.xpath(u'//th[text()="DOI号"]')).xpath('../td/a/text()').extract()])

		cankao = ''
		if len(new_response.xpath('//ul[@id="Ul1"]/li')) != 0:
			cankao_content = new_response.xpath('//ul[@id="Ul1"]/li')
			for li in cankao_content:
				cankao_author = li.xpath('./text()').extract()
				cankao_journal = li.xpath('./a/text()').extract()
				item1 = ''
				item2 = ''
				item3 = ''
				if len(cankao_author) == 2:
					item1 = cankao_author[0].strip('\r\n []1234567890.').strip()
					item3 = ''.join([i.strip() for i in cankao_author[1].split('\n')]).strip().strip('.')
					if len(cankao_journal):
						item2 = (cankao_journal[0].strip('\r\n []1234567890.').strip())
					item = ''+item1+'|'+item2+'|'+item3+';'
					cankao += item
				elif len(cankao_author) == 3:
					item1 = cankao_author[0].strip('\r\n []1234567890.').strip()
					item3 = ''.join([i.strip() for i in cankao_author[2].split('\n')]).strip().strip('.')
					if len(cankao_journal):
						item2 = (cankao_journal[0].strip('\r\n []1234567890.').strip())
					item = ''+item1+'|'+item2+'|'+item3+';'
					cankao += item
		else:
			if len(new_response.xpath('//ul[@id="Ul1"]/text()')) != 0:
				cankao = new_response.xpath('//ul[@id="Ul1"]/text()').extract()[0]+';'

			# cankao = "//".join(c.xpath('./text()').extract()[0].strip('\r\n []1234567890').strip() + '|' + c.xpath('./a/text()').extract()[0].strip('\r\n []1234567890').strip() + '|' + "".join(c.xpath('./text()').extract()[2].split()).strip('.') for c in new_response.xpath('//ul[@id="Ul1"]/li'))

		yizheng = ''
		if len(new_response.xpath('//ul[@id="Ul2"]/li')) != 0:
			yinzheng_content = new_response.xpath('//ul[@id="Ul2"]/li')
			for li in yinzheng_content:
				yinzheng_author = li.xpath('./text()').extract()
				yinzheng_journal = li.xpath('./a/text()').extract()
				item1 = ''
				item2 = ''
				item3 = ''
				if len(yinzheng_author) == 2:
					item1 = yinzheng_author[0].strip('\r\n []1234567890.').strip()
					item3 = ''.join([i.strip() for i in yinzheng_author[1].split('\n')]).strip().strip('.')
					if len(yinzheng_journal):
						item2 = (yinzheng_journal[0].strip('\r\n []1234567890.').strip())
					item = ''+item1+'|'+item2+'|'+item3+';'
					yizheng += item
				elif len(yinzheng_author) == 3:
					item1 = yinzheng_author[0].strip('\r\n []1234567890.').strip()
					item3 = ''.join([i.strip() for i in yinzheng_author[2].split('\n')]).strip().strip('.')
					if len(yinzheng_journal):
						item2 = (yinzheng_journal[0].strip('\r\n []1234567890.').strip())
					item = ''+item1+'|'+item2+'|'+item3+';'
					yizheng += item
		else:
			if len(new_response.xpath('//ul[@id="Ul2"]/text()')) != 0:
				yizheng = new_response.xpath('//ul[@id="Ul2"]/text()').extract()[0]+';'

			# yinzheng = ''.join(c.xpath('./text()').extract()[0].strip('\r\n []1234567890').strip() + '|' + c.xpath('./a/text()').extract()[0].strip('\r\n []1234567890').strip() + '|' + "".join(c.xpath('./text()').extract()[2].split()).strip('.') for c in new_response.xpath('//ul[@id="Ul2"]/li'))

		sswenxian = ''
		if len(new_response.xpath('//ul[@id="Ul5"]/li')) != 0:
			yinzheng_content = new_response.xpath('//ul[@id="Ul5"]/li')
			for li in yinzheng_content:
				yinzheng_author = li.xpath('./text()').extract()
				yinzheng_journal = li.xpath('./a/text()').extract()
				item1 = ''
				item2 = ''
				item3 = ''
				if len(yinzheng_author) == 2:
					item1 = yinzheng_author[0].strip('\r\n []1234567890.').strip()
					item3 = ''.join([i.strip() for i in yinzheng_author[1].split('\n')]).strip().strip('.')
					if len(yinzheng_journal):
						item2 = (yinzheng_journal[0].strip('\r\n []1234567890.').strip())
					item = ''+item1+'|'+item2+'|'+item3+';'
					sswenxian += item
				elif len(yinzheng_author) == 3:
					item1 = yinzheng_author[0].strip('\r\n []1234567890,').strip()
					item3 = ''.join([i.strip() for i in yinzheng_author[2].split('\n')]).strip().strip('.')
					if len(yinzheng_journal):
						item2 = (yinzheng_journal[0].strip('\r\n []1234567890.').strip())
					item = ''+item1+'|'+item2+'|'+item3+';'
					sswenxian += item
		else:
			if len(new_response.xpath('//ul[@id="Ul5"]/text()')) != 0:
				sswenxian = new_response.xpath('//ul[@id="Ul5"]/text()').extract()[0]+';'

		sswaiwen = ''
		if len(new_response.xpath('//ul[@id="Ul7"]/li')) != 0:
			yinzheng_content = new_response.xpath('//ul[@id="Ul7"]/li')
			for li in yinzheng_content:
				yinzheng_author = li.xpath('./text()').extract()
				yinzheng_journal = li.xpath('./a/text()').extract()
				item1 = ''
				item2 = ''
				item3 = ''
				if len(yinzheng_author) == 2:
					item1 = yinzheng_author[0].strip('\r\n []1234567890.').strip()
					item3 = ''.join([i.strip() for i in yinzheng_author[1].split('\n')]).strip().strip('.')
					if len(yinzheng_journal):
						item2 = (yinzheng_journal[0].strip('\r\n []1234567890.').strip())
					item = ''+item1+'|'+item2+'|'+item3+';'
					sswaiwen += item
				elif len(yinzheng_author) == 3:
					item1 = yinzheng_author[0].strip('\r\n []1234567890.').strip()
					item3 = ''.join([i.strip() for i in yinzheng_author[2].split('\n')]).strip().strip('.')
					if len(yinzheng_journal):
						item2 = (yinzheng_journal[0].strip('\r\n []1234567890.').strip())
					item = ''+item1+'|'+item2+'|'+item3+';'
					sswaiwen += item
		else:
			if len(new_response.xpath('//ul[@id="Ul7"]/text()')) != 0:
				sswaiwen = new_response.xpath('//ul[@id="Ul7"]/text()').extract()[0]+';'

		sshuiyi = ''
		if len(new_response.xpath('//ul[@id="Ul6"]/li')) != 0:
			yinzheng_content = new_response.xpath('//ul[@id="Ul6"]/li')
			for li in yinzheng_content:
				yinzheng_author = li.xpath('./text()').extract()
				yinzheng_journal = li.xpath('./a/text()').extract()
				item1 = ''
				item2 = ''
				item3 = ''
				if len(yinzheng_author) == 2:
					item1 = yinzheng_author[0].strip('\r\n []1234567890.').strip()
					item3 = ''.join([i.strip() for i in yinzheng_author[1].split('\n')]).strip().strip('.')
					if len(yinzheng_journal):
						item2 = (yinzheng_journal[0].strip('\r\n []1234567890.').strip())
					item = ''+item1+'|'+item2+'|'+item3+';'
					sshuiyi += item
				elif len(yinzheng_author) == 3:
					item1 = yinzheng_author[0].strip('\r\n []1234567890.').strip()
					item3 = ''.join([i.strip() for i in yinzheng_author[2].split('\n')]).strip().strip('.')
					if len(yinzheng_journal):
						item2 = (yinzheng_journal[0].strip('\r\n []1234567890.').strip())
					item = ''+item1+'|'+item2+'|'+item3+';'
					sshuiyi += item
		else:
			if len(new_response.xpath('//ul[@id="Ul6"]/text()')) != 0:
				sshuiyi = new_response.xpath('//ul[@id="Ul6"]/text()').extract()[0]+';'

		ssxuewei = ''
		if len(new_response.xpath('//ul[@id="Ul8"]/li')) != 0:
			yinzheng_content = new_response.xpath('//ul[@id="Ul8"]/li')
			for li in yinzheng_content:
				yinzheng_author = li.xpath('./text()').extract()
				yinzheng_journal = li.xpath('./a/text()').extract()
				item1 = ''
				item2 = ''
				item3 = ''
				if len(yinzheng_author) == 2:
					item1 = yinzheng_author[0].strip('\r\n []1234567890.').strip()
					item3 = ''.join([i.strip() for i in yinzheng_author[1].split('\n')]).strip().strip('.')
					if len(yinzheng_journal):
						item2 = (yinzheng_journal[0].strip('\r\n []1234567890.').strip())
					item = ''+item1+'|'+item2+'|'+item3+';'
					ssxuewei += item
				elif len(yinzheng_author) == 3:
					item1 = yinzheng_author[0].strip('\r\n []1234567890.').strip()
					item3 = ''.join([i.strip() for i in yinzheng_author[2].split('\n')]).strip().strip('.')
					if len(yinzheng_journal):
						item2 = (yinzheng_journal[0].strip('\r\n []1234567890.').strip())
					item = ''+item1+'|'+item2+'|'+item3+';'
					ssxuewei += item
		else:
			if len(new_response.xpath('//ul[@id="Ul8"]/text()')) != 0:
				ssxuewei = new_response.xpath('//ul[@id="Ul8"]/text()').extract()[0]+';'

		item = WanfangItem()
		item['url'] = pageurl.encode('utf8')
		item['title'] = title.encode('utf8')
		item['click'] = click.encode('utf8')
		item['down'] = download.encode('utf8')
		item['des'] = des.encode('utf8')
		item['zuozhe'] = zuozhe.encode('utf8')
		item['kanming'] = kanming[:-1].encode('utf8')
		item['yingwenkanming'] = yingwenkanming.encode('utf8')
		item['keyword'] = keyword[:-1].encode('utf8')
		item['lanmuname'] = lanmuname.encode('utf8')
		item['doi'] = doi.encode('utf8')
		item['cankao'] = cankao[:-1].encode('utf8')
		item['yinzheng'] = yizheng[:-1].encode('utf8')
		item['sswenxian'] = sswenxian[:-1].encode('utf8')
		item['sswaiwen'] = sswaiwen[:-1].encode('utf8')
		item['sshuiyi'] = sshuiyi[:-1].encode('utf8')
		item['ssxuewei'] = ssxuewei[:-1].encode('utf8')


		return item

