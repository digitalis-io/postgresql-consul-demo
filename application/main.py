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
        self.conn.set_session(autocommit=True)

    def connected_to(self):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT inet_server_addr(), CASE WHEN pg_is_in_recovery() THEN 'replica' ELSE 'primary' END")
            res = cur.fetchall()
            cur.close()
            return res[0]
        except Exception as e:
            logging.error(e)
            return (None, None)


db = DB()

while True:
    db_ip, role = db.connected_to()
    msg = f"I'm connected to {db_ip} and it's {role}"
    logging.info(msg)
    time.sleep(1)
