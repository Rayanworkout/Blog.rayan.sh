from django.contrib import admin
from core.models import Article, Tag
from django.contrib.auth.models import Group

admin.site.register(Tag)

admin.site.unregister(Group)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    def get_tags(self, obj):
        return ", ".join([t.name for t in obj.tags.all()])
    
    def shorter_description(self, obj):
        return obj.description[:40] + " ..."
    
    get_tags.short_description = "Tags"
    shorter_description.short_description = "Description"
    
    list_display = ('title', 'shorter_description', 'get_tags', 'creation_date')
    search_fields = ('title', 'description', 'content')
    list_filter = ('creation_date', 'tags')
    date_hierarchy = 'creation_date'
    ordering = ('-creation_date',)
    
    fieldsets = (
        ('Article', {
            'fields': ('title', 'description', 'content', 'tags')
        }),
        ('Metadata', {
            'fields': ('creation_date',)
        })
    )
