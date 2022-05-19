# import datetime
# a = datetime.date("2022-05-19 09:28:52.852002")
# b = datetime.datetime.now()
# print(b-a)

# print(datetime.datetime.now())
import time

TIMER_TIMER = 0

while True:
    TIMER_TIMER += 1
    time.sleep(1)
    print(TIMER_TIMER)