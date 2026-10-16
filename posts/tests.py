from django.test import TestCase
from django.urls import reverse

from .forms import CategoryForm, PostForm, QuoteForm
from .models import Category, Post, Quote


class PostFormTests(TestCase):
    def test_category_form_saves_category(self):
        form = CategoryForm(data={
            "name": "Фантастика",
            "description": "Фантастические произведения",
        })

        self.assertTrue(form.is_valid())
        category = form.save()

        self.assertEqual(category.name, "Фантастика")
        self.assertEqual(category.description, "Фантастические произведения")

    def test_post_form_saves_category_relation(self):
        category, _ = Category.objects.get_or_create(name="Стихи")
        form = PostForm(data={
            "category": category.pk,
            "title": "Зимний вечер",
            "description": "Буря мглою небо кроет...",
        })

        self.assertTrue(form.is_valid())
        post = form.save()

        self.assertEqual(post.category, category)

    def test_add_category_view_creates_category(self):
        response = self.client.post(reverse("add_category"), {
            "name": "Новые рассказы",
            "description": "Короткая проза",
        })

        self.assertRedirects(response, reverse("post_list"))
        self.assertTrue(
            Category.objects.filter(
                name="Новые рассказы",
                description="Короткая проза",
            ).exists()
        )

    def test_quote_form_saves_post_relation(self):
        post = Post.objects.create(title="Повесть", description="Текст")
        form = QuoteForm(data={
            "post": post.pk,
            "text": "Короткая цитата",
            "author": "Автор",
        })

        self.assertTrue(form.is_valid())
        quote = form.save()

        self.assertEqual(quote.post, post)

    def test_post_list_accepts_model_form(self):
        category, _ = Category.objects.get_or_create(name="Рассказы")

        response = self.client.post(reverse("post_list"), {
            "kind": "post",
            "category": category.pk,
            "title": "Новая публикация",
            "description": "Текст публикации",
        })

        self.assertRedirects(response, reverse("post_list"))
        self.assertTrue(
            Post.objects.filter(
                category=category,
                title="Новая публикация",
            ).exists()
        )

    def test_quote_list_uses_related_post(self):
        post = Post.objects.create(title="Книга", description="Текст")
        Quote.objects.create(post=post, text="Связанная цитата")

        response = self.client.get(reverse("quote_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Книга")
