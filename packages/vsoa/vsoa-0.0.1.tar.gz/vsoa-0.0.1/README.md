# Overview

VSOA is the abbreviation of Vehicle SOA presented by ACOINFO, VSOA provides a reliable, Real-Time SOA (Service Oriented Architecture) framework, this framework has multi-language and multi-environment implementation, developers can use this framework to build a distributed service model. 

VSOA includes the following features:
1. Support resource tagging of unified URL
1. Support URL matching subscribe and publish model
1. Support Real-Time Remote Procedure Call
1. Support parallel multiple command sequences
1. Support reliable and unreliable data publishing and datagram
1. Support multi-channel full-duplex high speed parallel data stream
1. Support network QoS control
1. Easily implement server fault-tolerant design
1. Supports multiple language bindings

VSOA is a dual-channel communication protocol, using both **TCP** and **UDP**, among which the API marked with `quick` uses the **UDP** channel. The quick channel is used for high-frequency data update channels. Due to the high data update frequency, the requirements for communication reliability are not strict. It should be noted that **UDP** channel cannot pass through NAT network, so please do not use quick channel in NAT network.

The total url and payload length of the VSOA data packet cannot exceed **256KBytes - 20Bytes** and **65507Bytes - 20Bytes** on quick channel, so if you need to send a large amount of data, you can use the VSOA data stream.

User can use the following code to import the `vsoa` module.
``` python
import vsoa
```

# VSOA Server Class
## vsoa.Server(info: dict | str = '', passwd: str = '', raw: bool = False)
+ `info` This server information.
+ `passwd` This server password.
+ `raw` Whether RPC and DATAGRAM `payload.param` automatically perform JSON parsing.
+ Returns: VSOA server object.

Create a VSOA server.

``` python
server = vsoa.Server('VSOA python server')
```

# VSOA Server Object
## server.clients() -> list[RemoteClient]
+ Returns: List of clients.

Get list of clients currently connected to this server.

``` python
for cli in server.clients():
	print(cli.id) # Print remote client ID
```

## server.address() -> tuple[str, int]
+ Returns: Server address tuple.

Get the server address currently bound to this server. Exception will be thrown when the server is not started.

``` python
addr, port = server.address()
```

## server.passwd(passwd: str = '')
+ `passwd` New password.

Set a new password for the server, `None` or `''` mean no password.

## server.publish(url: str, payload: vsoa.Payload | dict = None, quick: bool = False) -> bool
+ `url` Publish URL.
+ `payload` Payload
+ `quick` Whether to use quick mode.
+ Returns: Whether publish is successful.

Publish a message, all clients subscribed to this URL will receive this message. If a large number of high-frequency releases are required and delivery is not guaranteed, the `quick` parameter can be set to `True`.

The `payload` object contains the following members:
+ `param`: *{object | dict | list | str | bytes | bytearray}* Parameters of this RPC request. Optional.
+ `data` *{bytes | bytearray}* Data for this publish. Optional.

URL matching: URL uses `'/'` as a separator, for example: `'/a/b/c'`, if the client subscribes to `'/a/'`, the server publish `'/a'`, `'/a/b'` or `'/a/b/c'` message, the client will be received.

``` python
server.publish('/a/b/c')
server.publish('/a/b/c', { 'param': { 'hello': 'hello' } })
server.publish('/a/b/c', { 'param': { 'hello': 'hello' }, 'data': bytes([1, 2, 3]) })

# Or
server.publish('/a/b/c', vsoa.Payload({ 'hello': 'hello' }))
server.publish('/a/b/c', vsoa.Payload({ 'hello': 'hello' }, bytes([1, 2, 3])))
```

## server.is_subscribed(url: str) -> bool
+ `url` Publish URL.
+ Returns: Whether the specified URL is subscribed by clients.

Whether the specified URL is subscribed. When the return value is `True`, it means that the specified URL is subscribed by at least one client.

## server.command(url: str, wq: vsoa:WorkQueue = None) -> callable
+ `url` RPC command URL.
+ `wq` This command function runs in the specified workqueue.

Server RPC command entry registration decorator.

