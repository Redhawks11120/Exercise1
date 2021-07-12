from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .serializers import UserSerializer, RegisterSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework import status, generics
from rest_framework.response import Response
from knox.models import AuthToken
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import login
from rest_framework.views import APIView
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, get_object_or_404
import requests
from django.urls import reverse

class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'data': RegisterSerializer(user, context=self.get_serializer_context()).data,
            'code': status.HTTP_201_CREATED,
            'token': AuthToken.objects.create(user)[1]
        })


class LoginAPI(KnoxLoginView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)


class GetAllUser(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        list_user = User.objects.all()
        my_data = UserSerializer(list_user, many=True)
        return Response({
            'data': my_data.data,
            'status': status.HTTP_200_OK,
            'message': 'Get all user successfully!'
        })

class GetUser(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request, id):
        user = get_object_or_404(User,id=id)
        return Response(UserSerializer(user).data)
def index(request):
    return render(request, 'users/Login.html')


def login_user(request):
    if request.method == 'POST':
        login_json = requests.post('http://127.0.0.1:8000/api/login/', data=request.POST)
        login_text = login_json.json()
        headers = {'Authorization': 'Token ' + login_text['token']}
        data_json = requests.get('http://127.0.0.1:8000/api/all/', headers=headers, params=request.GET)
        data = data_json.json()
        context = {
            'data': data['data'],
        }
        if data['status'] == 200:
            return render(request, 'users/Home.html', context)
        else:
            return HttpResponse('Not OK')
    return HttpResponseRedirect(reverse('index'))


def register_user(request):
    if request.method == 'POST':
        register_json = requests.post('http://127.0.0.1:8000/api/register/', data=request.POST)
        return HttpResponseRedirect(reverse('login'))
    return render(request, 'users/Register.html')