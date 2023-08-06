"""
Hi this is calion speaking now
"""


import socketio, asyncio, inspect, datetime, types
from .context import Context
from .message import Message
from .help import mk_help 


class Bot:
    def __init__(self, *args, **kwargs):
        prefix = kwargs.get("prefix")
        username = kwargs.get("username")
        auth = kwargs.get("auth")

        if prefix == None:
            raise ValueError("Missing required value, prefix.")

        if auth == None:
            raise ValueError("Missing required value, auth.")

        if username == None:
            raise ValueError("Missing required value, username.")

        
        self.__uri = kwargs.get("sio_uri", "wss://replchat.vapwastaken.repl.co/")
        self.__headers = {
            'X-Replit-User-Name': username,
            "Cookie": "REPL_AUTH="+auth
        }

        self.username = username
        self.prefix = prefix
        self.watermark = kwargs.get('watermark')
        self.commands = []
        self.events = []
        self.case_insensitive = kwargs.get('case_insensitive', False)

        self.loop = asyncio.get_event_loop()
        self.ws = socketio.AsyncClient()
        self.connected = False
        self.owner = kwargs.get("owner")
        if not self.owner:
            raise ValueError("Who is making this bot? Missing required value, owner.")
        self.on_ready_callback = None
        self.help_command = kwargs.get("help_command", True)

        if kwargs.get("help_command", True):
            @self.command(
                name="help",
                description="Displays this message."
            )
            async def help_cmd(ctx):
                await ctx.send(mk_help(self.commands, prefix))

    

    def command(self, **kwargs):
        def register_command(callback, **callback_kwargs):
            parameters = str(inspect.signature(callback))[1:][:-1].split(", ")
            self.commands.append(
                {
                    'name': kwargs.get('name', callback.__name__) if not self.case_insensitive else kwargs.get('name', callback.__name__).lower(),
                    'description': kwargs.get('description', "None provided!"),
                    'hidden': kwargs.get('hidden', False),
                    'aliases': kwargs.get('aliases', []),
                    'callback': callback,
                    'params': parameters
                }
            )
            return callback
        return register_command

    async def latency(self):
        self.start = datetime.datetime.now().timestamp()
        await self.ws.emit('ping')
        self.ws.on('chat message')
        self.ltncy = datetime.datetime.now().timestamp() - self.start
        return self.ltncy * 100

    async def send(self, content: str = "Message sent by replchat.py"):
        if not self.connected:
            return

        if self.watermark:
            content += f"\n\n\n\n{self.watermark}"

        await self.ws.emit(
            "chat message",
            {
                "message": content
            }
        )

    
    def on_ready(self, callback):
        self.ws.on('connect', callback)

    def on(self, event):
        def register_event(callback, **callback_kwargs):
            parameters = str(inspect.signature(callback))[1:][:-1].split(", ")
            self.events.append(
                {
                    'name': event.lower() or callback.__name__.lower(),
                    'callback': callback,
                    'params': parameters
                }
            )
            return callback
        return register_event

    def find_event(self, event_name):
        evt = [e for e in self.events if e['name'].lower() == event_name.lower()]

        async def nothing(*_, **__):
            "nothing"

        res = evt[0] if bool(evt) else {'callback':nothing}
        return res

    async def invoke(self, command, data):
        msg = data['message']
        cmd = command
        context = Context(self, data, cmd)
        args = cmd['params'][1:]
        
        if args == []:
            await cmd['callback'](context)
        if '*' in args:
            one_word_args = args.index("*")

        else:
            one_word_args = len(args)

        true_args = args.copy()
        try:
            true_args.remove("*")
        except Exception as e:
            pass

        if one_word_args != -1:
            if one_word_args == len(true_args) and one_word_args != 0:
                one_word_args = " ".join(msg.split(" ")[one_word_args:])
                await cmd['callback'](context, *[one_word_args])

            elif one_word_args > 0 and len(true_args) == one_word_args:
                argus = msg.split(" ")[1:]
                await cmd['callback'](context, *[argus])

            elif len(true_args) != 0 and one_word_args == 0:
                m = " ".join(msg.split(" ")[1:])
                m = [
                    m if m else a.split("=")[1]
                    for a in true_args
                    if '=' in a
                ]
                m_n = [
                    a.split("=")[0]
                    for a in true_args
                    if '=' in a
                ]
                try:
                    m = m[0]
                except IndexError:
                    m = " ".join(msg.split(" ")[1:])
                    m_n = m_n = [
                        args[-1]
                    ]

                if isinstance(m, str):
                    try:
                        m = eval(m)
                    except Exception:
                        pass

                
                await cmd['callback'](
                    context, 
                    **{
                        m_n[0]: m
                    })

            elif len(true_args) != 0 and one_word_args >= 0:
                argus = msg.split(" ")[1:one_word_args+1]
                await cmd['callback'](
                    context,
                    *argus,
                    **{
                        args[-1]: " ".join(msg.split(" ")[one_word_args+1:])
                    }
                )

        
    def run(self):
        @self.ws.on('debug')
        async def debug(code):
            if code == "REQUIRES_IDENTIFY":
                await self.ws.emit('identify', self.username)

        @self.ws.on('*')
        async def event(evt, data):
            if evt == "getmessages":
                self.connected = True


            elif evt == "chat message":
                message = Message(data, self)
                msg_evt = self.find_event('message')
                await msg_evt['callback'](message)
                if '@'+self.username.lower() in message.content.lower():
                    message = Message(data, self)
                    mention = self.find_event('mention')
                    await mention['callback'](message)

                if data['username'] != self.username:
                    msg = data['message']
                    username = data['message']
                    if isinstance(self.prefix, types.FunctionType):
                        prefix = self.prefix()
    
                    else:
                        prefix = self.prefix
    
                    if msg.startswith(prefix):
                        command = [
                            c for c in self.commands if msg[1:].startswith(c['name'])
                        ]

                        aliases = [
                            c for c in self.commands
                            for a in c['aliases'] if msg[1:].startswith(a)
                        ]
                        
                        if not bool(command) and not bool(aliases):
                            message = Message(data, self)
                            cmd_not_found = self.find_event('command_not_found')
                            await cmd_not_found['callback'](message)
    
                        elif bool(command):
                            cmd = command[0]
                            await self.invoke(cmd, data)

                        elif bool(aliases):
                            cmd = aliases[0]
                            await self.invoke(cmd, data)
    
    
                pass
        async def main():
            await self.ws.connect(
                self.__uri,
                self.__headers
            )

        self.loop.create_task(main())
        self.loop.run_forever()
        
