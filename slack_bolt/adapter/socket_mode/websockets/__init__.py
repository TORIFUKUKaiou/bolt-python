import os
from time import time
from typing import Optional

from slack_sdk.socket_mode.websockets import SocketModeClient
from slack_sdk.socket_mode.request import SocketModeRequest

from slack_bolt import App
from slack_bolt.adapter.socket_mode.async_base_handler import AsyncBaseSocketModeHandler
from slack_bolt.adapter.socket_mode.async_internals import (
    send_async_response,
    run_async_bolt_app,
)
from slack_bolt.adapter.socket_mode.internals import run_bolt_app
from slack_bolt.app.async_app import AsyncApp
from slack_bolt.response import BoltResponse


class SocketModeHandler(AsyncBaseSocketModeHandler):
    app: App
    app_token: str
    client: SocketModeClient

    def __init__(
        self, app: App, app_token: Optional[str] = None,
    ):
        self.app = app
        self.app_token = app_token or os.environ["SLACK_APP_TOKEN"]
        self.client = SocketModeClient(app_token=self.app_token)
        self.client.socket_mode_request_listeners.append(self.handle)

    async def handle(self, client: SocketModeClient, req: SocketModeRequest) -> None:
        start = time()
        bolt_resp: BoltResponse = run_bolt_app(self.app, req)
        await send_async_response(client, req, bolt_resp, start)


class AsyncSocketModeHandler(AsyncBaseSocketModeHandler):
    app: AsyncApp
    app_token: str
    client: SocketModeClient

    def __init__(
        self, app: AsyncApp, app_token: Optional[str] = None,
    ):
        self.app = app
        self.app_token = app_token or os.environ["SLACK_APP_TOKEN"]
        self.client = SocketModeClient(app_token=self.app_token)
        self.client.socket_mode_request_listeners.append(self.handle)

    async def handle(self, client: SocketModeClient, req: SocketModeRequest) -> None:
        start = time()
        bolt_resp: BoltResponse = await run_async_bolt_app(self.app, req)
        await send_async_response(client, req, bolt_resp, start)
