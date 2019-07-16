from aiohttp import web
import socketio
from faceRecog import FacRecog

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)

async def index(request):
    with open('index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')

@sio.on('renderFrame')
async def print_message(sid, message):
    x = FacRecog()
    imageSX4 = x.getFoundFrame()
    imageSX4.encode('unicode_escape')
    print("Connected via Socket ID: ", sid)
    print(message)
    await sio.emit('response', imageSX4)

app.router.add_get('/', index)
if __name__ == '__main__':
    web.run_app(app)