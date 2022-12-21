import pymysql

import os


class ProductResource:

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

        sql = "SELECT * FROM coms6156_sprint1_microservice2.product where productID=%s";
        conn = ProductResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, args=key)
        result = cur.fetchone()

        return result

    @staticmethod
    def add(product):
        placeholder = ", ".join(["%s"] * len(product))
        sql = "insert into {table} ({columns}) values ({values});".format(table='coms6156_sprint1_microservice2.product',
                                                                          columns=",".join(product.keys()),
                                                                          values=placeholder)
        conn = ProductResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, list(product.values()))
        result = cur.fetchone()

        return res

    @staticmethod
    def update(product):
        sql = "update  coms6156_sprint1_microservice2.product set product_name=%s, price=%s where productID=%s"
        conn = ProductResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, [product['product_name'], product['price'], product['productID']])
        result = cur.fetchone()

        return res

    @staticmethod
    def delete_by_key(key):
        sql = "Delete FROM coms6156_sprint1_microservice2.product where productID=%s"
        conn = ProductResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, args=key)
        result = cur.fetchone()

        return res