``` python
server = vsoa.Server('VSOA python server')

@server.command('/echo')
def echo(cli, request, payload):
	cli.reply(request.seqno, payload) # echo reply

server.run('0.0.0.0', 3005)
```

## server.sendtimeout(timeout: float)
+ `timeout` Send timeout.

Set send timeout, default is `0.1`. (100ms)

## server.run(addr: str, port: int, sslopt: dict = None)
+ `addr` Local address.
+ `port` Local port.
+ `sslopt` TLS connection options, Currently not supported.

Start the server and execute the event loop. This function does not return when no errors occur.

## server.onclient
+ On client connect / disconnect callback.

The server will call this function when the client connects and disconnects.

``` python
def onclient(cli, conn: bool):
	print('Client:', cli.id, 'connect:', conn)

server.onclient = onclient
```

## server.ondata
+ On client DATAGRAM data received callback.

The server will call this function when client DATAGRAM data received.

``` python
def ondata(cli, url: str, payload: vsoa.Payload, quick: bool):
	print('Client:' cli.id, 'DATARAM URL:', url, 'Payload:', dict(payload), 'Q:', quick)

server.ondata = ondata
```

## server.create_stream(onlink: callable, ondata: callable, timeout: float = 5.0) -> ServerStream
+ `onlink` Client stream connect / disconnect callback.
+ `ondata` Receive client stream data callback
+ `timeout` Wait for client connection timeout.

Create a stream to communicate with the client via stream. During normal communication, `onlink` will be called twice, once when the connection is successful and once when the connection is disconnected. When the stream wait times out, `onlink` will only be called once, and the `conn` parameter is `False`.

Server:
``` python
@server.command('/get_data')
def get_data(cli, request, payload):
	def onlink(stream, conn: bool):
		if conn:
			with open('file') as file:
				stream.send(file.read())

	def ondata(stream, data: bytes):
		print('Received:', len(data))

	stream = server.create_stream(onlink, ondata)
	cli.reply(request.seqno, tunid = stream.tunid)
```

Client:
``` python
client = vsoa.Client()
client.robot(...)

file = None
def onlink(stream, conn: bool):
	if conn:
		file = open('file')
	else:
		if file:
			file.close()
			file = None

def ondata(stream, data: bytes):
	file.write(data)

header, payload, _ = client.fetch('/get_data')
if header and header.tunid > 0
	stream = client.create_stream(header.tunid, onlink, ondata)
```

# VSOA Server Remote Client Object
## cli.id

Client ID getter. (`int` type)

## cli.authed

Whether this client has logged in. When a client correctly connects to the server (passed the password check), this property defaults to `True`. If the server requires other login authentication methods at this time, you can set this property to `False`, and the client will not be able to receive publish message from current server.

``` python
def onclient(cli, conn: bool):
	if conn:
		cli.authed = False # This client can not received publish message

server.onclient = onclient

@server.command('/user_auth')
def user_auth(cli, request, payload):
	if user_check:
		cli.authed = True # This client can received publish message
		cli.reply(...)
	else:
		cli.reply(...)
```

## cli.priority

This property is the client priority getter and setter, the valid range is `0` ~ `7`, `0` is the lowest.

## cli.close()

Close this client, the client object can no longer be used.

## cli.is_closed() -> bool

Determine whether the client has been closed. The reason for closure may be that the client actively closed, the developer called the `cli.close()` method, or the client connection was disconnected.

## cli.address() -> tuple[str, int]

Get client address.

``` python
def onclient(cli, conn: bool):
	if conn:
		print('Client:', cli.id, 'connected, address:', cli.address())
	else:
		print('Client:', cli.id, 'lost!')

server.onclient = onclient
```

## cli.is_subscribed(url: str) -> bool
+ `url` Publish URL.
+ Returns: Whether the specified URL is subscribed by this client.

Whether the specified URL is subscribed by this client.

## cli.reply(seqno: int, payload: vsoa.Payload | dict = None, status: int = 0, tunid: int = 0) -> bool
+ `seqno` Request seqno.
+ `payload` Payload to be replied.
+ `status` Replied `header.status`.
+ `tunid` If stream communication exists, the returned `stream.tunid`.

