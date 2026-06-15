import asyncio
import queue
import time

from fastapi import WebSocket, FastAPI, WebSocketDisconnect

from Board import Board
from Controller import Controller, ForfeitException
from MoveParser import MoveParser, InvalidMove
from logger import Logger


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
        self.player_queue: asyncio.LifoQueue = asyncio.LifoQueue()
        self.inboxes: dict[WebSocket, asyncio.Queue] = {}
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        self.inboxes[websocket] = asyncio.Queue()
        await self.player_queue.put(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

class Game:
    def __init__(self,player1,player2,manager:ConnectionManager):
        self.board:Board = Board()
        self.board.seed_starting_board()
        self.player1 = player1
        self.player2 = player2
        self.manager = manager
        self.winner = None

    async def play(self):
        await self.manager.send_personal_message("FOUND",self.player1)
        await self.manager.send_personal_message("FOUND",self.player2)
        move_parser = MoveParser()
        logger = Logger()

        white_controller = Controller(move_parser,self.board,"white",logger)
        black_controller = Controller(move_parser,self.board,"black",logger)
        if time.time_ns() %2 ==1:
            await self.manager.send_personal_message("WHITE",self.player1)
            await self.manager.send_personal_message("BLACK",self.player2)
            white = self.player1
            black = self.player2
        else:
            await self.manager.send_personal_message("BLACK",self.player1)
            await self.manager.send_personal_message("WHITE",self.player2)
            white = self.player2
            black = self.player1
        await self.manager.send_personal_message("START", white)
        await self.manager.send_personal_message("START", black)
        while True:

            moved: bool = False
            while not moved:
                try:
                    movestr = (await self.manager.inboxes[white].get()).strip()
                    if movestr == "disconnect":
                        await self.manager.send_personal_message("ff white", black)
                        return
                    if white_controller.proccess_input(movestr):
                        moved = True
                        if self.board.is_checkmate():
                            await self.manager.send_personal_message("CHECKMATE "+ self.board.get_winner(), black)
                            await self.manager.send_personal_message("CHECKMATE "+ self.board.get_winner(), white)
                            return

                        await self.manager.send_personal_message("CORRECT", white)
                        await self.manager.send_personal_message(movestr,black)


                except queue.Empty:
                    continue
                except InvalidMove as e:
                    await self.manager.send_personal_message(e.message,white)
                except ForfeitException as e:
                    await self.manager.send_personal_message("ff" +e.message,white)
                    await self.manager.send_personal_message("ff" + e.message,black)
                    return
                except RuntimeError as e:
                    try:
                        await self.manager.send_personal_message("ff white" , white)
                    except:
                        await self.manager.send_personal_message("ff black", black)

            moved: bool = False
            while not moved:
                try:
                    movestr = await self.manager.inboxes[black].get()
                    if movestr == "disconnect":
                        await self.manager.send_personal_message("ff black", white)
                        return

                    if black_controller.proccess_input(movestr):
                        moved = True
                        if self.board.is_checkmate():
                            await manager.send_personal_message("CHECKMATE "+ self.board.get_winner(), black)
                            await manager.send_personal_message("CHECKMATE "+ self.board.get_winner(), white)
                            return
                        await manager.send_personal_message("CORRECT", black)
                        await manager.send_personal_message(movestr,white)

                except queue.Empty:
                    continue
                except InvalidMove as e:
                    await self.manager.send_personal_message(e.message, white)
                except ForfeitException as e:
                    await self.manager.send_personal_message("ff" + e.message, white)
                    await self.manager.send_personal_message("ff" + e.message, black)
                    return
manager = ConnectionManager()

app = FastAPI()


async def matchmaker():
    while True:
        player1 = await manager.player_queue.get()
        player2 = await manager.player_queue.get()

        game = Game(player1, player2, manager)
        print(f"starting game for {player1} and {player2}")
        asyncio.create_task(game.play())


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(matchmaker())


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print("recieved:" + data)
            await manager.inboxes[websocket].put(data)
    except WebSocketDisconnect:
        manager.inboxes[websocket].put_nowait("disconnect")
        manager.disconnect(websocket)