from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import Book, UserProfile
from .decorators import profile_require

import random
import time


def home(request):
    context = {
        'random_items': Book.objects.all()[:10],
    }
    return render(request, 'index.html', context)


def sign_up(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            messages.add_message(request, messages.ERROR, '用户名已存在！')
        else:
            user_obj = User.objects.create_user(username=username, password=password)
            UserProfile.objects.create(user=user_obj)
            messages.add_message(request, messages.SUCCESS, '注册成功！')
            return HttpResponseRedirect('/')
    return render(request, 'sign_up.html')


def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user=user)
            messages.success(request, '登录成功')
            return HttpResponseRedirect('/')
        else:
            messages.add_message(request, messages.ERROR, '用户名或密码错误！')
    return render(request, 'sign_in.html')


@login_required(login_url='/sign_in')
def user_logout(request):
    logout(request)
    messages.info(request, '退出登录')
    return HttpResponseRedirect('/')


@login_required(login_url='/sign_in')
@profile_require 
def user_center(request):
    profile_obj = UserProfile.objects.get(user=request.user)

    return render(request, 'user.html', {'profile': profile_obj})


def details(request, pk):
    item_obj: Book = get_object_or_404(Book.objects.all(), pk=pk)
    is_purchased = False

    if request.user.is_authenticated:
        profile_set = UserProfile.objects.filter(user=request.user)
        if profile_set.exists():
            profile_obj = profile_set.first()
            if item_obj in profile_obj.purchased.all():
                is_purchased = True

    context = {
        'item': item_obj,
        'is_purchased': is_purchased,
    }

    return render(request, 'details.html', context)


@login_required(login_url='/sign_in')
@profile_require
def cart(request):
    profile_obj = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        action = request.POST.get('action')
        from_url = request.POST.get('from_url')
        if action == 'add':
            item_id = request.POST.get('item')
            item: Book = get_object_or_404(Book.objects.all(), pk=item_id)
            profile_obj.cart.add(item)
            messages.success(request, f'添加 <b>{item.title}</b> 到购物车成功！')
            return HttpResponseRedirect(from_url)
        if action == 'delete':
            item_id = request.POST.get('item')
            item = get_object_or_404(Book.objects.all(), pk=item_id)
            profile_obj.cart.remove(item)
            messages.success(request, f'已经将 <b>{item.title}</b> 从购物车中移除！')
        if action == 'pay':
            for item in profile_obj.cart.all():
                profile_obj.purchased.add(item)
                profile_obj.cart.remove(item)
            messages.success(request, f'支付成功，恭喜购物车已清空！')
            return HttpResponseRedirect(reverse('user'))
        if action == 'direct_pay':
            item_id = request.POST.get('item')
            item = get_object_or_404(Book.objects.all(), pk=item_id)
            profile_obj.purchased.add(item)
            messages.success(request, f'购买成功！')
            return HttpResponseRedirect(reverse('user'))

    context = {
        'profile': profile_obj,
        'cart': profile_obj.cart.all(),
        'total': profile_obj.cart.count(),
        'price': 0
    }

    for item in profile_obj.cart.all():
        context['price'] += item.price

    return render(request, 'cart.html', context)
