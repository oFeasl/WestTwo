import time

year=(time.localtime(time.time()).tm_year)
(time.localtime(time.time()).tm_mon)
(time.localtime(time.time()).tm_mday)

current_time = (str)(time.localtime(time.time()).tm_year)+"."+(str)(time.localtime(time.time()).tm_mon)+"."+(str)(time.localtime(time.time()).tm_mday)
print(current_time)