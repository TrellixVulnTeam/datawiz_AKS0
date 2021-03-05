from django.urls import path, include

urlpatterns = [
    path("account/", include("account.urls")),
    path("article/", include("article.api_urls")),
]
