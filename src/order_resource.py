import pymysql

import os


class OrderResource:

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

        sql = "SELECT * FROM coms6156_sprint1_microservice2.order_table where orderID=%s";
        conn = OrderResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, args=key)
        result = cur.fetchone()

        return result

    @staticmethod
    def get_count_by_key(key):
        sql = "SELECT COUNT(*) FROM coms6156_sprint1_microservice2.order_table where orderID=%s";
        conn = OrderResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, args=key)
        result = cur.fetchone()

        return result

    @staticmethod
    def add(order):
        placeholder = ", ".join(["%s"] * len(order))
        sql = "insert into {table} ({columns}) values ({values});".format(table='coms6156_sprint1_microservice2.order_table',
                                                                             columns=",".join(order.keys()),
                                                                             values=placeholder)
        print(sql)
        conn = OrderResource._get_connection()
        cur = conn.cursor()
        res =cur.execute(sql, list(order.values()))
        result = cur.fetchone()

        return res

    @staticmethod
    def update(order):
        sql = "update  coms6156_sprint1_microservice2.order_table set shopID=%s, productID=%s, date=%s, num=%s where orderID=%s"
        conn = OrderResource._get_connection()
        cur = conn.cursor()
        res =cur.execute(sql, [order['shopID'],order['productID'],order['date'],order['num'],order['orderID']])
        result = cur.fetchone()

        return res

    @staticmethod
    def delete_by_key(key):

        sql = "Delete FROM coms6156_sprint1_microservice2.order_table where orderID=%s"
        conn = OrderResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, args=key)
        result = cur.fetchone()

        return res