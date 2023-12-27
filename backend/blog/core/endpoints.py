from core.models import Article
from django.http import JsonResponse


def get_all_articles_list(request):
    """Returned articles are sorted by creation date, from newest to oldest,
    and stored in a tuple of dictionaries."""
    articles = Article.objects.all().order_by('-creation_date')

    serialized_entries = tuple(article.serialize_short() for article in articles)
            
    return JsonResponse(serialized_entries, safe=False)


def get_article(request, id):
    try:
        article = Article.objects.get(id=id)

        serialized_article = article.serialize_full()
        return JsonResponse(serialized_article, safe=False)
    
    except Article.DoesNotExist:
        return JsonResponse({"error": "this article does not exist"}, status=404)


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
