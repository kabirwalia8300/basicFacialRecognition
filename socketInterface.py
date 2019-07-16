from aiohttp import web
import socketio

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)

# we can define aiohttp endpoints just as we normally
# would with no change
async def index(request):
    with open('index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')

@sio.on('renderFrame')
async def print_message(sid, message):
    print("Connected via Socket ID: " , sid)
    print(message)
    await sio.emit('response', message[::-1])

app.router.add_get('/', index)

# We kick off our server
if __name__ == '__main__':
    web.run_app(app)