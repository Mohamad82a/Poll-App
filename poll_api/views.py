from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from polls.models import Poll
from .serializers import PollSerializers
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

class PollDetailView(APIView):
    serializer_class = PollSerializers
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        poll = get_object_or_404(Poll, id=pk)
        serializer = PollSerializers(instance=poll)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PollEditView(APIView):
    serializer_class = PollSerializers
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def get_object(self, pk):
        obj = get_object_or_404(Poll, id=pk)
        self.check_object_permissions(self.request, obj)
        return obj

    def put(self, request, pk):
        poll = self.get_object(pk)
        serializer = PollSerializers(instance=poll, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
