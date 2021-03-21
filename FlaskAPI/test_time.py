import time

year = (time.localtime(time.time()).tm_year)
month = (time.localtime(time.time()).tm_mon)
day = (time.localtime(time.time()).tm_mday)

current_time = (str)(year)+"."+(str)(month)+"."+(str)(day)
print(current_time)