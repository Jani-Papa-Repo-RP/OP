import asyncio

from PritiMusic.misc import db
from PritiMusic.utils.database import get_active_chats, is_music_playing


async def timer():
    while not await asyncio.sleep(1):
        active_chats = await get_active_chats()
        for chat_id in active_chats:
            if not await is_music_playing(chat_id):
                continue
            playing = db.get(chat_id)
            if not playing:
                continue
            duration = int(playing[0].get("seconds", 0))
            if duration == 0:
                continue
                
            # 🚀 KeyError Fix: Safely get the 'played' value, default to 0 if not found
            current_played = db[chat_id][0].get("played", 0)
            
            if current_played >= duration:
                continue
                
            # Safely increment the 'played' value
            db[chat_id][0]["played"] = current_played + 1


asyncio.create_task(timer())