Client RPC call response. `status` values include:

Constant|Value|
---|:--:|
`vsoa.parser.VSOA_STATUS_SUCCESS`|0
`vsoa.parser.VSOA_STATUS_PASSWORD`|1
`vsoa.parser.VSOA_STATUS_ARGUMENTS`|2
`vsoa.parser.VSOA_STATUS_INVALID_URL`|3
`vsoa.parser.VSOA_STATUS_NO_RESPONDING`|4
`vsoa.parser.VSOA_STATUS_NO_PERMISSIONS`|5
`vsoa.parser.VSOA_STATUS_NO_MEMORY`|6

`0` means correct, `128` ~ `255` is the server custom error return value.

``` python
p = vsoa.Payload({ 'a': 1 }, bytes([1, 2, 3]))

# Same as:
p = vsoa.Payload()
p.param = { 'a': 1 }
p.data  = bytes([1, 2, 3])

# Same as:
p = { 'param': { 'a': 1 }, 'data': bytes([1, 2, 3]) }

cli.reply(request.seqno, p)
```

## cli.datagram(url: str, payload: vsoa.Payload | dict = None, quick: bool = False)
+ `url` Specified URL.
+ `payload` Payload to be send.
+ `quick` Whether to use quick channel.

Send a DATAGRAM data to the specified client.

``` python
p = vsoa.Payload(data = bytes([1, 2, 3, 4, 5]))
cli.datagram('/custom/data', p)
```

## cli.keepalive(idle: int)
+ `idle` Idle interval time, unit: seconds

Enable the client TCP keepalive function. If no reply is received for more than three times the `idle` time, it means the client is breakdown.

## cli.sendtimeout(timeout: float)
+ `timeout` Packet send timeout.

When sending packet to the client, the sending is considered failed if the `timeout` period is exceeded. Default: 0.5s.

## cli.onsubscribe

This function is called when the client subscribes to the URLs.

``` python
def onsubscribe(cli, url: str | list[str]):
	print('onsubscribe:', url)

cli.onsubscribe = onsubscribe
```

## cli.onunsubscribe

This function is called when the client unsubscribes to the URLs.

``` python
def onunsubscribe(cli, url: str | list[str]):
	print('onunsubscribe:', url)

cli.onunsubscribe = onunsubscribe
```

# Server Stream Object
## stream.tunid

Get stream tunnel ID.

## stream.connected

Check if stream is connected.

## stream.close()

Close this stream.

## stream.send(data: bytearray | bytes) -> int
+ `data` Data to be sent.
+ Returns: The actual data length sent

Send data using stream.

## stream.keepalive(idle: int)
+ `idle` Idle interval time, unit: seconds

Enable the stream TCP keepalive function. If no reply is received for more than three times the `idle` time, it means the stream is breakdown.

## stream.sendtimeout(timeout: float)
+ `timeout` Packet send timeout.

When sending packet to the stream, the sending is considered failed if the `timeout` period is exceeded. Default: block until ready to send.

# VSOA Client Class
## vsoa.Client(raw: bool = False)
+ `raw` Whether publish, RPC and DATAGRAM `payload.param` automatically perform JSON parsing.
+ Returns: VSOA server object.

``` python
client = vsoa.Client()
```

# VSOA Client Object
## client.connected

Whether the current client is connected to the server.

## client.onconnect

This function is called when this client connects or disconnects from the server.

``` python
def onconnect(client, conn: bool, info: str | dict | list)
	if conn:
		print('Connected, server info:', info)
	else:
		print('disconnected')

client.onconnect = onconnect
```

## client.ondata
+ On server DATAGRAM data received callback.

The client will call this function when server DATAGRAM data received.

``` python
def ondata(client, url: str, payload: vsoa.Payload, quick: bool):
	print('DATARAM URL:', url, 'Payload:', dict(payload), 'Q:', quick)

client.ondata = ondata
```

## client.close()

Close this client. This client object is no longer allowed to be used.

