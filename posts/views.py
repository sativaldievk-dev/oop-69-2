from django.shortcuts import redirect, render

from .forms import CategoryForm, PostForm, QuoteForm
from .models import Post, Quote


def post_list(request):
    post_form = PostForm()
    quote_form = QuoteForm()

    if request.method == "POST":
        kind = request.POST.get("kind", "")

        if kind == "post":
            post_form = PostForm(request.POST)
            if post_form.is_valid():
                post_form.save()
                return redirect("post_list")

        elif kind == "quote":
            quote_form = QuoteForm(request.POST)
            if quote_form.is_valid():
                quote_form.save()
                return redirect("post_list")

    posts = (
        Post.objects
        .filter(is_active=True)
        .select_related("category")
        .prefetch_related("quotes")
        .order_by("-id")
    )
    quotes = Quote.objects.select_related("post").order_by("-created_at")

    return render(request, "posts/post_list.html", {
        "posts": posts,
        "quotes": quotes,
        "post_form": post_form,
        "quote_form": quote_form,
    })


def profile(request):
    return render(request, "posts/profile.html")


def add_publication(request):
    form = PostForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("post_list")

    return render(request, "posts/add_publication.html", {"form": form})


def add_category(request):
    form = CategoryForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("post_list")

    return render(request, "posts/add_category.html", {"form": form})


def quote_list(request):
    quotes = Quote.objects.select_related("post").order_by("-created_at")
    return render(request, "posts/quotes.html", {"quotes": quotes})


def add_quote(request):
    form = QuoteForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("quote_list")

    return render(request, "posts/add_quote.html", {"form": form})


def library(request):
    posts = (
        Post.objects
        .filter(is_active=True)
        .select_related("category")
        .order_by("-id")
    )
    return render(request, "posts/library.html", {"posts": posts})


def book_reader(request):
    from pathlib import Path
    import json
    from django.conf import settings

    book_file = Path(settings.BASE_DIR) / "posts" / "books.json"
    chapters = []

    if book_file.exists():
        try:
            chapters = json.loads(book_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            chapters = []

    chapters = sorted(chapters, key=lambda item: item["number"])
    number = request.GET.get("chapter", "1")

    try:
        number = int(number)
    except (TypeError, ValueError):
        number = 1

    current_index = next(
        (i for i, item in enumerate(chapters)
         if item["number"] == number),
        0
    )

    current = chapters[current_index] if chapters else None
    previous = chapters[current_index - 1] if current_index > 0 else None
    next_chapter = (
        chapters[current_index + 1]
        if current_index + 1 < len(chapters)
        else None
    )

    return render(request, "posts/book.html", {
        "chapters": chapters,
        "current": current,
        "previous": previous,
        "next": next_chapter,
    })


def book_catalog(request):
    from pathlib import Path
    import json
    from django.conf import settings

    folder = Path(settings.BASE_DIR) / "posts" / "book_data"
    books = []
    for slug, filename in [
        ("amir-timur", "amir_timur.json"),
        ("pushkin", "pushkin.json"),
        ("aitmatov", "aitmatov.json"),
    ]:
        file_path = folder / filename
        if file_path.exists():
            data = json.loads(file_path.read_text(encoding="utf-8"))
            books.append({"slug": slug, "title": data["title"]})

    return render(request, "posts/book_catalog.html", {"books": books})


def book_detail(request, slug):
    from pathlib import Path
    import json
    from django.conf import settings
    from django.http import Http404

    allowed = {
        "amir-timur": "amir_timur.json",
        "dostoevsky": "dostoevsky.json",
        "aitmatov": "aitmatov.json",
        "pushkin": "pushkin.json",
    }
    filename = allowed.get(slug)
    if not filename:
        raise Http404("Книга не найдена")

    file_path = Path(settings.BASE_DIR) / "posts" / "book_data" / filename
    if not file_path.exists():
        raise Http404("Файл книги не найден")

    data = json.loads(file_path.read_text(encoding="utf-8"))
    chapters = data.get("chapters", [])
    chapters.sort(key=lambda chapter: chapter["number"])

    try:
        number = int(request.GET.get("chapter", "1"))
    except (TypeError, ValueError):
        number = 1

    index = next(
        (i for i, chapter in enumerate(chapters)
         if chapter["number"] == number),
        0
    )

    current = chapters[index] if chapters else None
    previous = chapters[index - 1] if index > 0 else None
    next_chapter = chapters[index + 1] if index + 1 < len(chapters) else None

    return render(request, "posts/book_detail.html", {
        "book": data,
        "chapters": chapters,
        "current": current,
        "previous": previous,
        "next": next_chapter,
        "slug": slug,
    })
