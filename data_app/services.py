from datetime import timedelta
from django.utils import timezone
from django.db import transaction
from django.core.paginator import Paginator
from .models import Person, History, Post, Comment


def save_analysis_entry(data: dict):
    with transaction.atomic():

        person, _ = Person.objects.get_or_create(name=data['name'])
        person.created_date = data.get('created_date', None)

        history = History.objects.create(
            person=person,
            karma=data['karma'],
            link_karma=data['link_karma'],
            comment_karma=data['comment_karma'],
            is_mod=data['is_mod'],
            is_employee=data['is_employee'],
            is_gold=data['is_gold'],
            verified=data['verified'],
            trophies=data['trophies'],
            has_verified_email=data['has_verified_email'],
            bot_likelihood_percent=data['bot_likelihood_percent'],
            subreddit=data.get('subreddit', None),
        )


        for post_data in data.get('recent_posts', []):
            Post.objects.create(
                history=history,
                title=post_data['title'],
                body=post_data['body'],
                subreddit=post_data['subreddit'],
                permalink=f"https://reddit.com{post_data['permalink']}",
                url=post_data['url'],
                score=post_data['score'],
                upvotes_ratio=post_data['upvotes_ratio'],
                created_date=post_data['created_date'],
                num_comments=post_data['num_comments'],
                over_18=post_data['over_18'],
            )


        for comment_data in data.get('recent_comments', []):
            Comment.objects.create(
                history=history,
                body=comment_data['body'],
                score=comment_data['score'],
                subreddit=comment_data['subreddit'],
                url=f"https://reddit.com{comment_data['url']}",
                created_date=comment_data['created_date'],
            )

        return history

def get_analysis_entry(name: str) -> dict:
    """Get the analysis entry for a given Reddit username"""
    person = Person.objects.filter(name=name).first()
    history = person.last_analysis
    if not history:
        return {'error': f"No last analysis found for '{name}'"}


    recent_posts = [
        {
            'title': post.title,
            'subreddit': post.subreddit,
            'permalink': post.permalink.replace("https://reddit.com", ""),
            'url': post.url,
            'score': post.score,
            'upvotes_ratio': post.upvotes_ratio,
            'created_date': post.created_date,
            'num_comments': post.num_comments,
            'over_18': post.over_18,
        }
        for post in history.posts.all()
    ]

    recent_comments = [
        {
            'body': comment.body,
            'score': comment.score,
            'subreddit': comment.subreddit,
            'url': comment.url.replace("https://reddit.com", ""),
            'created_date': comment.created_date,
        }
        for comment in history.comments.all()
    ]

    data = {
        'name': person.name,
        'karma': history.karma,
        'link_karma': history.link_karma,
        'comment_karma': history.comment_karma,
        'created_date': person.created_date,
        'is_mod': history.is_mod,
        'is_employee': history.is_employee,
        'is_gold': history.is_gold,
        'verified': history.verified,
        'trophies': history.trophies,
        'has_verified_email': history.has_verified_email,
        'bot_likelihood_percent': history.bot_likelihood_percent,
        'subreddit': history.subreddit,
        'recent_posts': recent_posts,
        'recent_comments': recent_comments,
    }

    return data
def serialize_the_persons_data(page, limit, sort_key, sort_dir):
    persons = Person.objects.all().select_related("last_analysis")

    if sort_key in ["comments", "bot_likelihood_percent", "posts"]:
        if sort_key == "bot_likelihood_percent":
            persons = sorted(
                persons,
                key=lambda p: p.last_analysis.bot_likelihood_percent if p.last_analysis else -1,
                reverse=(sort_dir == "desc")
            )
        elif sort_key == "karma":
            persons = sorted(
                persons,
                key=lambda p: (p.last_analysis.karma if p.last_analysis else 0),
                reverse=(sort_dir == "desc")
            )
        else:
            persons = persons.order_by(f"{'' if sort_dir == 'asc' else '-'}{sort_key}")
    else:
        persons = persons.order_by('-last_analysis__analyzed_at')


    paginator = Paginator(persons, limit)
    page_obj = paginator.get_page(page)

    data = []
    for person in page_obj:
        history = person.last_analysis
        post_count = history.posts.count() if history else 0
        comment_count = history.comments.count() if history else 0

        data.append({
            "username": person.name,
            "posts": post_count,
            "comments": comment_count,
            "bot_percentage": history.bot_likelihood_percent if history else "N/A"
        })
    
    return data
def check_if_user_exists(username: str) -> bool:
    """Check if a user exists in the database"""
    return Person.objects.filter(name=username).exists()

def get_date_of_last_analysis(username: str):
    person = Person.objects.filter(name=username).select_related('last_analysis').first()
    return person.last_analysis.analyzed_at.strftime("%B %d %Y")

def is_last_analysis_recent(username:str):
    person = Person.objects.filter(name=username).select_related('last_analysis').first()
    if person and person.last_analysis:
        return person.last_analysis.analyzed_at >= timezone.now() - timedelta(days=7)