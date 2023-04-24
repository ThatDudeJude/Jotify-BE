from django.shortcuts import render
from base.models import CustomUser
from django.core.exceptions import ObjectDoesNotExist
from .models import QuickNote, CategorizedNote, NoteType
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework import permissions
from rest_framework.reverse import reverse
import json
from .serializers import (
    AuthorNotesSerializer,
    QuickNotesSerializer,
    CategorizedNotesSerializer,
    AuthorNoteCategoriesSerializer,
    NoteTypeSerializer,
)

# Create your views here.


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def author_note_categories_list(request):
    token = Token.objects.get(user=request.user)
    if request.auth.key == token.key:
        author = CustomUser.objects.get(email=request.user.email)
    else:
        return Response(
            {"message": "Unauthorized access attempted! Please log in."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    if request.method == "GET":
        serializers = AuthorNoteCategoriesSerializer(author)
        return Response(serializers.data, status=status.HTTP_200_OK)


@api_view(["POST", "DELETE"])
@permission_classes([permissions.IsAuthenticated])
def note_categories_detail(request, pk=None):
    token = Token.objects.get(user=request.user)
    if request.auth.key == token.key:
        author = CustomUser.objects.get(email=request.user.email)
    else:
        return Response(
            {"message": "Unauthorized access attempted! Please log in."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    if request.method == "POST":
        serializer = NoteTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        try:
            note_type = NoteType.objects.get(id=pk)
            note_type.delete()
            return Response(
                {"message": "Category delete successful"}, status=status.HTTP_200_OK
            )
        except ObjectDoesNotExist:
            return Response(
                {"message": "Note category not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def notes_list(request, category=None, category_id=None):
    token = Token.objects.get(user=request.user)
    if request.auth.key == token.key:
        author = CustomUser.objects.get(email=request.user.email)
    else:
        return Response(
            {"message": "Unauthorized access attempted! Please log in."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    if request.method == "GET":
        if not category:
            print(f"category: {category}")
            serializer = AuthorNotesSerializer(author)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif category == "quicknotes":
            serializer = QuickNotesSerializer(
                author.author_notes_quicknote.all(), many=True
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif category == "categorized":
            try:
                note_type = NoteType.objects.get(id=category_id)
                categorized_notes = author.author_notes_categorizednote.filter(
                    note_category=note_type, note_author=author
                )
                print(categorized_notes)
                serializer = CategorizedNotesSerializer(categorized_notes, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response(
                    {"message": "Note category not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            return Response(
                {"message": "Notes not found"}, status=status.HTTP_404_NOT_FOUND
            )


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def create_note(request):
    token = Token.objects.get(user=request.user)
    if request.auth.key == token.key:
        author = CustomUser.objects.get(email=request.user.email)
    else:
        return Response(
            {"message": "Unauthorized access"},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    available_note_types = [note_type.category for note_type in NoteType.objects.all()][
        1:
    ]

    serializer_is_set = False
    if request.data["note_category"] == "Quick Note":
        serializer = QuickNotesSerializer(
            data=request.data, context={"request": request}
        )
        serializer_is_set = True
    elif request.data["note_category"] in available_note_types:
        # Debug note
        # To remove after building ui as id will be provided by default in the request

        data = json.dumps(request.data)
        data = json.loads(data)
        category_id = NoteType.objects.get(category=data["note_category"]).id
        data["note_category"] = category_id
        print("category:", data["note_category"])
        serializer = CategorizedNotesSerializer(data=data, context={"request": request})
        serializer_is_set = True
    if serializer_is_set:
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(
            {"message": "Note category wasn't well specified"},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([permissions.IsAuthenticated])
def quick_note_detail(request, pk=None):
    token = Token.objects.get(user=request.user)
    if request.auth.key == token.key:
        try:
            author = CustomUser.objects.get(email=request.user.email)
            note = QuickNote.objects.get(id=pk, note_author=author)
        except ObjectDoesNotExist:
            return Response(
                {"message": "User's quick note not found "},
                status=status.HTTP_404_NOT_FOUND,
            )
    else:
        return Response(
            {"message": "Unauthorized access attempted! Please log in."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    if request.method == "GET":
        serializer = QuickNotesSerializer(note)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "PUT":
        serializer = QuickNotesSerializer(
            note, data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        note.delete()
        return Response(
            {"message": "Quick note deleted successfully"}, status=status.HTTP_200_OK
        )


@api_view(["GET", "DELETE", "PUT"])
@permission_classes([permissions.IsAuthenticated])
def categorized_note_detail(request, pk):
    token = Token.objects.get(user=request.user)
    if request.auth.key == token.key:
        try:
            author = CustomUser.objects.get(email=request.user.email)
            note = CategorizedNote.objects.get(id=pk, note_author=author)
        except ObjectDoesNotExist:
            return Response(
                {"message": "User's categorized note not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
    else:
        return Response(
            {"message": "Unauthorized access attempted! Please log in."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    if request.method == "GET":
        serializer = CategorizedNotesSerializer(note)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "PUT":
        data = json.dumps(request.data)
        data = json.loads(data)
        category_id = NoteType.objects.get(category=data["note_category"]).id
        data["note_category"] = category_id
        serializer = CategorizedNotesSerializer(
            note, data=data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        note.delete()
        return Response(
            {"message": "Categorized note deleted successfully"},
            status=status.HTTP_200_OK,
        )
