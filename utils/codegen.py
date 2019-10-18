import time
import base64
import random
import string

count = 0


def gen_code():
    global count
    count += 1
    return str(base64.b64encode((''.join(random.choices(string.ascii_uppercase + string.digits, k=4)) + str(count) + str(int(time.time()))).encode()).decode("utf-8"))[:-2]
