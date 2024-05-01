from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create_article/', views.create_article, name='create_article'),
    path('articles_by_user/', views.articles_by_user, name='articles_by_user'),
    path('article/<int:article_id>/', views.article_detail, name='article_detail'),
    path('article/<int:article_id>/comment/', views.add_comment_to_article, name='add_comment_to_article'),
    path('login/', auth_views.LoginView.as_view(), name='signin'),
    path('logout/', views.logout_view, name='logout'), 
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
     ]