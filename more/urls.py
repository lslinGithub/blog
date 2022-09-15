from django.urls import path
from . import views
urlpatterns = [
    path('login/', views.login_, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('findpwd/', views.findpwd, name='findpwd'),
    path('commit/', views.Commit, name='commit'),
    path('add/', views.post_add, name='add'),
    path('update/<int:pk>/', views.post_update, name='post_update'),
    path('delete/<int:pk>/', views.post_delete, name='post_delete'),
]