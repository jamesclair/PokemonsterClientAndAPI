# PokemonsterClientAndAPI

## Client Features

Retrieve Pokémon's name, order, height, weight, associated types (just the name of the type), and available moves (name and power of the move) that each Pokémon can learn.

- get_pokemon_by_type(type_name) that’ll return a collection of Pokémon of a specified
type
- get_pokemon_by_move(move_name) that’ll return a collection of Pokémon that can
learn specified move
- choose how many pokemon are loaded to make dev'ing quicker
- parallelized retrieval of data from api

## API Features

API includes pagination, validation, and persistence.

1. Create new Pokémon with name, order, height, weight, associated types, and available moves.
2. Create a new moves.
3. List all Pokémon.
   1. Allows filtering by Pokémon type and move name.
4. Get the best move for a Pokémon
   1. returns a move with the highest power that the specified Pokémon can learn.
5. Get pairs of Pokémon that can learn at least three same moves


## Pre-Reqs

- Python 3.11.1
- Poetry (version 1.5.1)

## Build

Install deps: `poetry install`
To apply your db schema: `python manage.py migrate`


## CLI Usage

Run `poetry shell` to source the your poetry venv.
Run `python ./poke_cli` to run a small example composition in which the pokeAPI returns all or a subset of pokemon, details are looked up for each pokemon in an async event loop w/ caching, and an example of the get_pokemon_by_type and get_pokemon_by_move lookups are used.

## API Usage

Run `python manage.py runserver` to start the django dev web server.

Create a pokemon:
```
curl --location --request GET 'http://127.0.0.1:8000/pokemon/create/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "Pikachu",
    "order": 25,
    "height": 0.4,
    "weight": 6,
    "types": [
        "Electric"
    ],
    "moves": [
        {
            "name": "Thunderbolt",
            "power": 90
        },
        {
            "name": "Quick Attack",
            "power": 40
        }
    ]
}'
```

Retrieve List of Pokemon:
```
curl --location --request GET 'http://127.0.0.1:8000/pokemon/'
```

Create a Move:
```
curl --location --request POST 'http://127.0.0.1:8000/move/create/' \
--header 'Content-Type: application/json' \
--data-raw '{
  "name": "haymaker",
  "power": 1000
}'
```

Learn new move:
```
curl --location --request POST 'http://127.0.0.1:8000/pokemon/learn_move/' \
--header 'Content-Type: application/json' \
--data-raw '{"pokemon_id": 1, "move_id": 4}'
```

Get best move:
```
curl --location --request GET 'http://127.0.0.1:8000/pokemon/best_move/1/'
```

Get similar:
```
curl --location --request GET 'http://127.0.0.1:8000/pokemon/similar/1'
```

## Testing

Run tests: `python poke_cli_tests.py`

## Improvements

- wrap it in an object oriented interface keeping as simple as possible
- separate concerns of working with aiopoke, pokeAPI, and manipulating the data in three different classes to decouple and allow for independent deployability and reduce potential of customers/clients being subject to breaking changes.  Rather only aditive changes.
- dockerize (I would use podman), but OCI compliant containers is the goal.  Allows a single versioned artifact that is deployable to a wide variety of different hosting platforms increasing portability.  Also doesn't hurt that it is declarative and extensible.  Multi-layer builds can be used to trim down the size of the container.
- Add a data model.  I'm used to pydantic and fastAPI.  Even started to use dataclasses, but aiopoke provided a pretty robust model for the data retrieved.  But it is also too verbose with too many extra fields for the use case.  
- Add standardized logging rather than print statements, log infra's love json so switch to structured as well.
- Add metrics so we could measure upstream latency, loading time, 
- Add more error/exception handling to all upstream calls and any dictionary access that assumes a key
- More robust tests, use a framework like pytest, and use mocks for calls made to extenal services that are subject to intermediary network and infra outages.
  - Add tests to API code , mock or use in-memory db
- Externalize any configuration that is subject to change between environments
 - Add backoff and retry logic to upstream calls (aiopoke might already do this)
 - Split stateless and stateful workloads.  Based off of domain, areas of expected change and bounded contexts.  Stateless could be the upstream client integration, another service would be the persistent datastore access.  This would allow for independent and cheap scaling of stateless clients from backend services used to interact with the datastore.  The data store could also be a separate service that is clustered and scaled as well.
 - If this was getting into the millions of many to many relationships than I would want to reduce and validate only the essential fields in a sane way.  If however the intent of the application was to become a datasource that heavily manipulated what was retrieved I would probably move that data model into a graph API with a graph datastore.
 - Test caching strategy, if workloads were split as explained above may need to move to distributed cache.
