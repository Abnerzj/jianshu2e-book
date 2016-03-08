# -*- coding: utf-8 -*-
from debug import Debug
from src.tools.type import Type


class DB(object):
    u"""
    存放常用的 SQL 代码
    """
    cursor = None
    conn = None

    @staticmethod
    def set_conn(conn):
        DB.conn = conn
        DB.conn.text_factory = str     # 将text返回为bytestrings
        DB.cursor = conn.cursor()
        return

    @staticmethod
    def execute(sql):
        return DB.cursor.execute(sql)

    @staticmethod
    def commit():
        return DB.cursor.commit()

    @staticmethod
    def save(data={}, table_name=''):
        sql = "replace into {table_name} ({columns}) values ({items})".format(table_name=table_name,
                                                                              columns=','.join(data.keys()),
                                                                              items=(',?' * len(data.keys()))[1:])
        # Debug.logger.debug(sql)
        DB.cursor.execute(sql, tuple(data.values()))
        # Debug.logger.info("tuple?????" + str(tuple(data.values())))
        return

    @staticmethod
    def commit():
        DB.conn.commit()
        return

    @staticmethod
    def get_result_list(sql):
        Debug.logger.debug(sql)
        result = DB.cursor.execute(sql).fetchall()
        return result

    @staticmethod
    def get_result(sql):
        result = DB.cursor.execute(sql).fetchone()
        return result

    @staticmethod
    def wrap(kind, result=()):
        u"""
        将筛选出的列表按SQL名组装为字典对象
        :param kind:
        :param result:
        :return:
        """
        template = {
            Type.jianshu_info: (
                'creator_id', 'creator_hash', 'creator_name', 'creator_sign',
                'creator_logo', 'description', 'article_num', 'follower'
            ),
            Type.jianshu_article: (                # 这里把article_id 和author_id对换一下,不然会出错???TODO
                'article_id', 'author_hash', 'author_name', 'author_sign',
                'author_id', 'href', 'title', 'content', 'comment', 'publish_date'
            )
        }
        return {k: v for (k, v) in zip(template[kind], result)}
