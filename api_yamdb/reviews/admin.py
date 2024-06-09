from django.contrib import admin

from reviews.models import Category, Comment, Genre, Review, Title


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'description')
    search_fields = ('description',)
    list_filter = ('year',)
    empty_value_display = '-пусто-'


admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Genre)
admin.site.register(Review)
