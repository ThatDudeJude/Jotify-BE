from django.contrib import admin
from .models import QuickNote, CategorizedNote, NoteType, Note
from .forms import CreateQuickNoteForm, CreateCategorizedNoteForm


@admin.register(QuickNote)
class QuickNoteAdmin(admin.ModelAdmin):
    form = CreateQuickNoteForm
    list_display = [
        "note_title",
        "note_category",
        "note_author",
        "time_modified",
    ]
    list_filter = ("note_author",)
    date_hierarchy = "time_modified"

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "note_category",
                    "note_title",
                    "note_body",
                    "note_author",
                ),
            },
        ),
    )


@admin.register(CategorizedNote)
class CategorizedNoteAdmin(admin.ModelAdmin):
    form = CreateCategorizedNoteForm
    list_display = [
        "note_title",
        "note_category",
        "note_author",
        "time_modified",
    ]
    list_filter = ("note_author",)
    date_hierarchy = "time_modified"

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "note_category",
                    "note_title",
                    "note_body",
                    "note_author",
                ),
            },
        ),
    )


@admin.register(NoteType)
class NoteTypeAdmin(admin.ModelAdmin):
    list_display = ["id", "category"]
