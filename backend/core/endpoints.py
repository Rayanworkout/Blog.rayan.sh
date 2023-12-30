from core.models import Article, Tag, Category
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import subprocess


def get_all_articles_list(request):
    """Returned articles are sorted by creation date, from newest to oldest,
    and stored in a tuple of dictionaries."""
    articles = Article.objects.all().order_by("-creation_date")

    serialized_entries = tuple(article.serialize_short() for article in articles)

    return JsonResponse(serialized_entries, safe=False, status=200)


def get_article(request, id):
    try:
        article = Article.objects.get(id=id)

        serialized_article = article.serialize_full()
        return JsonResponse(serialized_article, safe=False, status=200)

    except Article.DoesNotExist:
        return JsonResponse({"error": "this article does not exist"}, status=404)


def get_all_tags(request):
    tags = [tag.name for tag in Tag.objects.all()]


    return JsonResponse(tuple(tags), safe=False, status=200)


def get_all_categories(request):
    categories = [category.name for category in Category.objects.all()]

    return JsonResponse(tuple(categories), safe=False, status=200)


# def create_article(request):
#     # Allowing only POST requests
#     if request.method != 'POST':
#         return JsonResponse({"error": "bad request method"}, status=400)

#     try:
#         # Get the JSON data from the request body
#         data = json.loads(request.body)

#         title, content = data['title'], data['content']

#         new_article = Article.objects.create(title=title, content=content)
#         new_article.save()

#         return JsonResponse({"success": True, "message": "article successfully created"}, safe=False, status=201)

#     except json.JSONDecodeError:
#         return JsonResponse({"error": "invalid JSON"}, status=400)

#     except Exception as e:
#         return JsonResponse({"error": str(e)}, status=400)


@csrf_exempt
def trigger_build(request):
    """Triggers a build for the blog app
    by sending a webhook from github."""
    if request.method == 'GET':
        subprocess.run(['/var/www/html/blog/blog_pipeline.sh'])
        return JsonResponse({'message': 'Build triggered successfully.'}, status=200)
    else:
        return JsonResponse({'message': 'Invalid request method.'}, status=405)