## client.call(url: str, method: str | int = 0, payload: vsoa.Payload | dict = None, callback: callable = None, timeout: float = 60.0) -> bool
+ `url` Command URL.
+ `method` Request method `vsoa.METHOD_GET` (0) or `vsoa.METHOD_SET` (1)
+ `payload` Request payload.
+ `callback` Server response callback.
+ `timeout` Wait timeout out.
+ Returns: Whether request send successfully.

``` python
def onreply(client, header: vsoa:Header, payload: vsoa:Payload):
	if header:
		print(dict(header), dict(payload))
	else:
		print('Server no response!')

ret = client.call('/echo', payload = vsoa.Payload({ 'a': 1 }), callback = onreply)
if not ret:
	print('RPC request error!')
```

This function will return immediately, and the `callback` will be executed in the client event loop thread. The `callback` `header` argument object has the following members:

+ `status` Response status.
+ `tunid` If it is not 0, it means the server stream tunnel ID.

## client.ping(callback: callable = None, timeout: float = 60.0) -> bool
+ `callback` Server ping echo callback.
+ `timeout` Wait timeout out.
+ Returns: Whether request send successfully.

Send a ping request.

``` python
def onecho(cli, success: bool):
	print('Ping echo:', success)

client.ping(onecho, 10)
```

## client.subscribe(url: str | list[str], callback: callable = None, timeout: float = 60.0) -> bool:
+ `url` URL or URL list that needs to be subscribed.
+ `callback` Subscription callback.
+ `timeout` Wait timeout out.
+ Returns: Whether request send successfully.

Subscribe to the specified URLs message. When the server publishes matching message, the client can receive this data use `onmessage`.

``` python
def onmessage(client, url: str, payload: vsoa.Payload, quick: bool):
	print('Msg received, url:', url, 'payload:', dict(payload), 'Q:', quick)

client.onmessage = onmessage

client.subscribe('/topic1')
client.subscribe(['/topic2', '/topic3'])
```

## client.unsubscribe(url: str | list[str], callback: callable = None, timeout: float = 60.0) -> bool:
+ `url` URL or URL list that needs to be unsubscribed.
+ `callback` Subscription callback.
+ `timeout` Wait timeout out.
+ Returns: Whether request send successfully.

Unsubscribe to the specified URLs message.

## client.datagram(url: str, payload: vsoa.Payload | dict = None, quick: bool = False) -> bool
+ `url` Specified URL.
+ `payload` DATAGRAM payload.
+ `quick` Whether to use quick channel.
+ Returns: Whether send successfully.

Send a DATAGRAM data to server.

# VSOA Client Object Current Thread Loop Mode
## client.connect(url: str, passwd: str = '', timeout: float = 10.0, sslopt: dict = None) -> int
+ `url` Server URL.
+ `passwd` Server password. Optional.
+ `timeout` Connect timeout.
+ `sslopt` TLS connection options, Currently not supported.
+ Returns: Error code.

Connect to the specified server and return the following code:

Constant|Value|
---|:--:|
`Client.CONNECT_OK`|0
`Client.CONNECT_ERROR`|1
`Client.CONNECT_UNREACHABLE`|2
`Client.SERVER_NOT_FOUND`|3
`Client.SERVER_NO_RESPONDING`|4
`Client.INVALID_RESPONDING`|5
`Client.INVALID_PASSWD`|6

``` python
ret = client.connect('vsoa://vserv')
ret = client.connect('vsoa://192.168.0.1:3005')
if ret:
	print('Connect error:', ret)
```

## client.disconnect()

Disconnect from server. 

``` python
client.disconnect()

time.sleep(3)

client.connect('vsoa://your_server_name_or_ip:port') # reconnect
```

## client.run()

Run the client event loop. When this function exits normally, it means that the client has disconnected from the server or the client has been closed.

``` python
client = vsoa.Client()

while True:
	if client.connect('vsoa://192.168.1.1:3005'):
		time.sleep(1)
	else:
		client.run()
		time.sleep(1)
```

