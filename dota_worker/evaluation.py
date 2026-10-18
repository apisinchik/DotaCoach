import asyncio
import json
import subprocess

import aiohttp


class DataRecipient:
 
    def write_schema_to_file(self, schema):
        with open('data/heroes_schema.json', 'w') as file:
            json.dump(schema, file)


    async def get_heroes_schema(self) -> dict:
        async with aiohttp.ClientSession().get('https://api.opendota.com/api/heroes') as schema:
            schema = await schema.json()
            await asyncio.to_thread(self.write_schema_to_file(schema))


    def decompile_images(self):
        subprocess.run(['/home/algol83/PycharmProjects/DotaCoach/Source2Viewer-CLI/Source2Viewer-CLI',
                        '-i', '/home/algol83/.var/app/com.valvesoftware.Steam/.local/share/Steam/steamapps/common/dota 2 beta/game/dota/pak01_dir.vpk',
                        '--output', '/home/algol83/PycharmProjects/DotaCoach/images/selection',
                        '-f', 'panorama/images/heroes/selection', '-d'], check=False)


class Map:
    def __init__(self, data=()):
        self.data = []
        for key, val in data:
            self[key] = val

    def __getitem__(self, key):
        for selfed_key, val in self.data:
            if key == selfed_key:
                return val

    def __setitem__(self, key, val):
        for i, (selfed_key, _) in enumerate(self.data):
            if selfed_key == key:
                self.data[i] = key, val
                return
        self.data.append((key, val))

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        for key, _ in self.data:
            yield key

    def __contains__(self, key):
        return any(selfed_key == key for selfed_key, _ in self.data)

    def get(self, key):
        try:
            return self[key]
        except Exception as exc:
            return exc