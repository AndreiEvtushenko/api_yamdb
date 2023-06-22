from django.contrib import admin

from .models import (Categories, Comments, Genres,
                     GenreTitle, Title, Review)


class CategoriesAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug'
    )
    search_fields = ('slug',)
    list_filter = ('slug',)
    empty_value_display = 'пусто'


class GenresAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug'
    )
    search_fields = ('slug',)
    list_filter = ('slug',)
    empty_value_display = 'пусто'


class TitlesAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'year',
        'description',
        'category',
    )
    search_fields = ('name',)
    list_filter = ('year',)
    empty_value_display = 'пусто'


class ReviewsAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'author',
        'title_id',
        'text',
        'score',
        'pub_date'
    )
    search_fields = ('author',)
    list_filter = ('pub_date',)
    empty_value_display = 'пусто'


class CommentsAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'author',
        'reviews_id',
        'text',
        'pub_date'
    )
    search_fields = ('author',)
    list_filter = ('pub_date',)
    empty_value_display = 'пусто'


class GenreTitleAdmin(admin.ModelAdmin):
    list_display = (
        'genre',
        'title'
    )


admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Genres, GenresAdmin)
admin.site.register(Title, TitlesAdmin)
admin.site.register(Review, ReviewsAdmin)
admin.site.register(Comments, CommentsAdmin)
admin.site.register(GenreTitle, GenreTitleAdmin)
