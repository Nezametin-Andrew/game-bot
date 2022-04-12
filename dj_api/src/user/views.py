from django.shortcuts import redirect
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response

from .models import UserProfile
from .serializers import UserProfileSerializer, UserDetailSerializer
from services.utils import CreatingUserHandler


class CreateProfileApiView(APIView):

    def post(self, request, *args, **kwargs):
        #user = CreatingUserHandler(method='create', serializer=UserProfileSerializer, data=request.data).process()
        #return Response(user.data)

        serialize = UserProfileSerializer(data=request.data)
        print(serialize.is_valid())
        print(serialize.errors)
        #print(serialize.validated_data)
        print(serialize.data)
        return Response({})


class ListUserApiView(ListAPIView):

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class DetailUserApiView(RetrieveAPIView):

    queryset = UserProfile.objects.all()
    serializer_class = UserDetailSerializer
