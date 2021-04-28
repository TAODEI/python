import time
x = 0
while 1:    
    if x == 0:
        ti = int(time.time())
        x = 1
    tim = 120 + ti -int(time.time())
    print(tim)
    