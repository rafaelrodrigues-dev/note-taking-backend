from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from .serializers import NoteSerializer
from .models import Note


class Pagination(PageNumberPagination):
    page_size = 10


class NoteViewSet(ModelViewSet):
    serializer_class = NoteSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names =['get', 'options', 'head', 'post', 'patch', 'delete']
    pagination_class = Pagination

    def get_queryset(self):
        return Note.objects.filter(user_id=self.request.user.id)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
