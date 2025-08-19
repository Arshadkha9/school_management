from rest_framework import generics, permissions
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
    

@api_view(['GET','POST'])
def createParentData(request,pk=None,format=None):
    print(request,"type of request",type(request))
    print("requestdata",request.data,"type of data",type(request.data))
    if request.method == 'POST':
        serializer = ParentsDataSerializer(data=request.data)
        print("serializerdata",serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        if pk:  # fetch single parent
            try:
                parent = ParentsData.objects.get(pk=pk)
                serializer = ParentsDataSerializer(parent)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ParentsData.DoesNotExist:
                return Response({"error": "Parent not found"}, status=status.HTTP_404_NOT_FOUND)
        else:  # fetch all parents
            parents = ParentsData.objects.all()
            serializer = ParentsDataSerializer(parents, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
    