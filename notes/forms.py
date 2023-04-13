from django.forms.models import ModelForm
from .models import CategorizedNote, QuickNote


class CreateQuickNoteForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CreateQuickNoteForm, self).__init__(*args, **kwargs)
        self.fields["note_category"].disabled = True

    class Meta:
        model = QuickNote
        fields = [
            "note_category",
            "note_title",
            "note_body",
            "note_author",
        ]


class CreateCategorizedNoteForm(ModelForm):
    class Meta:
        model = CategorizedNote
        fields = [
            "note_category",
            "note_title",
            "note_body",
            "note_author",
        ]
