from django.contrib import admin
from .models import Person, History, Post, Comment

class HistoryAdmin(admin.ModelAdmin):
    list_display = ('person', 'analyzed_at', 'karma', 'bot_likelihood_percent', 'pic')
    list_filter = ('analyzed_at',)

class PostAdmin(admin.ModelAdmin):
    list_display = ('history', 'title', 'subreddit', 'created_date')
    list_filter = ('created_date', 'subreddit')
    search_fields = ('title', 'subreddit')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('history', 'subreddit', 'created_date')
    list_filter = ('created_date', 'subreddit')
    search_fields = ('subreddit',)

class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'last_analysis')
    search_fields = ('name',)
    list_filter = ('last_analysis',)

admin.site.register(Person, PersonAdmin)
admin.site.register(History, HistoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)