from django.http import HttpResponse
from .models import Post


def post_list(request):
    posts = Post.objects.all()

    result = ""

    for post in posts:
        result += f"""
        <h1>{post.title}</h1>
        <p>{post.description}</p>
        <p>Активен: {post.is_active}</p>
        <hr>
        """

    return HttpResponse(result)