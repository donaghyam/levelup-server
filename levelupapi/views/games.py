"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Games
from levelupapi.models import Gamer
from levelupapi.models import Game_Type
from django.core.exceptions import ValidationError


class GameView(ViewSet):
    """Level up events view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game

        Returns:
            Response -- JSON serialized game
        """
        # After getting the event, it is passed to the serializer. 
        # Lastly, the serializer.data is passed to the Response as the response body. 
        # Using Response combines what we were doing with the _set_headers and wfile.write functions.
        try:
            game = Games.objects.get(pk=pk)
            serializer = GameSerializer(game)
            return Response(serializer.data)
        except Games.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        # The serializer class determines how the Python data should be serialized to be sent 
        # back to the client
        

    def list(self, request):
        """Handle GET requests to get all games

        Returns:
            Response -- JSON serialized list of games
        """
        # The game variable is now a list of Game objects
        games = Games.objects.all()
        
        # The request from the method parameters holds all the information for the request from the client. 
        # The request.query_params is a dictionary of any query parameters that were in the url. Using the 
        # .get method on a dictionary is a safe way to find if a key is present on the dictionary. 
        # If the 'type' key is not present on the dictionary it will return None.
        game_type = request.query_params.get('type', None)
        if game_type is not None:
            games = games.filter(game_type_id=game_type)
            
        # The serializer class determines how the Python data should be serialized to be sent 
        # back to the client
        serializer = GameSerializer(games, many=True)
        # This time adding many=True to let the serializer know that a list vs. a single 
        # object is to be serialized.
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized game instance
        """
        # Instead of making a new instance of the Game model, the request.data dictionary is 
        # passed to the new serializer as the data. The keys on the dictionary must match what 
        # is in the fields on the serializer. After creating the serializer instance, call is_valid 
        # o make sure the client sent valid data. If the code passes validation, then the save method 
        # will add the game to the database and add an id to the serializer.
        gamer = Gamer.objects.get(user=request.auth.user)
        serializer = CreateGameSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(gamer=gamer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """
        game = Games.objects.get(pk=pk)
        serializer = CreateGameSerializer(game, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for games
    """
    # The Meta class hold the configuration for the serializer. We’re telling the serializer 
    # to use the Games model and to include the id andlabel fields.
    class Meta:
        model = Games
        fields = ('id', 'game_type', 'title', 'maker', 'gamer', 'number_of_players', 'skill_level')
        depth = 2
        
class CreateGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Games
        # Since the gamer comes from the Auth header it will not be in the request body
        fields = ['id', 'title', 'maker', 'number_of_players', 'skill_level', 'game_type']