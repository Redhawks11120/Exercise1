from .views import LoginAPI, RegisterAPI, GetAllUser, login_user, index, register_user, GetUser
from django.urls import path
from knox.views import LogoutView

urlpatterns = [
    path('', index, name='index'),
    path('api/register/', RegisterAPI.as_view(), name='api-register'),
    path('api/login/', LoginAPI.as_view(), name='api-login'),
    path('api/logout/', LogoutView.as_view(), name='api-logout'),
    path('api/all/', GetAllUser.as_view(), name='api-all'),
    path('api/get/<int:id>/', GetUser.as_view(), name='api-get'),
    path('login', login_user, name='login'),
    path('register', register_user, name='register'),
]