import os

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.utils import timezone


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cart = models.ManyToManyField('Book', verbose_name='购物车', related_name='cart_user_profile', blank=True)
    purchased = models.ManyToManyField('Book', verbose_name='已购买商品', related_name='purchased_user_profile', blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = '用户资料'
        verbose_name_plural = verbose_name


def item_image_upload_to(instance, filename):
    return os.path.join('items', instance.name, filename)


class Book(models.Model):
    """图书"""
    isbn = models.TextField('全球唯一图书编号')
    title = models.TextField('书名')
    author = models.TextField('作者')
    author_intro = models.TextField('作者简介')
    tag = models.TextField('标签')
    NumRaters = models.IntegerField('评分人数', default=0)
    average = models.FloatField('平均评分', default=0.0)
    Id = models.TextField('豆瓣图书Id', default='', primary_key=True)
    binding = models.TextField('精装/简装')
    pages = models.IntegerField('页数', default=0)
    publisher = models.TextField('出版商')
    origin_title = models.TextField('图书原名')
    url = models.TextField('豆瓣链接')
    image = models.TextField('图书豆瓣图片')
    summary = models.TextField('图书概述')

    price = models.DecimalField('价格', max_digits=8, decimal_places=2, default=19.99)
    sales = models.IntegerField('销量', default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '图书'
        verbose_name_plural = verbose_name
 