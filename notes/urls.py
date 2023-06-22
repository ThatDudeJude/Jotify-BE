from django.urls import path
from .views import (
    notes_list,
    author_note_categories_list,
    note_categories_detail,
    user_note_types,
    quick_note_detail,
    categorized_note_detail,
    create_note,
)

urlpatterns = [
    path("all/", notes_list, name="all_notes"),
    path("all/<category>/", notes_list, name="all_quicknotes"),
    path("all/<category>/<int:category_id>/", notes_list, name="categorized_notes"),
    path(
        "all-notes-categories/",
        author_note_categories_list,
        name="note_categories_list",
    ),
    path(
        "note-categories/",
        note_categories_detail,
        name="create_new_note_category",
    ),
    path(
        "note-categories/<int:pk>/",
        note_categories_detail,
        name="note_categories_detail_delete",
    ),
    path("user-note-types/", user_note_types, name="get_all user_categories"),
    path("create/new/", create_note, name="create_new_note"),
    path("quick-note/<int:pk>/", quick_note_detail, name="quick_note_fetch"),
    path("quick-note/update/<int:pk>/", quick_note_detail, name="quick_note_update"),
    path("quick-note/delete/<int:pk>/", quick_note_detail, name="quick_note_delete"),
    path(
        "categorized-note/<int:pk>/",
        categorized_note_detail,
        name="categorized_note_fetch",
    ),
    path(
        "categorized-note/update/<int:pk>/",
        categorized_note_detail,
        name="categorized_note_update",
    ),
    path(
        "categorized-note/delete/<int:pk>/",
        categorized_note_detail,
        name="categorized_note_delete",
    ),
    # path("categorized-note/<int:pk>/", get_categorized_note, name="categorized_note"),
]
