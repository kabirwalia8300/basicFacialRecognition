from aiohttp import web
import socketio
from faceRecog import FacRecog
import time
import redis
sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)
r = redis.Redis(host='localhost', port=6379, db=0)

async def index(request):
    with open('index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')

@sio.on('renderFrame')
async def print_message(sid, message):
    index = 0
    imageSX4 = ""
    print(message)
    while(True):
        imageSX4 = (r.get(index)).decode('utf-8')
        # imageSX4.encode('unicode_escape')
        print("Connected via Socket ID: ", sid)
        if(r.get(str(index))) == None:
            time.sleep(5)
            continue
        await sio.emit('response', imageSX4)
        print(message)
        r.delete(str(index))
        index+=1 
        time.sleep(5)
    
app.router.add_get('/', index)
if __name__ == '__main__':
    web.run_app(app)