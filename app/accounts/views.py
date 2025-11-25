from rest_framework.viewsets import ModelViewSet
from .serializers import UserSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

User = get_user_model()


class UserModelViewSet(ModelViewSet):
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'options', 'head', 'post', 'patch', 'delete']
    
    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)
