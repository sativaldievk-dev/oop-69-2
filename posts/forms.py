from django import forms

from .models import Category, Post, Quote


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "description"]
        labels = {
            "name": "Название категории",
            "description": "Описание",
        }
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Например, Фантастика",
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Краткое описание категории",
                "rows": 4,
            }),
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["category", "title", "description"]
        labels = {
            "category": "Категория",
            "title": "Название произведения",
            "description": "Текст произведения",
        }
        widgets = {
            "category": forms.Select(attrs={"class": "form-control"}),
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Например, Зимний вечер",
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Напиши рассказ, стихотворение или другой текст...",
                "rows": 8,
            }),
        }


class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ["post", "text", "author"]
        labels = {
            "post": "Связанная публикация",
            "text": "Текст цитаты",
            "author": "Автор",
        }
        widgets = {
            "post": forms.Select(attrs={"class": "form-control"}),
            "text": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Напиши цитату...",
                "rows": 5,
            }),
            "author": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Имя автора",
            }),
        }
