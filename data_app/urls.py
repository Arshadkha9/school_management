from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenObtainPairView
from .authentication import CustomTokenObtainPairSerializer
from .views import UserListView, UserCreateView,createParentData
from rest_framework.routers import DefaultRouter

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

router=DefaultRouter()
router.register(r'parentdata', createParentData)

urlpatterns = [
    path('users/', UserListView.as_view(), name='user-list'),
    path('register/', UserCreateView.as_view(), name='user-register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('parentapi/', include(router.urls)),

]

