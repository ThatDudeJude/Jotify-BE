from django.db import models
from base.models import CustomUser

# Create your models here.


class Note(models.Model):
    author = models.ForeignKey(
        to=CustomUser,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        name="note_author",
        related_name="author_%(app_label)s_%(class)s",
    )
    title = models.CharField(blank=False, name="note_title", max_length=50)
    body = models.TextField(blank=False, name="note_body", max_length=100)
    created = models.DateTimeField(auto_now_add=True, name="time_created")
    modified = models.DateTimeField(auto_now=True, name="time_modified")

    class Meta:
        abstract = True
        ordering = ["-time_modified"]


class NoteType(models.Model):
    category = models.CharField(max_length=25, blank=False)
    creator_id = models.IntegerField(blank=False, null=False, default=0)

    @classmethod
    def get_default_category_pk(cls):
        default_category, created = cls.objects.get_or_create(category="Quick Note")
        return default_category.pk

    def __str__(self):
        return f"id: {self.id}, category: {self.category}"


class QuickNote(Note):
    category = models.ForeignKey(
        to=NoteType,
        on_delete=models.CASCADE,
        default=NoteType.get_default_category_pk,
        name="note_category",
    )


class CategorizedNote(Note):
    category = models.ForeignKey(
        to=NoteType, on_delete=models.CASCADE, name="note_category"
    )
