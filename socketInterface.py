from aiohttp import web
import socketio

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)


async def index(request):
    with open('index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')


@sio.on('renderFrame')
async def print_message(sid, message):
    print("Connected via Socket ID: ", sid)
    print(message)
    await sio.emit('response', '')

app.router.add_get('/', index)

if __name__ == '__main__':
    web.run_app(app)