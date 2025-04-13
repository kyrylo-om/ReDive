from django.db import models
from django.utils import timezone

class Person(models.Model):
    name = models.CharField(max_length=75, unique=True)
    entry_date = models.DateTimeField(auto_now_add=True)
    created_date = models.DateField(null=True, blank=True)
    last_analysis = models.ForeignKey('History', null=True, blank=True, on_delete=models.SET_NULL, related_name="last_analysis_for_person")

    def __str__(self):
        return f'{self.name}'

    def update_last_analysis(self):
        """Оновлює посилання на останній аналіз користувача"""
        latest_history = self.histories.order_by('-analyzed_at').first()
        self.last_analysis = latest_history
        self.save()

class History(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="histories")
    analyzed_at = models.DateTimeField(default=timezone.now)
    karma = models.IntegerField()
    pic = models.URLField(max_length=2048)
    link_karma = models.IntegerField()
    comment_karma = models.IntegerField()
    is_mod = models.BooleanField()
    is_employee = models.BooleanField()
    trophies = models.JSONField(default=list)
    is_gold = models.BooleanField()
    verified = models.BooleanField()
    has_verified_email = models.BooleanField()
    bot_likelihood_percent = models.IntegerField()
    subreddit = models.JSONField(default=dict)
    def __str__(self):
        analyzed_at = self.analyzed_at.strftime('%Y-%m-%d %H:%M')
        return f"{self.person.name} @ {analyzed_at}"

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)
        self.person.update_last_analysis()

class Post(models.Model):
    history = models.ForeignKey(History, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=300)
    body = models.TextField()
    subreddit = models.CharField(max_length=100)
    permalink = models.URLField()
    url = models.URLField()
    score = models.IntegerField()
    upvotes_ratio = models.FloatField()
    created_date = models.DateTimeField()
    num_comments = models.IntegerField()
    over_18 = models.BooleanField()

    def __str__(self):
        return f"{self.url}"

class Comment(models.Model):
    history = models.ForeignKey(History, on_delete=models.CASCADE, related_name="comments")
    body = models.TextField()
    score = models.IntegerField()
    subreddit = models.CharField(max_length=100)
    url = models.URLField()
    created_date = models.DateTimeField()

    def __str__(self):
        return f"{self.url}"

