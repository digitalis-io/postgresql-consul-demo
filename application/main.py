#!/usr/bin/env python3

import logging
import time
import psycopg2
import sys

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', stream=sys.stdout, level=logging.DEBUG)

class DB:

    def __init__(self):
        logging.info("Starting.")
        while True:
            try:
                self.connect()
                break
            except Exception as e:
                logging.error(e)
                time.sleep(2)

    def connect(self):
        logging.info('Connecting.')
        self.conn = psycopg2.connect("")

    def disconnect(self):
        logging.info('Disconnecting.')
        self.conn.close()

    def reconnect(self):
        while True:
            try:
                self.disconnect()
                self.connect()
                break
            except:
                logging.error("Connection failed. Retrying.")
                time.sleep(1)


    def connected_to(self):
        while True:
            try:
                cur = self.conn.cursor()
                cur.execute("SELECT inet_server_addr()")
                res = cur.fetchall()
                break
            except Exception as e:
                logging.error(e)
                logging.warning("Something went wrong. Reconnecting.")
                time.sleep(1)
                self.reconnect()
            finally:
                cur.close()
        return res[0][0]


db = DB()
db.connected_to()

while True:
    db_ip = db.connected_to()
    msg = "I'm connected to %s" % db_ip
    logging.info(msg)
    time.sleep(1)
