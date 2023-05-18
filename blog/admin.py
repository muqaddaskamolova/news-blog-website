from django.contrib import admin
from .models import Article, Category, Developer, Comment, Like

# Register your models here.


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'title',
                    'category',
                    'views',
                    'created_at',
                    'updated_at',
                    'publish',
                    'get_articles_count',
                    )
    list_display_links = ('title',)
    list_editable = ('publish',)
    readonly_fields = ('views',)
    list_filter = ('title', 'category', 'created_at',)

    def get_articles_count(self, obj):
        if obj.products:
            return str(len(obj.products.all()))
        else:
            return '0'

    get_articles_count.short_description = 'Number of articles'


class DeveloperAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'full_name',
                    'job',
                    )
    list_display_links = ('full_name',)
    list_filter = ('job',)


admin.site.register(Category)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Developer, DeveloperAdmin)
admin.site.register(Comment)
admin.site.register(Like)
