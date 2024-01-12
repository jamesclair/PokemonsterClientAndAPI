from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Pokemon, Move, Type

class CreatePokemonView(APIView):
    def post(self, request):
        name = request.data.get('name')
        order = request.data.get('order')
        height = request.data.get('height')
        weight = request.data.get('weight')
        types = request.data.get('types', [])
        moves = request.data.get('moves', [])

        # Create the Pokémon instance
        pokemon = Pokemon.objects.create(
            name=name,
            order=order,
            height=height,
            weight=weight,
        )

        # Add associated types
        for type_name in types:
            pokemon_type, _ = Type.objects.get_or_create(name=type_name)
            pokemon.types.add(pokemon_type)

        # Add available moves
        for move_data in moves:
            move, _ = Move.objects.get_or_create(name=move_data['name'], power=move_data['power'])
            pokemon.moves.add(move)

        return Response({'message': 'Pokémon created successfully.'})


class CreateMoveView(APIView):
    def post(self, request):
        name = request.data.get('name')
        power = request.data.get('power')

        move, _ = Move.objects.get_or_create(name=name, power=power)

        return Response({'message': 'Move created successfully.'})


class LearnMoveView(APIView):
    def post(self, request):
        pokemon_id = request.data.get('pokemon_id')
        move_id = request.data.get('move_id')

        pokemon = Pokemon.objects.get(id=pokemon_id)
        move = Move.objects.get(id=move_id)

        pokemon.moves.add(move)

        return Response({'message': 'Move learned successfully.'})


class GetPokemonView(APIView):
    def get(self, request):
        p_type = request.query_params.get('p_type')
        p_move = request.query_params.get('p_move')

        pokemons = Pokemon.objects.all()

        if p_type:
            pokemons = pokemons.filter(types__name=p_type)

        if p_move:
            pokemons = pokemons.filter(moves__name=p_move)

        data = []
        for pokemon in pokemons:
            moves = pokemon.moves.values('name', 'power')
            data.append({
                'id': pokemon.id,
                'name': pokemon.name,
                'order': pokemon.order,
                'height': pokemon.height,
                'weight': pokemon.weight,
                'types': [t.name for t in pokemon.types.all()],
                'moves': list(moves)
            })

        return Response(data)

class GetBestMoveView(APIView):
    def get(self, request, pk):
        pokemon = Pokemon.objects.get(id=pk)
        best_move = pokemon.moves.order_by('-power').first()

        if best_move:
            return Response({'best_move': {
                'name': best_move.name,
                'power': best_move.power
            }})
        else:
            return Response({'message': 'No moves found for this Pokémon.'})

class GetSimilarPokemonView(APIView):
    def get(self, request, pk):
        pokemon = Pokemon.objects.get(id=pk)
        similar_pokemon = []

        # Find other Pokémon that share at least three moves with the specified Pokémon
        for other_pokemon in Pokemon.objects.exclude(id=pk):
            shared_moves = pokemon.moves.filter(name__in=other_pokemon.moves.values_list('name', flat=True))
            if shared_moves.count() >= 3:
                similar_pokemon.append({
                    'id': other_pokemon.id,
                    'name': other_pokemon.name,
                    'shared_moves': list(shared_moves.values('name', 'power'))
                })

        return Response(similar_pokemon)
