from django.urls import path
from . import views

urlpatterns = [
    # path("", views.categories),
    # path("<int:pk>", views.category),
    # path("", views.Categorie.as_view()),
    # path("<int:pk>", views.CategoryDetail.as_view()),
    path(
        "",
        views.CategorieViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
    ),
    path(
        "<int:pk>",
        views.CategoryViewSet.as_view(
            {
                "get": "retrieve",
                "put": "partial_update",
                "delete": "destroy",
            }
        ),
    ),
]
