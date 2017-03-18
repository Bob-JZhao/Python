# -*- coding:UTF-8 -*-
from urllib.request import urlopen
from bs4 import BeautifulSoup as bf
import re  # 正则表达式
import pymysql
import io  
import sys  
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') #改变标准输出的默认编码 

def conn_db():
    conn = pymysql.connect(host="127.0.0.1", user="root", password="111111", db="wiki", port=3306)
    cur = conn.cursor()
    return conn,cur
# 该方法执行sql语句
def exe_query(cur, sql):
    cur.execute(sql)
    return cur


resp = urlopen("https://en.wikipedia.org/wiki/Main_Page").read().decode('utf-8')
soup = bf(resp,'html.parser')
#print(resp)
listUrl = soup.findAll('a',href=re.compile('^/wiki/'))


try:

	conn,cur = conn_db()
	for url in listUrl:
		#print(url['href']) #此时会有。jdp 结尾的 需要过滤掉
		if not re.search ('\.(jpg|JPG)$',url['href']):
			print(url.get_text(),'<--->','https://en.wikipedia.org' + url['href'])
			# string 只能获取一个，get_text() 可以获取多个
			sql = "insert into urls (urlname,url) values ('"+url.get_text() +"','"+'https://en.wikipedia.org' + url['href']+"') "
			print(sql)
			cur.execute(sql)
	conn.commit()
finally:
	conn.close()








