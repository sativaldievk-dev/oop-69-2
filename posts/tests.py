from django.contrib.auth import get_user_model
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


class PostOwnershipTests(TestCase):
    def setUp(self):
        self.owner = get_user_model().objects.create_user(
            username="post-owner",
            password="test-password",
        )
        self.other_user = get_user_model().objects.create_user(
            username="another-user",
            password="test-password",
        )

    def test_my_posts_requires_login(self):
        response = self.client.get(reverse("my_posts"))

        self.assertRedirects(
            response,
            f"/accounts/login/?next={reverse('my_posts')}",
        )

    def test_my_posts_shows_only_current_users_posts(self):
        own_post = Post.objects.create(
            title="Моя публикация",
            description="Мой текст",
            created_by=self.owner,
        )
        Post.objects.create(
            title="Чужая публикация",
            description="Чужой текст",
            created_by=self.other_user,
        )
        Post.objects.create(
            title="Старая публикация без владельца",
            description="Текст без владельца",
        )
        self.client.force_login(self.owner)

        response = self.client.get(reverse("my_posts"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, own_post.title)
        self.assertNotContains(response, "Чужая публикация")
        self.assertNotContains(response, "Старая публикация без владельца")

    def test_authenticated_post_creation_records_owner(self):
        self.client.force_login(self.owner)

        response = self.client.post(reverse("post_list"), {
            "kind": "post",
            "title": "Созданный мной пост",
            "description": "Текст поста",
        })

        self.assertRedirects(response, reverse("post_list"))
        post = Post.objects.get(title="Созданный мной пост")
        self.assertEqual(post.created_by, self.owner)

    def test_add_publication_records_authenticated_owner(self):
        self.client.force_login(self.owner)

        response = self.client.post(reverse("add_publication"), {
            "title": "Публикация из отдельной формы",
            "description": "Текст поста",
        })

        self.assertRedirects(response, reverse("post_list"))
        post = Post.objects.get(title="Публикация из отдельной формы")
        self.assertEqual(post.created_by, self.owner)

    def test_only_owner_can_edit_or_delete_post(self):
        post = Post.objects.create(
            title="Чужой пост",
            description="Текст",
            created_by=self.other_user,
        )
        self.client.force_login(self.owner)

        edit_response = self.client.get(reverse("edit_post", args=[post.pk]))
        delete_response = self.client.post(
            reverse("delete_post", args=[post.pk])
        )

        self.assertEqual(edit_response.status_code, 404)
        self.assertEqual(delete_response.status_code, 404)
        self.assertTrue(Post.objects.filter(pk=post.pk).exists())

    def test_owner_can_edit_and_delete_post(self):
        post = Post.objects.create(
            title="Мой пост",
            description="Исходный текст",
            created_by=self.owner,
        )
        quote = Quote.objects.create(post=post, text="Цитата останется")
        self.client.force_login(self.owner)

        edit_response = self.client.post(
            reverse("edit_post", args=[post.pk]),
            {"title": "Обновлённый пост", "description": "Новый текст"},
        )
        post.refresh_from_db()
        self.assertRedirects(edit_response, reverse("post_list"))
        self.assertEqual(post.title, "Обновлённый пост")

        delete_response = self.client.post(
            reverse("delete_post", args=[post.pk])
        )
        self.assertRedirects(delete_response, reverse("post_list"))
        self.assertFalse(Post.objects.filter(pk=post.pk).exists())
        quote.refresh_from_db()
        self.assertIsNone(quote.post)
