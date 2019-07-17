import redis 
import time
r = redis.Redis(host='localhost', port=6379, db=0)
# this is just jank buffer

index = 0
while(r.get(str(index))!= None):
    print(r.get(str(index)))
    if(r.get(str(index))) == None:
        time.sleep(5)
        continue
    r.delete(str(index))
    index+=1 
    time.sleep(5)
