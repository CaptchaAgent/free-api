from django.urls import path

from . import views

app_name = "polls"
urlpatterns = [
    path("docs/", views.docs, name="docs"),
    path("<str:solver_name>/", views.api, name="api"),
]
