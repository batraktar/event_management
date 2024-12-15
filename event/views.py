from rest_framework import viewsets, status, generics
from event.api.serializers import EventSerializer
from event.models import Event, EventRegistration
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.generics import DestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.core.mail import send_mail


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response({'error': 'Username or password are required'}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username is already taken'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password)
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['date', 'location', 'organizer']
    search_fields = ['title', 'description']
    ordering_fields = ['date']

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)


class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class EventDeleteView(DestroyAPIView):
    queryset = Event.objects.all()
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        try:
            event = self.get_object()
            if event.organizer != request.user:
                return Response(
                    {"error": "You can only delete events that you have created."},
                    status=status.HTTP_403_FORBIDDEN,
                )
            event.delete()
            return Response({"message": "Event deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Event.DoesNotExist:
            return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)


class EventRegistrationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, event_id):
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)

        if EventRegistration.objects.filter(user=request.user, event=event).exists():
            return Response({'error': 'Already registered'}, status=status.HTTP_400_BAD_REQUEST)

        send_mail(
            'Event Registration',
            f'You have registered for the event: {event.title}',
            'no-reply@eventmanagement.local',
            [request.user.email],
        )
        EventRegistration.objects.create(user=request.user, event=event)
        return Response({'message': 'Successfully registered for the event'}, status=status.HTTP_201_CREATED)


class UserRegisteredEventsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        registrations = Event.objects.filter(eventregistration__user=request.user)
        serializer = EventSerializer(registrations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
