from core.models import Article, Tag, Category
from django.http import JsonResponse
from django_ratelimit.decorators import ratelimit
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt

@ratelimit(key='user_or_ip', rate='10/m')
def get_all_articles_list(request):
    """Returned articles are sorted by creation date, from newest to oldest,
    and stored in a tuple of dictionaries."""
    articles = Article.objects.all().order_by("-creation_date")

    serialized_entries = tuple(article.serialize_short() for article in articles)

    return JsonResponse(serialized_entries, safe=False, status=200)


@ratelimit(key='user_or_ip', rate='10/m')
def get_article(request, id):
    try:
        article = Article.objects.get(id=id)

        serialized_article = article.serialize_full()
        return JsonResponse(serialized_article, safe=False, status=200)

    except Article.DoesNotExist:
        return JsonResponse({"error": "this article does not exist"}, status=404)

@ratelimit(key='user_or_ip', rate='10/m')
def get_all_tags(request):
    tags = [tag.name for tag in Tag.objects.all()]


    return JsonResponse(tuple(tags), safe=False, status=200)

@ratelimit(key='user_or_ip', rate='10/m')
def get_all_categories(request):
    categories = [category.name for category in Category.objects.all()]

    return JsonResponse(tuple(categories), safe=False, status=200)

@csrf_exempt
@ratelimit(key='user_or_ip', rate='10/m')
def like_article(request, id):
    if request.method != "POST":
        return JsonResponse({"error": "Bad request method."}, status=400)
    
    try:
        article = Article.objects.get(id=id)
        article.likes += 1
        article.save()

        return JsonResponse({"success": "article liked"}, status=200)

    except Article.DoesNotExist:
        return JsonResponse({"error": "this article does not exist"}, status=404)