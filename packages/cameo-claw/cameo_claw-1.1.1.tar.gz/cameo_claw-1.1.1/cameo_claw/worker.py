import requests
import time
import os
import worker2

while True:
    print(__file__)
    # r = requests.get('http://localhost:20419/api/get_tasks/?token=123')
    # exec(r.text)
    worker2.w2()
    time.sleep(3)
