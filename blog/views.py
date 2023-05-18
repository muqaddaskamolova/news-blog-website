import social_core
from django.contrib.auth.views import PasswordChangeView
import requests
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.urls import reverse_lazy

from .models import Category, Article, Developer, Like
from .forms import *
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, UpdateView
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.contrib.auth.forms import UserChangeForm


# Create your views here.


def index(request):
    categories = Category.objects.all()
    articles = Article.objects.all()
    articles = articles.order_by('-created_at')

    context = {
        'title': 'WorldNews',
        'categories': categories,
        'articles': articles,
        'count': articles.count(),
        #  'articles_num': articles.filter(articles > 50)

    }
    return render(request, 'blog/index.html', context, )


def category_page(request, category_id):
    articles = Article.objects.filter(category_id=category_id)
    articles = articles.order_by('-created_at')

    category = Category.objects.get(pk=category_id)
    categories = Category.objects.all()
    context = {
        'title': f"Category: {category.title}",
        'articles': articles,
        'categories': categories,
    }

    return render(request, 'blog/index.html', context)


def about_dev(request):
    developers = Developer.objects.all()

    context = {
        'title': 'About Developers',
        'developers': developers
    }
    return render(request, 'blog/about_dev.html', context)


def search_results(request):
    word = request.GET.get('q')
    articles = Article.objects.filter(Q(title__icontains=word) | Q(content__icontains=word)
                                      )
    context = {
        'articles': articles.order_by('-created_at')
    }
    return render(request, 'blog/index.html', context)


def add_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = Article.objects.create(**form.cleaned_data)
            article.save()
            return redirect('index')
        else:
            pass
    else:
        form = ArticleForm()

        context = {
            'title': 'New Article',
            'form': form,
        }
        return render(request, 'blog/article_form.html', context)


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user:
                login(request, user)
                messages.success(request, 'You have successfully logged in!')
                return redirect('index')
            else:
                messages.error(request, 'You have not logged in,  Or  your login or password is wrong!')
                return redirect('login')
        else:
            messages.error(request, 'You have not logged in,  Or  your login or password is wrong!')
            return redirect('login')
    else:
        form = LoginForm()
        context = {
            'title': 'LOGIN',
            'form': form
        }
        return render(request, 'blog/user_login.html', context)


@login_required(login_url='login')
def user_logout(request):
    logout(request)
    messages.warning(request, 'You have successfully logged out!')
    return redirect('index')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have successfully registered! Sign in!')
            return redirect('login')
        for field in form.errors:
            messages.error(request, form.errors[field].as_text())
            return redirect('register')
    else:
        form = RegistrationForm()

        context = {
            'title': 'REGISTER',
            'form': form
        }
        return render(request, 'blog/register.html', context)


def article_detail(request, article_id):
    article = Article.objects.get(pk=article_id)
    article.views += 1
    article.save()

    context = {
        'title': article.title,
        'article': article

    }
    if request.user.is_authenticated:
        context['comment_form'] = CommentForm()
    context['comments'] = Comment.objects.filter(article=article)
    user = request.user
    if user.is_authenticated:
        mark, created = Like.objects.get_or_create(user=user, article=article)
        if created:
            context['like'] = False
            context['dislike'] = False
        else:
            context['like'] = mark.like
            context['dislike'] = mark.dislike

    else:
        context['like'] = False
        context['dislike'] = False

    marks = Like.objects.filter(article=article)
    likes_count = len([i for i in marks if i.like])
    dislikes_count = len([i for i in marks if i.dislike])
    context['likes_count'] = likes_count
    context['dislikes_count'] = dislikes_count

    return render(request, 'blog/article_detail.html', context)


@login_required(login_url='login')
def update_article(request, id):
    article = Article.objects.get(id=id)
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect('article', id)
        else:
            for field in form.errors:
                messages.error(request, form.errors[field].as_text)
                return redirect('update', id)
    else:
        form = ArticleForm(instance=article)

        context = {
            'title': 'UPDATE ARTICLE',
            'form': form,
        }

        return render(request, 'blog/article_form.html', context)


@login_required(login_url='login')
def delete_article(request, id):
    article = Article.objects.get(id=id)
    if request.method == 'POST':
        article.delete()
        return redirect('index')
    context = {
        'article': article
    }
    return render(request, 'blog/confirm_delete.html', context)


def save_comment(request, pk):
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.article = Article.objects.get(pk=pk)
        comment.user = request.user
        comment.save()
        messages.success(request, 'Your comment is added!')
        return redirect('article', pk)


@login_required(login_url='login')
# @allowed_users(allowed_roles=['admin', 'developer'])
def user_profile(request):
    context = {}

    return render(request, 'blog/user_profile.html', context)


@login_required(login_url='login')
def add_or_delete_mark(request, article_id, action):
    user = request.user
    if user.is_authenticated:
        article = Article.objects.get(pk=article_id)
        mark, created = Like.objects.get_or_create(user=user, article=article)
        if action == 'add_like':
            mark.like = True
            mark.dislike = False
        elif action == 'add_dislike':
            mark.like = False
            mark.dislike = True
        elif action == 'delete_like':
            mark.like = False
        elif action == 'delete_dislike':
            mark.dislike = False

            mark.save()
            return redirect('article', article.pk)
        else:
            return redirect('login')


def contact_us(request, ):
    if request.method == 'POST':
        message_name = request.POST['message-name'],
        message_email = request.POST['message-email'],
        subject_name = request.POST['subject-name'],
        message = request.POST['message'],

        send_mail(
            message_name,
            subject_name,
            message,
            message_email,
            ['kamolovamuqaddas@gmail.com']
        )

        return render(request, 'blog/contact.html', {'message_name': message_name,
                                                     'message_email': message_email,
                                                     'subject_name': subject_name,
                                                     'message': message})
    else:
        return render(request, 'blog/contact.html', {})


def listing(request):
    article_list = Article.objects.all()
    paginator = Paginator(article_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj
    }

    return render(request, 'blog/index.html', {'page_obj': page_obj})


def map_page(request):
    context = {}

    return render(request, 'blog/map_page.html', context)


@login_required
def edit_profile(request, template_name='blog/edit_profile.html'):
    if request.method == 'POST':
        userprofile_edit = EditUserForm(request.POST.copy())
        form = UserChangeForm(userprofile_edit)
        if form.is_valid():
            form.save()
            return redirect('blog/user_profile/')
    else:
        form = UserChangeForm()
        return render(request, 'blog/edit_profile.html', locals())

    def get_object(self):
        return self.request.user


def user_agent():
    """Builds a simple User-Agent string to send in requests"""
    return 'social-auth-' + social_core.__version__


class PasswordsChangeView(PasswordChangeView):
    success_url = reverse_lazy('password_success')


def password_success(request):
    return render(request, 'blog/password_success.html',
                  {})


def media(request):
    r = requests.get(
        'https://api.mediastack.com/v1/news? access_key = 3b57cf957527b994aa8f3c8d936827cf & countries = us')
    res = r.json()
    data = res['data']
    title = []
    description = []
    image = []
    url = []
    for i in data:
        title.append(i['title'])
        description.append(i['description'])
        image.append(i['image'])
        url.append(i['url'])
        news = zip(title, description, image, url)

    return render(request, 'blog/media.html', {'news': news})