# VSOA Client Object Robot Loop Mode
## client.robot(server: str, passwd: str = '', keepalive: float = 3.0, conn_timeout: float = 10.0, reconn_delay: float = 1.0, sslopt: dict = None)
+ `server` Server URL.
+ `passwd` Server password.
+ `keepalive` How long does it take to ping the server after a successful connection?
+ `conn_timeout` Connection timeout.
+ `reconn_delay` Waiting time for reconnection after disconnection.
+ `sslopt` TLS connection options, Currently not supported.

This function will automatically start a robot thread to handle the client event loop, and will automatically handle broken links.

``` python
client = vsoa.Client()
client.robot('vsoa://192.168.1.1:3005') # Automatically create a new thread responsible for the event loop

while True:
	time.sleep(1)

	header, payload, errcode = client.fetch('/echo', payload = { 'param': { 'a': 3 }})
	if header:
		print(dict(header), dict(payload))
	else:
		print('fetch error:', errcode) # `errcode` is same as client connect error code
```

## client.fetch(url: str, method: str | int = 0, payload: vsoa.Payload | dict = None, timeout: float = 60.0) -> tuple[vsoa.Header, vsoa.Payload, int]
+ `url` Command URL.
+ `method` Request method `vsoa.METHOD_GET` (0) or `vsoa.METHOD_SET` (1)
+ `payload` Request payload.
+ `timeout` Wait timeout out.
+ Returns: Request result and error code.

This function is a synchronous version of client.call, this function is not allowed to be executed in the client event loop thread.

# VSOA Client 'Once'
If we only need one RPC request and don't want to maintain a long-term connection with the server, we can use the following operation.

## vsoa.fetch(url: str, passwd: str = None, method: str | int = 0, payload: vsoa.Payload | dict = None, timeout: float = 10.0, raw: bool = False, sslopt: dict = None) -> tuple[vsoa.Header, vsoa.Payload, int]
+ `url` Request URL.
+ `passwd` Server password.
+ `method` Request method `vsoa.METHOD_GET` (0) or `vsoa.METHOD_SET` (1)
+ `payload` Request payload.
+ `timeout` Wait timeout out.
+ `raw` Whether to automatically parse JSON `payload.param`.
+ `sslopt` TLS connection options, Currently not supported.
+ Returns: Whether request result and error code.

``` python
header, payload, _ = vsoa.fetch('vsoa://192.168.1.1:3001/echo', payload = { 'param': { 'a': 3 }})
if header:
	print(dict(header), dict(payload))
```

# VSOA Position Server
## vsoa.Position(onquery: callable)
+ `onquery` Client host address query callback.
+ Returns: Position server object.

Create a position server.

``` python
def onquery(search: dict, reply: callable):
	if search['name'] == 'myserver':
		reply({ 'addr': '127.0.0.1', 'port': 3005, 'domain': socket.AF_INET })
	else:
		reply(None)

pserv = vsoa.Position(onquery)

pserv.run('0.0.0.0', 3000) # Position server run, never return
```

# VSOA Position Query
## vsoa.pos(addr: str, port: int)
+ `addr` Position server IP address.
+ `port` Position server port.

This function can specify the position server address used by `vsoa.lookup`.

## vsoa.lookup(name: str, domain: int = -1) -> tuple[str, int]:
+ `name` Server name.
+ `domain` Specify IP protocol family, `-1` means any.
+ Returns: Queryed server address.

Query the specified server address.

``` python
addr, port = vsoa.lookup('myserv')
if addr:
	...
```

Query order:
+ Use the position server specified by `vsoa.pos()`
+ Use the position server specified by the `VSOA_POS_SERVER` environment variable.
+ Use the position server specified by the `/etc/vsoa.pos` configuration file (`C:\Windows\System32\drivers\etc\vsoa.pos` on windows)

# VSOA Timer
VSOA provides a general timer function, and the timer callback will be executed in the timer service thread.

## vsoa.Timer() -> Timer

Create a timer object.

## timer.start(timeout: float, callback: callable, interval: float = 0, args = (), kwargs = {})
+ `timeout` Timer timeout seconds.
+ `callback` Timer timeout callback.
+ `interval` Periodic interval seconds, `0` means one shot timing.
+ `args` Callback arguments.
+ `kwargs` Callback keywords arguments.

