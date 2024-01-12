from dataclasses import dataclass
from typing import List, Dict
import asyncio
import aiopoke
import requests
from unittest import IsolatedAsyncioTestCase

BASE_URL: str = 'https://pokeapi.co/api/v2/'
pokemon_by_type: Dict[str, List] = {}
pokemon_by_move: Dict[str, List] = {}

def get_pokemon_page(offset: int = 0, limit: int = 10) -> List:
    payload = {'offset': f'{offset}', 'limit': f'{limit}'}
    try:
        with requests.get(f'{BASE_URL}pokemon', params=payload) as r:
            r.raise_for_status()
            data = r.json()
            return data['results']
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
    except requests.exceptions.ReadTimeout as e:
        print(f"Time out: {e}")
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error: {e}")
    except requests.exceptions.JSONDecodeError as e:
        print(f"Unable to Decode JSON: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Exception request: {e}")

async def get_pokemon_details(pokemons: List[Dict[str, str]]) -> aiopoke.Pokemon:
    pokemons_detailed = []
    # might be able to move this to a more generalized location
    async with aiopoke.AiopokeClient() as client:
        for p in pokemons:
            pokemons_detailed.append(client.get_pokemon(p['name']))
        
        pokemons_detailed = await asyncio.gather(*pokemons_detailed)
        # name, order, height, weight, associated types (just the name of the type),
#     # and available moves (name and power of the move)
    return pokemons_detailed

def set_type_and_move_lookups(pokemon_details):
    
    for p in pokemon_details:
        for t in p.types:
            if pokemon_by_type.get(t.type.name):
                pokemon_by_type[t.type.name].append(p)
            else:
                pokemon_by_type[t.type.name] = [p]

        for m in p.moves:
            if pokemon_by_move.get(m.move.name):
                pokemon_by_move[m.move.name].append(p)
            else:
                pokemon_by_move[m.move.name] = [p]
        
    return pokemon_by_type, pokemon_by_move
    
    
def get_pokemon_by_type(type_name: str) -> List:
    return pokemon_by_move[type_name]
    
def get_pokemon_by_move(move_name: str) -> List:
    return pokemon_by_move[move_name]
    
if __name__ == "__main__":
    
    loop = asyncio.get_event_loop()
    pokemons = get_pokemon_page(limit = 3)
    pokemon_details = loop.run_until_complete(get_pokemon_details(pokemons))
    
    set_type_and_move_lookups(pokemon_details)
    
    print('Grass type pokemon: ')
    for p in get_pokemon_by_type("grass"):
        print(p.name)
    
    print('Pokemon with leech-seed move: ')
    for p in get_pokemon_by_move('leech-seed'):
        print(p.name)
