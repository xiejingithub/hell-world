# -*- coding: utf-8 -*-
import MySQLdb
from twisted.enterprise import adbapi
import codecs
import MySQLdb.cursors

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ZhilianzhaopinPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host = settings["MYSQL_HOST"],
            db = settings["MYSQL_DBNAME"],
            user = settings["MYSQL_USER"],
            passwd = settings["MYSQL_PASSWORD"],
            port = settings['PORT'],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)

        return cls(dbpool)

    def process_item(self, item, spider):
        #使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)


    def do_insert(self, cursor, item):
        #执行具体的插入
        #根据不同的item 构建不同的sql语句并插入到mysql中
        insert_sql = """
            insert into zhilian(url, title, company, salary_min, salary_max, start_date, experience, count, site, nature, edu, type)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (item["url"], item["title"], item["company"], item["salary_min"], item['salary_max'],
                                         item['start_date'], item['experience'], item['count'], item['site'], item['nature'],
                                         item['edu'], item['type'])
        cursor.execute(insert_sql, params)


class MysqlPipeline(object):
    #采用同步的机制写入mysql
    def __init__(self):
        self.conn = MySQLdb.connect('localhost', 'root', '', 'article_spider', charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
            insert into zhilian(url, title, company, salary_min, salary_max, start_date, experience, count, site, nature, edu, type)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(insert_sql, (item["url"], item["title"], item["company"], item["salary_min"], item['salary_max'],
                                         item['start_date'], item['experience'], item['count'], item['site'], item['nature'],
                                         item['edu'], item['type']))
        self.conn.commit()


