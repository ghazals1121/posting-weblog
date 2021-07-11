"""posting_weblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from panel import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', views.RegisterView.as_view(), name='panel-register-api'),
    path('api/login/', views.LoginView.as_view(), name='panel-login-api'),
    path('api/logout/', views.logout_view, name='panel-logout-api'),
    path('api/create_post/', views.create_post),
    path('api/edit_post/', views.edit_post),
    path('api/delete_post/', views.delete_post),
    path('api/post_comment/', views.post_comment),
    path('api/post_reply/', views.post_reply),
    path('api/like_post/', views.post_like),
    path('api/like_comment/', views.comment_like),
    path('api/dislike_post/', views.post_dislike),
    path('api/dislike_comment/', views.comment_dislike),
    # path('api/get_users_posts/', views.get_users_posts),
    # path('api/get_users_comments/', views.get_users_comments),
    # path('api/get_posts_comments/', views.get_posts_comments),
    # path('api/get_posts_likes/', views.get_posts_likes),
    # path('api/get_posts_dislikes/', views.get_posts_dislikes),
    # path('api/get_comments_replies/', views.get_comments_replies),
]
