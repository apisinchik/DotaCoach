import json

from fastapi import FastAPI, Request
from PyQt6.QtCore import QObject, pyqtSignal

from dota_worker.evaluation import Map

dota_worker = FastAPI()

class UiBridge(QObject):
    hero_ban = pyqtSignal(int)

ui_bridge = UiBridge()

class DotaWorker:
    @dota_worker.post("/")
    @staticmethod
    async def main_router(request: Request):
        data = await request.json()

        game_status = data['map']['game_state']
        is_banning_event = 'CHAT_MESSAGE_HERO_BANNED' in data['events'][0]['data']
        if game_status == 'DOTA_GAMERULES_STATE_HERO_SELECTION' and is_banning_event:
            banning_events = data['events']
            for event in banning_events:
                event = json.loads(event['data'], object_pairs_hook=Map)
                hero_id = event['value']
                print(hero_id, type(hero_id))
                ui_bridge.hero_ban.emit(hero_id)


        
        return 'ok'