``` python
timer = vsoa.Timer()

def func(a, b, c):
	print('timer!', a, b, c)

# One shot timer, Execute `func` function after 1.5s
timer.start(1.5, func, args = (1, 2, 3))
```

## timer.stop()

Stop a timer. A stopped timer can be started again.

## timer.is_started() -> bool

Check whether the timer is timing.

# VSOA EventEmitter
vsoa provides an `EventEmitter` class similar to JSRE and NodeJS to facilitate event subscription.

`EventEmitter` has two special events `'new_listener'` and `'remove_listener'` indicating the installation and removal of listener. These events is generated automatically. Developers are not allowed to emit these events.

`'new_listener'` and `'remove_listener'` event callback parameters are as follows:
+ `event` Event.
+ `listener` Event listener.

## vsoa.EventEmitter()

Event emitter class, Users class can inherit this class.

``` python
class MyClass(vsoa.EventEmitter):
	def __init__(self):
		super().__init__()
		...
```

## event.add_listerner(event: int | str | object, listener: callable) -> None
+ `event` Event
+ `listener` When this event occurs, this callback function is executed.

Add a listener for the specified event. The listener function arguments need to be consistent with the parameters generated by the event.

``` python
def func():
	print('event catched!')

event = vsoa.EventEmitter()

# Add listener
event.add_listerner('test', func)

# Emit event
event.emit('test')
```

## event.on(event: int | str | object, listener: callable) -> None

Alias ​​of `event.add_listerner`

## event.once(event: int | str | object, listener: callable) -> None

Similar to `event.add_listerner`, but the added event listener function will only be executed once.

## event.remove_listener(event, listener: callable = None) -> bool
+ `event` Event
+ `listener` Need matching listener function

Delete the previously added event listener. If `listener` is `None`, it means deleting all listeners for the specified event.

## event.remove_all_listeners(event = None) -> None
+ `event` Event

Delete all listeners for the specified event, `event` is `None` means deleting all listeners functions for all events.

## event.listener_count(event) -> int
+ `event` Event

Get the number of listeners for the specified event.

## event.listeners(event) -> list[callable]
+ `event` Event

Get the listener list of the specified event

## event.emit(event, args = (), kwargs = {}) -> bool
+ `event` Event
+ `args` Event arguments.
+ `kwargs` Event keyword arguments.

Generate an event, the listener corresponding to this event will be run according to the installation order.

``` python
class MyClass(vsoa.EventEmitter):
	def __init__(self):
		super().__init__()
		self.on('test', self.on_test)

	def on_test(self, a, b) -> None:
		print(a, b)

e = MyClass()
e.emit('test', args = (1, 2))
```

# VSOA WorkQueue
VSOA provides an asynchronous work queue function. Users can add job functions to the asynchronous work queue for sequential execution.

## vsoa.WorkQueue() -> WorkQueue

Create a work queue.

## wq.add(func: callable, args = (), kwargs = {}) -> None
+ `func` Work queue job function.
+ `args` Function arguments.
+ `kwargs` Function keywords arguments.

``` python
def hello(count: int):
	print('Hello count:', count)

wq = vsoa.WorkQueue()
wq.add(hello, args = (1))
wq.add(hello, args = (2))
wq.add(hello, args = (3))
```

The server can use `WorkQueue` to implement asynchronous command processing to avoid the main loop being blocked for too long.

``` python
app = vsoa.Server('hello')
wq  = vsoa.WorkQueue()

@app.command('/hello', wq)
def echo(cli, request, payload):
	cli.reply(request.seqno, payload)

app.run('0.0.0.0', 3005)
```

## wq.add_if_not_queued(func: callable, args = (), kwargs = {}) -> bool
+ `func` Work queue job function.
+ `args` Function arguments.
+ `kwargs` Function keywords arguments.
+ Returns: Whether add is successful.

Add job if job function not in queued.

## wq.delete(func: callable) -> bool:
+ `func` Work queue job function.
+ Returns: Whether the deletion is successful.

Delete the specified job that is not being executed in the queue.

## wq.is_queued(func: callable) -> bool:
+ `func` Work queue job function.
+ Returns: Whether queued.

Whether the specified jon is in the queue.

---
