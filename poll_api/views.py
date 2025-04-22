from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated

from polls.models import Poll
from .serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .pagination import CustomPageNumberPagination
from rest_framework.generics import get_object_or_404
from .permissions import IsOwnerOrReadOnly


class PollListView(APIView, CustomPageNumberPagination):
    serializer_class = PollSerializers

    def get(self, request):
        polls = Poll.objects.all()
        paginated_polls = self.paginate_queryset(polls, request)
        serializer = PollSerializers(instance=paginated_polls, many=True)
        return self.get_paginated_response(serializer.data)


class UserPollsListView(APIView, CustomPageNumberPagination):
    serializer_class = PollSerializers
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        polls = Poll.objects.filter(owner=request.user)
        paginated_polls = self.paginate_queryset(polls, request)
        serializer = PollSerializers(instance=paginated_polls, many=True)
        return self.get_paginated_response(serializer.data)


class PollCreateView(APIView):
    serializer_class = PollSerializers
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = PollSerializers(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class PollDetailView(APIView):
    serializer_class = PollSerializers
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        poll = get_object_or_404(Poll, id=pk)
        serializer = PollSerializers(instance=poll)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PollEditView(APIView):
    serializer_class = PollSerializers
    # parser_classes = (MultiPartParser,)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def get_object(self, pk):
        obj = get_object_or_404(Poll, id=pk)
        self.check_object_permissions(self.request, obj)
        return obj

    def put(self, request, pk):
        poll = self.get_object(pk)
        serializer = PollSerializers(poll, data=request.data, partial=True)
        if serializer.is_valid():
            # serializer.update(instance=poll, validated_data=serializer.validated_data)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class PollDeleteView(APIView):
    serializer_class = PollSerializers
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    def get_object(self, pk):
        obj = get_object_or_404(Poll, id=pk)
        self.check_object_permissions(self.request, obj)
        return obj

    def delete(self, request, pk):
        poll = self.get_object(pk)
        poll.delete()
        return Response({'response': 'Poll has been deleted successfully'} ,status=status.HTTP_200_OK)
