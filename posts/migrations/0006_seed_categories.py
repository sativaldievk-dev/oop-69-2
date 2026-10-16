from django.db import migrations


def create_categories(apps, schema_editor):
    Category = apps.get_model("posts", "Category")
    for name, description in [
        ("Стихи", "Поэтические публикации"),
        ("Рассказы", "Короткие литературные тексты"),
        ("Заметки", "Небольшие мысли и наброски"),
    ]:
        Category.objects.get_or_create(
            name=name,
            defaults={"description": description},
        )


def delete_categories(apps, schema_editor):
    Category = apps.get_model("posts", "Category")
    Category.objects.filter(name__in=["Стихи", "Рассказы", "Заметки"]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("posts", "0005_category_alter_post_options_alter_quote_options_and_more"),
    ]

    operations = [
        migrations.RunPython(create_categories, delete_categories),
    ]
