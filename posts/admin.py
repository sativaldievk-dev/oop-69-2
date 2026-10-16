from django.contrib import admin

from .models import Category, Post, Quote


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "is_active")
    list_filter = ("category", "is_active")
    search_fields = ("title", "description")


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ("short_text", "author", "post", "created_at")
    list_filter = ("post",)
    search_fields = ("text", "author", "post__title")

    def short_text(self, obj):
        return obj.text[:60]

    short_text.short_description = "Цитата"
