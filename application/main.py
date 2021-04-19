
import time
#import psycopg2

while True:
  localtime = time.localtime()
  result = time.strftime("%I:%M:%S %p", localtime)
  print(result, flush=True)
  time.sleep(1)
