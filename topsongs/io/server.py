import asyncio

from fastapi import FastAPI
from uvicorn import Config, Server


class SimpleServer:
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 8080

        self.app = FastAPI()
        self.app.post("/")(self.callback)

        self.event = asyncio.Event()
        self.code = None

    @property
    def url(self) -> str:
        return f"http://{self.host}:{self.port}/"

    async def callback(self, code: str):
        self.code = code
        self.event.set()
        return {"status": "Thanks for authorizing"}

    async def listen(self) -> str:
        config = Config(app=self.app, host=self.host, port=self.port, loop="asyncio")
        server = Server(config)

        await server.serve()
        await self.event.wait()
        await server.shutdown()
        return self.code