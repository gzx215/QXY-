from django.contrib import admin
from store.models import UserProfile, Book

admin.site.site_header = '书城后台管理'
admin.site.site_title = '书城后台管理'
admin.site.index_title = '书城后台管理'


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user']


@admin.register(Book)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['Id', 'title', 'author', 'tag']
    search_fields = ['title', 'author']
 