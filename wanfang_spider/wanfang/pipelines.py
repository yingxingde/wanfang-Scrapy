# -*- coding: utf8 -*-

from wanfang.settings import *

def mysql_reconnect():
    while(True):
        try:
            if(db.ping(reconnect=True)==None):
                break
        except Exception, e:
            pass

class WanfangPipeline(object):
    def process_item(self, item, spider):
        mysql = "insert ignore into wanfang(url, title, click, down, des, zuozhe, " \
				"kanming, yingwenkanming, keyword, lanmuname, doi, cankao, yinzheng, " \
				"sswenxian, sswaiwen, sshuiyi, ssxuewei)" \
				" VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        try:
            cursor.execute(mysql, (item['url'], item['title'], item['click'], item['down'],
							   item['des'], item['zuozhe'],item['kanming'],item['yingwenkanming'],
							   item['keyword'], item['lanmuname'], item['doi'],item['cankao'], item['yinzheng'],
							   item['sswenxian'], item['sswaiwen'],item['sshuiyi'],item['ssxuewei']))
        except Exception, e:
            mysql_reconnect()
            cursor.execute(mysql, (item['url'], item['title'], item['click'], item['down'],
							   item['des'], item['zuozhe'],item['kanming'],item['yingwenkanming'],
							   item['keyword'], item['lanmuname'], item['doi'],item['cankao'], item['yinzheng'],
							   item['sswenxian'], item['sswaiwen'],item['sshuiyi'],item['ssxuewei']))

        db.commit()
        return item
        # sql = "insert into wanfang(url, title, click, down, des, zuozhe, kanming, yingwenkanming, keyword, " \
			#   "lanmuname, doi, cankao, yinzheng, sswenxian, sswaiwen, sshuiyi, ssxuewei)" \
			#   " VALUES ('{0}', '{1}', {2}, {3}, '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}', '{11}'," \
			#   " '{12}', '{13}', '{14}', '{15}', '{16}')"\
        #           .format(item['url'], item['title'], item['click'], item['down'], item['des'], item['zuozhe'],
        #                   item['kanming'],item['yingwenkanming'],item['keyword'], item['lanmuname'], item['doi'],
        #                   item['cankao'], item['yinzheng'], item['sswenxian'], item['sswaiwen'],item['sshuiyi'],
        #                   item['ssxuewei'])
		#
        # print sql
        # cursor.execute(sql.decode('unicode_escape').encode('utf8'))


