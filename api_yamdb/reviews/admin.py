from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Category, Comments, Genre, Review, Title, User


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'slug'
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'slug'
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'year',
        'description',
        'category'
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'text',
        'author',
        'score',
        'pub_date'
    )
    search_fields = (
        'title',
        'author',
        'pub_date'
    )
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


@admin.register(Comments)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'review',
        'text',
        'author',
        'pub_date',
    )
    search_fields = (
        'review',
        'author',
        'pub_date'
    )
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
