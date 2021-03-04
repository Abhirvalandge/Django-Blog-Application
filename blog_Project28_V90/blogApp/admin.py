from django.contrib import admin
from blogApp.models import Post,Comment

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ['title','slug_field','author','body','publish','created','updated','status']
    list_filter = ('status','author',)
    search_fields = ('title','body',)
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ['status','publish']
    prepopulated_fields = {'slug_field':('title',)}

admin.site.register(Post,PostAdmin)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'body','created', 'updated', 'active']
    list_filter = ('active', 'created','updated')
    search_fields = ('name', 'email', 'body')
