"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Game_Type


class GameTypeView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game type

        Returns:
            Response -- JSON serialized game type
        """
        # After getting the game_type, it is passed to the serializer. 
        # Lastly, the serializer.data is passed to the Response as the response body. 
        # Using Response combines what we were doing with the _set_headers and wfile.write functions.
        try:
            game_type = Game_Type.objects.get(pk=pk)
            serializer = GameTypeSerializer(game_type)
            return Response(serializer.data)
        except Game_Type.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        # The serializer class determines how the Python data should be serialized to be sent 
        # back to the client
        

    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        # The game_types variable is now a list of GameTypeobjects
        game_types = Game_Type.objects.all()
        # The serializer class determines how the Python data should be serialized to be sent 
        # back to the client
        serializer = GameTypeSerializer(game_types, many=True)
        # This time adding many=True to let the serializer know that a list vs. a single 
        # object is to be serialized.
        return Response(serializer.data)

class GameTypeSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    # The Meta class hold the configuration for the serializer. We’re telling the serializer 
    # to use the GameType model and to include the id andlabel fields.
    class Meta:
        model = Game_Type
        fields = ('id', 'label')
        depth = 2