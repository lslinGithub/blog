from django.urls import path
from . import views
urlpatterns = [
    path('<int:post_pk>/', views.comment, name='comment'),
]