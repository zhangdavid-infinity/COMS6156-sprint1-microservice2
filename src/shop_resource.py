import pymysql

import os


class ShopResource:

    def __int__(self):
        pass

    @staticmethod
    def _get_connection():
        usr = 'admin'
        pw = '1TDjlgyd'
        h = 'db6156.ceja91pylrkk.us-east-1.rds.amazonaws.com'

        conn = pymysql.connect(
            user=usr,
            password=pw,
            host=h,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        return conn

    @staticmethod
    def get_by_key(key):

        sql = "SELECT * FROM coms6156_sprint1_microservice2.shop where shopID=%s"
        conn = ShopResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, args=key)
        result = cur.fetchone()

        return result

    @staticmethod
    def add(shop):
        placeholder = ", ".join(["%s"] * len(shop))
        sql = "insert into {table} ({columns}) values ({values});".format(table='coms6156_sprint1_microservice2.shop',
                                                                             columns=",".join(shop.keys()),
                                                                             values=placeholder)
        print(sql)
        conn = ShopResource._get_connection()
        cur = conn.cursor()
        res =cur.execute(sql, list(shop.values()))
        result = cur.fetchone()

        return res

    def update(shop):
        placeholder = ", ".join(["%s"] * len(shop))
        sql = "update  coms6156_sprint1_microservice2.shop set name=%s, email=%s, address=%s, phone=%s where shopID=%s"
        print(sql)
        conn = ShopResource._get_connection()
        cur = conn.cursor()
        res =cur.execute(sql, [shop['name'],shop['email'],shop['address'],shop['phone'],shop['shopID']])
        result = cur.fetchone()

        return res

    @staticmethod
    def delete_by_key(key):

        sql = "Delete  FROM coms6156_sprint1_microservice2.shop where shopID=%s"
        conn = ShopResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, args=key)
        result = cur.fetchone()

        return res