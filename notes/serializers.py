from rest_framework import serializers
from .models import CategorizedNote, QuickNote, NoteType
from base.models import CustomUser
from operator import itemgetter
from itertools import chain


class NoteTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoteType
        fields = ["category"]


class CategorizedNotesSerializer(serializers.ModelSerializer):
    note_author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = CategorizedNote
        fields = [
            "id",
            "note_category",
            "note_title",
            "note_body",
            "time_modified",
            "note_author",
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["note_category"] = instance.note_category.category
        return representation

    def create(self, validated_data):

        print(f"validated {validated_data}")
        return super().create(validated_data)


class QuickNotesSerializer(serializers.ModelSerializer):
    note_category = serializers.SerializerMethodField()
    note_author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = QuickNote
        fields = [
            "id",
            "note_category",
            "note_title",
            "note_body",
            "time_modified",
            "note_author",
        ]

    def get_note_category(self, note):
        return NoteTypeSerializer(note.note_category).data["category"]


class AuthorNotesSerializer(serializers.ModelSerializer):
    author_notes = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ["name", "email", "id", "author_notes"]

    def get_author_notes(self, author):
        all_notes = []
        all_notes.extend(
            [
                {**QuickNotesSerializer(quicknote).data}
                for quicknote in author.author_notes_quicknote.all()
            ]
        )
        all_notes.extend(
            [
                {**CategorizedNotesSerializer(categorizednote).data}
                for categorizednote in author.author_notes_categorizednote.all()
            ]
        )
        return sorted(all_notes, key=itemgetter("time_modified"), reverse=True)


class AuthorNoteCategoriesSerializer(serializers.ModelSerializer):
    all_user_categories = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ["all_user_categories"]

    def get_all_user_categories(self, user):
        categories_list = []
        for note in user.author_notes_categorizednote.all():
            categories_list.append(
                {"category": note.note_category.category, "id": note.note_category.id}
            )
        for note in user.author_notes_quicknote.all():
            categories_list.append(
                {"category": note.note_category.category, "id": note.note_category.id}
            )
        return list({n["id"]: n for n in categories_list}.values())


class NoteTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoteType
        fields = "__all__"
