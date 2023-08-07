from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import QuickNote, CategorizedNote, NoteType
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
import json


# Create your tests here.


class QuickNotesTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.test_author = get_user_model().objects.create_user(
            email="user@example.com", name="userexample", password="1234567890"
        )
        cls.test_author.save()
        cls.quicknote = QuickNote(
            note_author=cls.test_author,
            note_title="First Test Quick Note",
            note_body="First userexample test quick note",
        )
        cls.quicknote.save()
        cls.client.post(
            reverse("custom_login"),
            {
                "email": cls.test_author.email,
                "password": "1234567890",
            },
            format="json",
        )
        cls.token = Token.objects.get(user=cls.test_author).key

    def test_quick_note(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")
        response = self.client.get(
            reverse("all_quicknotes", kwargs={"category": "quick"}), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)[0]["id"], self.quicknote.id)
        self.assertEqual(
            json.loads(response.content)[0]["note_category"]["name"],
            self.quicknote.note_category.category,
        )
        self.assertEqual(
            json.loads(response.content)[0]["note_title"],
            self.quicknote.note_title,
        )
        self.assertEqual(
            json.loads(response.content)[0]["note_body"],
            self.quicknote.note_body,
        )

    def test_create_quick_note(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")
        url = reverse("create_new_note")
        response = self.client.post(
            url,
            {
                "note_category": 1,
                "note_title": "Another Test Quick Note",
                "note_body": "Just another test quick note!",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = reverse("quick_note_fetch", kwargs={"pk": "2"})
        response = self.client.get(
            url,
        )
        self.assertEqual(json.loads(response.content)["id"], 2)
        self.assertEqual(
            json.loads(response.content)["note_category"]["name"],
            "Quick Note",
        )
        self.assertEqual(
            json.loads(response.content)["note_title"], "Another Test Quick Note"
        )
        self.assertEqual(
            json.loads(response.content)["note_body"],
            "Just another test quick note!",
        )

    def test_quicknote_update(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")
        url = reverse("quick_note_update", kwargs={"pk": 1})
        response = self.client.put(
            url,
            {
                "note_category": 1,
                "note_title": "First Test Quick Note (updated)",
                "note_body": "First userexample test quick note updated",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = reverse("quick_note_fetch", kwargs={"pk": "1"})
        response = self.client.get(
            url,
        )
        self.assertEqual(json.loads(response.content)["id"], 1)
        self.assertEqual(
            json.loads(response.content)["note_category"]["name"],
            "Quick Note",
        )
        self.assertEqual(
            json.loads(response.content)["note_title"],
            "First Test Quick Note (updated)",
        )
        self.assertEqual(
            json.loads(response.content)["note_body"],
            "First userexample test quick note updated",
        )


class CategorizedNotesTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.test_author = get_user_model().objects.create_user(
            email="user@example.com", name="userexample", password="1234567890"
        )
        cls.test_author.save()
        NoteType.get_default_category_pk()
        cls.notetype = NoteType.objects.create(category="Test Category Type One")
        cls.categorized_note = CategorizedNote.objects.create(
            note_category=cls.notetype,
            note_author=cls.test_author,
            note_title="First Test Category Note",
            note_body="First userexample test category note",
        )
        cls.categorized_note.save()
        cls.client.post(
            reverse("custom_login"),
            {
                "email": cls.test_author.email,
                "password": "1234567890",
            },
            format="json",
        )
        cls.token = Token.objects.get(user=cls.test_author).key

    def test_category_note(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")
        response = self.client.get(
            reverse(
                "categorized_notes",
                kwargs={"category": "categorized", "category_id": self.notetype.id},
            ),
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content)[0]["id"], self.categorized_note.id
        )
        self.assertEqual(
            json.loads(response.content)[0]["note_category"]["name"],
            self.categorized_note.note_category.category,
        )
        self.assertEqual(
            json.loads(response.content)[0]["note_title"],
            self.categorized_note.note_title,
        )
        self.assertEqual(
            json.loads(response.content)[0]["note_body"],
            self.categorized_note.note_body,
        )

    def test_create_categorized_note(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")
        url = reverse("create_new_note")
        notetype = NoteType.objects.create(category="Second Test Category Note")
        notetype.save()
        response = self.client.post(
            url,
            {
                "note_category": notetype.id,
                "note_title": "Another Test Category  Note",
                "note_body": "Just another test category note!",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = reverse("categorized_note_fetch", kwargs={"pk": "2"})
        response = self.client.get(
            url,
        )
        self.assertEqual(json.loads(response.content)["id"], 2)
        self.assertEqual(
            json.loads(response.content)["note_category"]["name"],
            "Second Test Category Note",
        )
        self.assertEqual(
            json.loads(response.content)["note_title"], "Another Test Category  Note"
        )
        self.assertEqual(
            json.loads(response.content)["note_body"],
            "Just another test category note!",
        )

    def test_categorized_note_update(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")
        url = reverse("categorized_note_update", kwargs={"pk": 1})
        response = self.client.put(
            url,
            {
                "note_category": self.notetype.id,
                "note_title": "First Test Category Note (updated)",
                "note_body": "First userexample test categorized note updated",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = reverse("categorized_note_fetch", kwargs={"pk": "1"})
        response = self.client.get(
            url,
        )
        self.assertEqual(json.loads(response.content)["id"], 1)
        self.assertEqual(
            json.loads(response.content)["note_category"]["name"],
            "Test Category Type One",
        )
        self.assertEqual(
            json.loads(response.content)["note_title"],
            "First Test Category Note (updated)",
        )
        self.assertEqual(
            json.loads(response.content)["note_body"],
            "First userexample test categorized note updated",
        )
