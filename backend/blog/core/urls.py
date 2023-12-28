from django.urls import path
import core.endpoints as api

urlpatterns = [
    path("articles/", api.get_all_articles_list),
    # path('create/', api.create_article),
    path("article/<int:id>", api.get_article),
    path("tags/", api.get_all_tags),
    path("categories/", api.get_all_categories),
]
