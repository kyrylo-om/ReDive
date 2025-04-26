"""Module about requesting info from Reddit"""

import re
from datetime import datetime, timezone
import os
import praw
import prawcore
from dotenv import load_dotenv

load_dotenv()
REDDIT_CLIENT_ID = os.getenv("REDDIT-CLIENT-ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT-CLIENT-SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT-USER-AGENT")


class RedditAPIError(Exception):
    """Base class for Reddit API errors"""


class NotFound(RedditAPIError):
    """Raised when a user or resource is not found"""


def handle_reddit_errors(func):
    """Decorator to handle Reddit API errors."""

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            raise NotFound("Resource not found") from e

    return wrapper


class DataGetter:
    """Get data about someone or something"""

    _reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=REDDIT_USER_AGENT,
    )

    def __init__(self):
        pass

    @handle_reddit_errors
    def check_for_errors(username: str):
        if not username or not isinstance(username, str):
            raise ValueError("Username must be a non-empty string")
        proxy_link = DataGetter._reddit.redditor(username)
        _ = proxy_link.id
        return True

    @handle_reddit_errors
    def get_user_analysis(self, username: str):
        """Get the analysis of a Reddit user"""
        if not username or not isinstance(username, str):
            raise ValueError("Username must be a non-empty string")
        proxy_link = DataGetter._reddit.redditor(username)
        _ = proxy_link.id
        return self.description_red(proxy_link, username)

    @staticmethod
    def description_red(
        proxy_link: praw.models.Redditor,
        username: str,
        limit_post=3000,
        limit_comment=3000,
    ):
        """Return the description of a Reddit user"""
        try:
            submissions = list(proxy_link.submissions.new(limit=limit_post))
            comments = list(proxy_link.comments.new(limit=limit_comment))
            subreddit = proxy_link.subreddit
            pic = proxy_link.icon_img
            if not "styles.redditmedia.com" in pic:
                pic = (
                    "https://www.redditstatic.com/avatars/avatar_default_01_A5A4A4.png"
                )
        except prawcore.exceptions.Forbidden:
            submissions, comments, bot_score = [], [], 0
        user_data = {
            "name": proxy_link.name,
            "pic": pic,
            "id": proxy_link.id,
            "karma": proxy_link.link_karma + proxy_link.comment_karma,
            "link_karma": proxy_link.link_karma,
            "comment_karma": proxy_link.comment_karma,
            "created_date": datetime.fromtimestamp(proxy_link.created_utc).date(),
            "is_mod": proxy_link.is_mod,
            "is_employee": proxy_link.is_employee,
            "is_gold": proxy_link.is_gold,
            "verified": proxy_link.verified,
            "trophies": [
                {
                    "name": trophy.name,
                    "icon_70": trophy.icon_70,
                    "icon_40": trophy.icon_40,
                }
                for trophy in proxy_link.trophies()
            ],
            "has_verified_email": proxy_link.has_verified_email,
            "bot_likelihood_percent": 0,
            "subreddit": {
                "name": subreddit.name,
                "over_18": subreddit.over_18,
                "public_description": subreddit.public_description,
                "subscribers": subreddit.subscribers,
                "title": subreddit.title,
            },
            "recent_posts": [
                {
                    "title": post.title,
                    "body": re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", post.selftext),
                    "html": post.selftext_html if post.selftext_html else "",
                    "subreddit": post.subreddit.display_name,
                    "permalink": f"https://www.reddit.com{post.permalink}",
                    "url": post.url,
                    "score": post.score,
                    "upvotes_ratio": post.upvote_ratio,
                    "created_date": datetime.fromtimestamp(
                        post.created_utc, tz=timezone.utc
                    ),
                    "num_comments": post.num_comments,
                    "spoiler": post.spoiler,
                    "oc": post.is_original_content,
                    "over_18": post.over_18,
                }
                for post in submissions
                if hasattr(post, "title")
            ],
            "recent_comments": [
                {
                    "body": re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", comment.body),
                    "html": comment.body_html,
                    "score": comment.score,
                    "subreddit": comment.subreddit.display_name,
                    "permalink": f"https://www.reddit.com{comment.permalink}",
                    "is_submitter": comment.is_submitter,
                    "created_date": datetime.fromtimestamp(
                        comment.created_utc, tz=timezone.utc
                    ),
                }
                for comment in comments
                if hasattr(comment, "body")
            ],
        }

        return user_data

    @handle_reddit_errors
    def get_subreddit_info(self, subreddit_name: str):
        """Отримати інформацію про сабреддіт"""
        if not subreddit_name or not isinstance(subreddit_name, str):
            raise ValueError("Subreddit name must be a non-empty string")

        subreddit = DataGetter._reddit.subreddit(subreddit_name)
        _ = subreddit.id

        return {
            "name": subreddit.display_name,
            "title": subreddit.title,
            "description": subreddit.public_description,
            "subscribers": subreddit.subscribers,
            "active_users": subreddit.accounts_active,
            "created_date": datetime.fromtimestamp(subreddit.created_utc).date(),
            "over18": subreddit.over18,
            "icon_url": subreddit.icon_img if subreddit.icon_img else None,
            "banner_url": (
                subreddit.banner_background_image
                if subreddit.banner_background_image
                else None
            ),
            "rules": (
                [rule.short_name for rule in subreddit.rules]
                if hasattr(subreddit, "rules")
                else []
            ),
            "top_posts": [
                {
                    "title": post.title,
                    "score": post.score,
                    "url": post.url,
                    "created_date": datetime.fromtimestamp(post.created_utc),
                    "author": post.author.name if post.author else "[deleted]",
                }
                for post in subreddit.top(limit=5)
            ],
        }
