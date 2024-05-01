# En el archivo views.py de tu aplicación 'blog'
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .forms import CommentForm, ArticleForm
from django.contrib.auth.decorators import login_required
from .models import Article
from django.contrib.auth import logout
from .forms import ArticleForm



def signup(request):
    if request.method == 'GET':
        return render(request, 'blog/signup.html', {"form": UserCreationForm})
    else:

        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    request.POST["username"], password=request.POST["password1"])
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {"form": UserCreationForm, "error": "Username already exists."})

        return render(request, 'signup.html', {"form": UserCreationForm, "error": "Passwords did not match."})

def signin(request):
    if request.method == 'GET':
        return render(request, 'registration/signin.html', {"form": AuthenticationForm})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'registration/signin.html', {"form": AuthenticationForm, "error": "Username or password is incorrect."})

        login(request, user)
        return redirect('create_article')

@login_required
def create_article(request):
    if request.method == "GET":
        return render(request, 'blog/create_article.html', {"form": ArticleForm()})
    else:
        try:
            form = ArticleForm(request.POST)
            print(request.POST)
            new_article = form.save(commit=False)
            new_article.author = request.user  # Asigna el usuario como autor del artículo
            print(new_article.author)
            new_article.save()
            return redirect('home')
        except ValueError:
            return render(request, 'blog/create_article.html', {"form": ArticleForm(), "error": "Error creating Article."})

def logout_view(request):
    logout(request)
    return redirect('home')

def home(request):
    articles = Article.objects.all()[1:10]  # Obtiene los primeros 3 artículos
    return render(request, 'blog/home.html', {'articles': articles})

def article_detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    # Aquí puedes agregar la lógica para mostrar los detalles del artículo
    # y también mostrar los comentarios relacionados
    return render(request, 'blog/article_detail.html', {'article': article})

def add_comment_to_article(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.author = request.user
            comment.save()
            return redirect('article_detail', article_id=article_id)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_article.html', {'form': form})

@login_required
def articles_by_user(request):
    # Obtener el ID del usuario actualmente autenticado
    usuario_id = request.user.id
    # Obtener todos los artículos publicados por el usuario
    articulos = Article.objects.filter(author_id=usuario_id)
    print(articulos)
    # Renderizar la plantilla con los artículos del usuario
    return render(request, 'blog/articles_by_user.html', {'articulos': articulos})
