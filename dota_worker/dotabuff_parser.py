import json
import asyncio
from abc import ABC, abstractmethod

import aiohttp
from bs4 import BeautifulSoup
from curl_cffi import AsyncSession
import lxml

from dota_worker.evaluation import Map

# www.dotabuff.com

class Entity(ABC):
    @property
    @abstractmethod
    def get_name(self):
        ...
    @get_name.setter
    @abstractmethod
    def set_name(self, name):
        ... 
    

class Hero(Entity):
    def __init__(self, 
                 id: int,
                 name: str):
        self.name = name
        self.id = id

    def __new__(cls, id, name):
        print('The __new__ method')
        return super().__new__(cls)

    def __del__(self):
        print('The __del__ method')

    def __repr__(self):
        print('The official string: ')
        return f'Hero class, id = {self.id}, name = {self.name}'

    def __str__(self):
        print('The string: ')
        return 'Hero class'

    def __eq__(self, other):
        print('EQ:')
        return self.id == other.id

    def __bytes__(self):
        print('Bytes: ')
        return str(self).encode('utf-8')

    @property
    def get_name(self):
        return self.name

    @get_name.setter
    def set_name(self, name: str):
        self.name = name

    @property
    def get_id(self):
        return self.id

    @get_id.setter
    def set_id(self, id: int):
        self.id = id

    @staticmethod
    def hero_name_by_id(hero_id: int) -> str | None:
        for hero in Hero.all_heroes_schema():
            if hero["id"] == hero_id:
                return hero["name"]
        return None

    def all_heroes_schema() -> dict:
        with open('data/heroes_schema.json') as file:
            schema = json.load(file, object_pairs_hook=Map)
            return schema



class DotabuffParser:
    def __init__(self):
        self.heroes = []

    def create_hero(self, id, name):
        hero = Hero(id, name)  
        self.heroes.append(hero)      

    @property
    def get_heroes(self):
        return self.heroes

    @get_heroes.setter
    def set_heroes(self, heroes):
        self.heroes = heroes

    def __eq__(self, other):
            print('EQ:')
            return self.heroes == other.heroes
    # async def parse_dotabuff_names(self):
    #     self.heroes = {}
    #     async with AsyncSession(impersonate='chrome') as session:
    #         response = await session.get('https://ru.dotabuff.com/heroes')
    #         soup = BeautifulSoup(response.text, 'lxml')
    #         cards = soup.find('tbody', class_='[&amp;_tr:last-child]:tw-border-0')
    #         print(soup)
    #         print(cards)
    #         schema = await asyncio.to_thread(Hero.all_heroes_schema)
    #         for link in cards.find_all('a', class_='tw-block tw-relative tw-shrink-0'):
    #             dotabuff_name = link['href'].split('/')[-1]
    #             clear_dotabuff_name = dotabuff_name.lower().split('-')
    #             for name in schema:
    #                 name = name['localized_name']
    #                 clear_name = name['localized_name'].lower().split(' ')
    #                 if clear_name in clear_dotabuff_name:
    #                     self.heroes.append(Hero(name, dotabuff_name, name['id']))

    #     print(self.heroes)
    #     print(len(self.heroes))

                    



