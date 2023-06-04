import time
date_format = '%Y-%m-%d'
a=time.strptime('2022-11-7',date_format)

print(a.tm_year,a.tm_mon,a.tm_mday,a.tm_yday,a.tm_wday)