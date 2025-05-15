from rest_framework import generics, permissions,viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from .models import UserLogin,ParentsData
from .serializers import UserLoginSerializer, UserCreateSerializer,ParentsDataSerializer


from rest_framework.decorators import api_view


class UserListView(generics.ListAPIView):
    queryset = UserLogin.objects.all()
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.IsAdminUser]


class UserCreateView(generics.CreateAPIView):
    queryset = UserLogin.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny]


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'id': user.pk,
            'email': user.email
        })
    

# @api_view(['POST'])
# def createParentData(request):
#     serializer = ParentsDataSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class createParentData(viewsets.ModelViewSet):
    queryset =ParentsData.objects.all()
    serializer_class=ParentsDataSerializer