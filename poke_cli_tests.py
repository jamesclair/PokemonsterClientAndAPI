import asyncio
from unittest import IsolatedAsyncioTestCase
from poke_cli import get_pokemon_details, get_pokemon_page, set_type_and_move_lookups

def test_get_pokemon_page_w_length():
    num_pokemon = 2
    assert(len(get_pokemon_page(limit = num_pokemon)) == num_pokemon)
    
def test_get_all_pokemon():
    num_pokemon_requested = 1500
    num_pokemon_total = 1281
    assert(len(get_pokemon_page(limit = num_pokemon_requested)) == num_pokemon_total)
    
def test_get_pokemon_page_data():
    num_pokemon = 2
    expected = [{'name': 'bulbasaur', 'url': 'https://pokeapi.co/api/v2/pokemon/1/'}, {'name': 'ivysaur', 'url': 'https://pokeapi.co/api/v2/pokemon/2/'}]
    assert(get_pokemon_page(limit = num_pokemon) == expected)

class Atest(IsolatedAsyncioTestCase):

    async def test_get_pokemon_details(self):
        pokemons =  [{'name': 'bulbasaur', 'url': 'https://pokeapi.co/api/v2/pokemon/1/'}, {'name': 'ivysaur', 'url': 'https://pokeapi.co/api/v2/pokemon/2/'}]
        result = await get_pokemon_details(pokemons)
        p_names = []
        for r in result:
            p_names.append(r.name)
        
        for p in pokemons:
            self.assertIn(p['name'], p_names)
            
    
    async def test_get_type_and_move_lookups(self):
        pokemons = [{'name': 'bulbasaur', 'url': 'https://pokeapi.co/api/v2/pokemon/1/'}, {'name': 'ivysaur', 'url': 'https://pokeapi.co/api/v2/pokemon/2/'}]
        pokemon_details = await get_pokemon_details(pokemons)
        pokemon_by_type, pokemon_by_move = set_type_and_move_lookups(pokemon_details)
        self.assertIn("grass", pokemon_by_type.keys())
        self.assertIn("leech-seed",  pokemon_by_move.keys())
        
        
if __name__ == "__main__":
    
    test_get_pokemon_page_w_length()
    test_get_all_pokemon()
    test_get_pokemon_page_data()
    
    atest = Atest()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(atest.test_get_pokemon_details())
    loop.run_until_complete(atest.test_get_type_and_move_lookups())