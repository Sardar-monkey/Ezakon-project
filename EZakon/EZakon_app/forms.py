from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Comment, Law, LawComment


class NewUser(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "email",
            "username",
            "first_name",
            "last_name",
            "password1",
            "password2",
        ]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        widgets = {
            "text": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Напишите ваш отзыв...",
                    "class": "form-control",
                }
            ),
        }
        labels = {
            "text": "Ваш отзыв",
        }


class LawSearchForm(forms.Form):
    """Форма для поиска и фильтрации законов"""

    SORT_CHOICES = [
        ("-date_published", "Новые сначала"),
        ("date_published", "Старые сначала"),
        ("-views_count", "По популярности"),
        ("title", "По названию (А-Я)"),
        ("-title", "По названию (Я-А)"),
    ]

    query = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Поиск по названию, номеру или содержанию...",
                "class": "form-control",
                "style": "padding: 10px; border-radius: 5px; border: 1px solid #ddd;",
            }
        ),
    )

    category = forms.ChoiceField(
        required=False,
        choices=[("", "Все категории")] + list(Law.CATEGORY_CHOICES),
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "style": "padding: 10px; border-radius: 5px; border: 1px solid #ddd;",
            }
        ),
    )

    status = forms.ChoiceField(
        required=False,
        choices=[("", "Все статусы")] + list(Law.STATUS_CHOICES),
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "style": "padding: 10px; border-radius: 5px; border: 1px solid #ddd;",
            }
        ),
    )

    is_active = forms.ChoiceField(
        required=False,
        choices=[("", "Все законы"), ("true", "Только действующие")],
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "style": "padding: 10px; border-radius: 5px; border: 1px solid #ddd;",
            }
        ),
    )

    sort_by = forms.ChoiceField(
        required=False,
        choices=SORT_CHOICES,
        initial="-date_published",
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "style": "padding: 10px; border-radius: 5px; border: 1px solid #ddd;",
            }
        ),
    )


class LawCommentForm(forms.ModelForm):
    """Форма для добавления комментариев к закону"""

    class Meta:
        model = LawComment
        fields = ["text"]
        widgets = {
            "text": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Напишите ваш комментарий или примечание к закону...",
                    "class": "form-control",
                    "style": "padding: 10px; border-radius: 5px; border: 1px solid #ddd;",
                }
            ),
        }
        labels = {
            "text": "Ваш комментарий",
        }
