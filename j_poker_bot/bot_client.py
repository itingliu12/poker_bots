# bot_client.py

import asyncio
import json
import os
import websockets

from poker_ai import choose_action  # hi
# hello there testing testing 123


PLAYER_ID = "csc4444-bot-j"
PLAYER_NAME = "CSC 4444 Team J"

SERVER_URL = os.getenv("POKER_WS_URL", "ws://localhost:8000/ws")


async def run_bot():

    print(f"Connecting to {SERVER_URL}")

    async with websockets.connect(SERVER_URL) as ws:
        # Join the poker table
        join_message = {"type": "join", "name": PLAYER_NAME, "player_id": PLAYER_ID}

        await ws.send(json.dumps(join_message))

        print(f"{PLAYER_NAME} connected")

        while True:
            raw_message = await ws.recv()
            message = json.loads(raw_message)
            message_type = message.get("type")

            if message_type == "state":
                state = message["payload"]

                # Only act when it is our turn
                if state.get("current_turn") != PLAYER_ID:
                    continue

                action = choose_action(state, PLAYER_ID)

                action_message = {"type": "action", "action": action}

                await ws.send(json.dumps(action_message))

                print(f"Sent action: {action}")

            elif message_type == "action_result":
                result = message["payload"]
                if not result.get("ok"):
                    print("Action rejected:", result)

            elif message_type == "error":
                print("Server error:", message.get("message"))


if __name__ == "__main__":
    try:
        asyncio.run(run_bot())
    except KeyboardInterrupt:
        print("Bot stopped")
