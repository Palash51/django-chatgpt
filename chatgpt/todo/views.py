from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from scripts.producer import send_website_data
from .serializers import TodoItemSerializer
from .models import TodoItem


# class based views

class ScrapeWebSiteData(APIView):
    """
    Scrape website data
    """
    def post(self, request):
        website_list = request.data.get('website_list')
        send_website_data(website_list)
        return HttpResponse('Background job triggered successfully!')



class TodoList(APIView):
    def get(self, request):
        todos = TodoItem.objects.all()
        serializer = TodoItemSerializer(todos, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TodoItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TodoDetail(APIView):
    def get_object(self, pk):
        try:
            return TodoItem.objects.get(pk=pk)
        except TodoItem.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        todo = self.get_object(pk)
        serializer = TodoItemSerializer(todo)
        return Response(serializer.data)

    def put(self, request, pk):
        todo = self.get_object(pk)
        serializer = TodoItemSerializer(todo, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        todo = self.get_object(pk)
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

