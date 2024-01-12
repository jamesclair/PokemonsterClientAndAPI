## Research

Named endpoints return following data structure:
    count: integer
    next: string
    previous: string
    results: list NamedAPIResource

At this time there are "count":1281 pokemon according to https://pokeapi.co/api/v2/pokemon call, the results list contains following objects:
{"name":"bulbasaur","url":"https://pokeapi.co/api/v2/pokemon/1/"},{"name":"ivysaur","url":"https://pokeapi.co/api/v2/pokemon/2/"}
    name: str
    url: str (the pokemon's detail URL)

Retrieval option comparison:
* create a cli from scratch
    * looks doable, might take awhile to write an async client for the bonus though.
    * would need to implement 
        * paging
        * logging
        * error handling
        * tests
        * model - dicts would be fine for MVP, but models will make excersize 2 easier.  They will need to be compatible with Django though
        * caching - performance improvement (optional)
* Use an existing API Wrapper Lib:
    * Python 3 with auto caching: PokeBase by Greg Hilmer
        * This looks to be the most stable with 10 issues that don't look fundamental to functionality not a ton of commits recently, but one in Feb and lots of stars
        * looks like pokemon are modeled well and can be accessed in dot notation as well, 
    * Python 2/3 with auto caching: Pokepy by Paul Hallett
        * When looking
    * Asynchronous Python wrapper with auto caching: aiopokeapi by beastmatser
        * https://github.com/beastmatser/aiopokeapi, Commits as recent as last week
        * no open issues, not very many stars, may have some risk to being fully usable
        * would allow data retrieval to happen in parallel
        * lots of usage documentation and total commits

### Conclusion
    
I'll probably go with a wrapper cli, no reason to rewrite with so many active options unless they suck.  I like the activity and documentation included with the aiopokeapi.  If that doesn't work, I can try the PokeBase wrapper.

I don't see a get_all_pokemon function or similar in the aiopokeapi wrapper, so we might need to send a simple synchronous request to grab all the pokemon, might be able to do without paging, by requesting more than total num of pokemon records, but will have to test.  Async is probably not necessary, but the returned data can be used to seed our calls for grabbing more detailed information about each pokemon.