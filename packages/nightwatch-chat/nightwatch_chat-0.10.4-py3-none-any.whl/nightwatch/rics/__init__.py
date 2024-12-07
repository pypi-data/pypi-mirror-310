# Copyright (c) 2024 iiPython

# Modules
import base64
import typing
import binascii
from time import time
from secrets import token_urlsafe

from requests import Session, RequestException
from pydantic import BaseModel, Field

from fastapi import FastAPI, Response, WebSocket
from fastapi.responses import JSONResponse
from starlette.websockets import WebSocketDisconnect, WebSocketState

from nightwatch.config import fetch_config

# Load config data
config = fetch_config("rics")

# Initialization
app = FastAPI(
    openapi_url = None
)

# Scaffold the application
app.state.clients = {}
app.state.pending_clients = {}
app.state.message_log = []

async def broadcast(payload: dict) -> None:
    payload["data"]["time"] = round(time())
    if payload["type"] == "message":
        if "user" not in payload["data"]:
            payload["data"]["user"] = {"name": "Nightwatch", "hex": "555753", "admin": False}

        app.state.message_log = app.state.message_log[-24:] + [payload["data"]]

    for client in app.state.clients.values():
        await client.send(payload)

app.state.broadcast = broadcast

# Setup routing
class Client:
    def __init__(self, websocket: WebSocket, user_data) -> None:
        self.websocket = websocket
        self.username, self.hex_code, self.admin = user_data["username"], user_data["hex"], False

        self._callback = None

        # Attach to client list
        app.state.clients[self.username] = self

    def serialize(self) -> dict[str, str | bool]:
        return {"name": self.username, "hex": self.hex_code, "admin": self.admin}

    def cleanup(self) -> None:
        del app.state.clients[self.username]
        del self  # Not sure if this helps, in case Python doesn't GC

    async def send(self, payload: dict) -> None:
        if self.websocket.client_state != WebSocketState.CONNECTED:
            return

        try:
            if self._callback is not None:
                payload["data"] = payload.get("data", {}) | {"callback": self._callback}
                self._callback = None

            await self.websocket.send_json(payload)

        except WebSocketDisconnect:
            pass

    async def receive(self) -> typing.Any:
        try:
            data = await self.websocket.receive_json()

            # Handle callback
            callback = data.get("data", {}).get("callback")
            if isinstance(callback, str):
                self._callback = callback

            return data

        except WebSocketDisconnect:
            return None

class ClientJoinModel(BaseModel):
    username: str = Field(..., min_length = 3, max_length = 30)
    hex: str = Field(..., min_length = 6, max_length = 6, pattern = "^[0-9A-Fa-f]{6}$")

@app.post("/api/join")
async def route_index(client: ClientJoinModel) -> JSONResponse:
    if client.username in app.state.clients:
        return JSONResponse({
            "code": 400,
            "message": "Requested username is in use on this server."
        }, status_code = 400)

    if client.username.strip() != client.username:
        return JSONResponse({
            "code": 400,
            "message": "Requested username has whitespace that should be removed prior to joining."
        }, status_code = 400)

    if client.username.lower() in ["nightwatch", "admin", "moderator"]:
        return JSONResponse({
            "code": 400,
            "message": "Requested username is restricted for use."
        }, status_code = 400)

    client_token = token_urlsafe()
    app.state.pending_clients[client_token] = client.model_dump()
    return JSONResponse({
        "code": 200,
        "authorization": client_token
    })

@app.websocket("/api/ws")
async def connect_endpoint(
    authorization: str,
    websocket: WebSocket
) -> None:
    if authorization not in app.state.pending_clients:
        return await websocket.close(1008)

    user_data = app.state.pending_clients[authorization]
    del app.state.pending_clients[authorization]

    await websocket.accept()

    # Initialize client
    client = Client(websocket, user_data)

    # Get the client up to speed
    await client.send({"type": "rics-info", "data": {
        "name": config["name"] or "Nightwatch Server",
        "message-log": app.state.message_log,
        "user-list": [client.serialize() for client in app.state.clients.values()]
    }})

    # Broadcast join
    await app.state.broadcast({"type": "join", "data": {"user": client.serialize()}})
    await app.state.broadcast({"type": "message", "data": {"message": f"{client.username} has joined the server."}})

    # Handle loop
    while websocket.client_state == WebSocketState.CONNECTED:
        match await client.receive():
            case {"type": "message", "data": {"message": message}}:
                await app.state.broadcast({"type": "message", "data": {"user": client.serialize(), "message": message}})

            case {"type": "user-list", "data": _}:
                await client.send({"type": "response", "data": {
                    "user-list": [client.serialize() for client in app.state.clients.values()]
                }})

            case _:
                await client.send({"type": "problem", "data": {"message": "Invalid payload received."}})

    await app.state.broadcast({"type": "leave", "data": {"user": client.serialize()}})
    await app.state.broadcast({"type": "message", "data": {"message": f"{client.username} has left the server."}})
    client.cleanup()

# Handle image forwarding
SESSION = Session()
PROXY_SIZE_LIMIT = 10 * (1024 ** 2)
PROXY_ALLOWED_SUFFIX = ["avif", "avifs", "apng", "png", "jpeg", "jpg", "jfif", "webp", "ico", "gif", "svg"]

@app.get("/api/fwd/{public_url:str}", response_model = None)
async def forward_image(public_url: str) -> Response | JSONResponse:
    try:
        new_url = f"https://{base64.b64decode(public_url, validate = True).decode('ascii').rstrip('/')}"

    except (binascii.Error, UnicodeDecodeError):
        return JSONResponse({"code": 400, "message": "Failed to contact the specified URI."}, status_code = 400)

    filename = new_url.split("?")[0].split("/")[-1]
    if "." not in filename:
        return JSONResponse({"code": 400, "message": "Specified URI does not have an extension."}, status_code = 400)

    if filename.split(".")[-1] not in PROXY_ALLOWED_SUFFIX:
        return JSONResponse({"code": 400, "message": "Specified URI has an unsupported extension."}, status_code = 400)

    try:
        data = b""
        with SESSION.get(new_url, stream = True) as response:
            response.raise_for_status()
            for chunk in response.iter_content(PROXY_SIZE_LIMIT):
                data += chunk
                if len(data) >= PROXY_SIZE_LIMIT:
                    return JSONResponse({"code": 400, "message": "Specified URI contains data above size limit."}, status_code = 400)

            return Response(
                data,
                response.status_code,
                {
                    k: v
                    for k, v in response.headers.items() if k in ["Content-Type", "Content-Length", "Cache-Control"]
                }
            )

    except RequestException:
        return JSONResponse({"code": 400, "message": "Failed to contact the specified URI."}, status_code = 400)
