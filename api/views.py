from django.shortcuts import render
from django.http import JsonResponse
from api.models import User

from api.serializer import MyTokenObtainPairSerializer, RegisterSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import MultiPartParser, FormParser

from api import serializer as api_serializer
from api import models as api_models
from django.db import IntegrityError
from django.http import FileResponse
from django.views.static import serve
from django.conf import settings
import os

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    

class RegisterView(generics.CreateAPIView):
    queryset = api_models.User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
    

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = api_serializer.ProfileSerializer
    
    def get(self, request):
        user = request.user
        api_models.Profile.objects.get_or_create(user=user)
        serializer = api_serializer.UserSerializer(user)
        return Response(serializer.data)


class ProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        profile = request.user.profile
        serializer = api_serializer.ProfileUpdateSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class BookListCreateView(APIView):
    parser_classes = (MultiPartParser, FormParser)  # Add parsers for file uploads

    def get(self, request):
        books = api_models.Book.objects.all()
        serializer = api_serializer.BookSerializer(books, many=True)
        return Response(serializer.data)

    def post(self, request):
        permission_classes = [IsAuthenticated]
        serializer = api_serializer.BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(uploaded_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class BookDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, book_id):
        try:
            book = api_models.Book.objects.get(id=book_id, uploaded_by=request.user)
            book.delete()
            return Response({"message": "Book deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except api_models.Book.DoesNotExist:
            return Response({"error": "Book not found or you don't have permission"}, status=status.HTTP_404_NOT_FOUND)


class BookDetailView(APIView):
    def get(self, request, book_id):
        try:
            book = api_models.Book.objects.get(id=book_id)
            serializer = api_serializer.BookSerializer(book)
            response = Response(serializer.data)
            response['X-Frame-Options'] = 'SAMEORIGIN'  # Override for this view
            return response
        except api_models.Book.DoesNotExist:
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
        

class UserBooksList(APIView):
    permission_classes = [IsAuthenticated] 

    def get(self, request):
        # Filter books by the authenticated user
        books = api_models.Book.objects.filter(uploaded_by=request.user)
        serializer = api_serializer.BookSerializer(books, many=True)
        return Response(serializer.data)           
    
    
class ReadingListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        reading_lists = api_models.ReadingList.objects.filter(user=request.user)
        serializer = api_serializer.ReadingListSerializer(reading_lists, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = api_serializer.ReadingListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReadingListDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, list_id):
        try:
            reading_list = api_models.ReadingList.objects.get(id=list_id, user=request.user)
            serializer = api_serializer.ReadingListSerializer(reading_list)
            return Response(serializer.data)
        except api_models.ReadingList.DoesNotExist:
            return Response({"error": "Reading list not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, list_id):
        try:
            reading_list = api_models.ReadingList.objects.get(id=list_id, user=request.user)
            serializer = api_serializer.ReadingListSerializer(reading_list, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except api_models.ReadingList.DoesNotExist:
            return Response({"error": "Reading list not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, list_id):
        try:
            reading_list = api_models.ReadingList.objects.get(id=list_id, user=request.user)
            reading_list.delete()
            return Response({"message": "Reading list deleted"}, status=status.HTTP_204_NO_CONTENT)
        except api_models.ReadingList.DoesNotExist:
            return Response({"error": "Reading list not found"}, status=status.HTTP_404_NOT_FOUND)


# class ReadingListItemView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, list_id):
#         try:
#             reading_list = api_models.ReadingList.objects.get(id=list_id, user=request.user)
#             serializer = api_serializer.ReadingListItemSerializer(data=request.data)
#             if serializer.is_valid():
#                 serializer.save(reading_list=reading_list)
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except api_models.ReadingList.DoesNotExist:
#             return Response({"error": "Reading list not found"}, status=status.HTTP_404_NOT_FOUND)

#     def delete(self, request, list_id, item_id):
#         try:
#             reading_list = api_models.ReadingList.objects.get(id=list_id, user=request.user)
#             item = api_models.ReadingListItem.objects.get(id=item_id, reading_list=reading_list)
#             item.delete()
#             return Response({"message": "Book removed from reading list"}, status=status.HTTP_204_NO_CONTENT)
#         except api_models.ReadingList.DoesNotExist:
#             return Response({"error": "Reading list not found"}, status=status.HTTP_404_NOT_FOUND)
#         except api_models.ReadingListItem.DoesNotExist:
#             return Response({"error": "Item not found in this reading list"}, status=status.HTTP_404_NOT_FOUND)


class ReadingListItemView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, list_id):
        try:
            reading_list = api_models.ReadingList.objects.get(id=list_id, user=request.user)
            serializer = api_serializer.ReadingListItemSerializer(data=request.data)
            if serializer.is_valid():
                book_id = serializer.validated_data['book'].id
                if not api_models.Book.objects.filter(id=book_id).exists():
                    return Response({"error": "Book does not exist"}, status=status.HTTP_400_BAD_REQUEST)
                try:
                    serializer.save(reading_list=reading_list)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                except IntegrityError:
                    return Response(
                        {"error": "This book is already in the reading list"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except api_models.ReadingList.DoesNotExist:
            return Response({"error": "Reading list not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, list_id, item_id):
        try:
            reading_list = api_models.ReadingList.objects.get(id=list_id, user=request.user)
            item = api_models.ReadingListItem.objects.get(id=item_id, reading_list=reading_list)
            item.delete()
            return Response({"message": "Book removed from reading list"}, status=status.HTTP_204_NO_CONTENT)
        except api_models.ReadingList.DoesNotExist:
            return Response({"error": "Reading list not found"}, status=status.HTTP_404_NOT_FOUND)
        except api_models.ReadingListItem.DoesNotExist:
            return Response({"error": "Item not found in this reading list"}, status=status.HTTP_404_NOT_FOUND)
        
        
# Get All Routes

@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/token/',
        '/api/register/',
        '/api/token/refresh/'
    ]
    return Response(routes)