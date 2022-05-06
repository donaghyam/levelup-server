"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Events
from levelupapi.models import Games
from levelupapi.models.gamer import Gamer
from django.core.exceptions import ValidationError


class EventView(ViewSet):
    """Level up events view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single event

        Returns:
            Response -- JSON serialized event
        """
        # After getting the event, it is passed to the serializer. 
        # Lastly, the serializer.data is passed to the Response as the response body. 
        # Using Response combines what we were doing with the _set_headers and wfile.write functions.
        try:
            event = Events.objects.get(pk=pk)
            serializer = EventSerializer(event)
            return Response(serializer.data)
        except Events.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        # The serializer class determines how the Python data should be serialized to be sent 
        # back to the client

    def list(self, request):
        """Handle GET requests to get all events

        Returns:
            Response -- JSON serialized list of events
        """
        # The event variable is now a list of Event objects
        events = Events.objects.all()
        
        # The request from the method parameters holds all the information for the request from the client. 
        # The request.query_params is a dictionary of any query parameters that were in the url. Using the 
        # .get method on a dictionary is a safe way to find if a key is present on the dictionary. 
        # If the 'type' key is not present on the dictionary it will return None.
        event_game = request.query_params.get('game', None)
        if event_game is not None:
            events = events.filter(game_id=event_game)
            
        # The serializer class determines how the Python data should be serialized to be sent 
        # back to the client
        serializer = EventSerializer(events, many=True)
        # This time adding many=True to let the serializer know that a list vs. a single 
        # object is to be serialized.
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """
        # the key in quotations must match the key of the object being entered by the client
       
        organizer = Gamer.objects.get(user=request.auth.user)
        
        # Instead of making a new instance of the Event model, the request.data dictionary is 
        # passed to the new serializer as the data. The keys on the dictionary must match what 
        # is in the fields on the serializer. After creating the serializer instance, call is_valid 
        # o make sure the client sent valid data. If the code passes validation, then the save method 
        # will add the game to the database and add an id to the serializer.
        serializer = CreateEventsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(organizer=organizer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """
        event = Events.objects.get(pk=pk)
        serializer = CreateEventsSerializer(event, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for events
    """
    # The Meta class hold the configuration for the serializer. We’re telling the serializer 
    # to use the Event model and to include the id andlabel fields.
    class Meta:
        model = Events
        fields = ('id', 'description', 'date', 'time', 'game', 'organizer')
        depth = 4
        
class CreateEventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = ['id', 'description', 'date', 'time', 'game']