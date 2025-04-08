"""Module about requesting info from Reddit"""
from datetime import datetime
import praw
import prawcore
import requests


class RedditAPIError(Exception):
    """Base class for Reddit API errors"""

class NotFound(RedditAPIError):
    """Raised when a user or resource is not found"""


def handle_reddit_errors(func):
    """Decorator to handle Reddit API errors."""

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except prawcore.exceptions.NotFound as e:
            raise NotFound("Resource not found") from e
        except prawcore.exceptions.Forbidden as e:
            raise RedditAPIError("Access forbidden") from e
        except Exception as e:
            raise RedditAPIError(f"Unexpected error: {e}") from e

    return wrapper


class DataGetter:
    """Get data about someone or something"""

    _reddit_client_id = "xyDp0DW13ZB9wDj7eU57nw"
    _reddit_client_secret = "hkG-118uedArdKf8T4gWi64so_YCFw"
    _reddit_user_agent = "windows:RedditAnalyzer:v1.0 (by /u/lukakerf)"
    _reddit = praw.Reddit(
        client_id=_reddit_client_id,
        client_secret=_reddit_client_secret,
        user_agent=_reddit_user_agent,
    )

    def __init__(self):
        pass

    @handle_reddit_errors
    def get_user_analysis(self, username: str):
        """Get the analysis of a Reddit user"""
        if not username or not isinstance(username, str):
            raise ValueError("Username must be a non-empty string")
        proxy_link = DataGetter._reddit.redditor(username)
        _ = proxy_link.id
        return self.description_red(proxy_link)

    @staticmethod
    def description_red(proxy_link: praw.models.Redditor, limit_post = 1000, limit_comment = 1000):
        """Return the description of a Reddit user"""
        try:
            submissions = list(proxy_link.submissions.new(limit=limit_post))
            comments = list(proxy_link.comments.new(limit=limit_comment))
        except prawcore.exceptions.Forbidden:
            submissions, comments = [], []

        return {
            "name": proxy_link.name,
            "id": proxy_link.id,
            "karma": proxy_link.link_karma + proxy_link.comment_karma,
            "link_karma": proxy_link.link_karma,
            "comment_karma": proxy_link.comment_karma,
            "created_date": datetime.fromtimestamp(proxy_link.created_utc).date(),
            "is_mod": proxy_link.is_mod,
            "is_employee": proxy_link.is_employee,
            "is_gold": proxy_link.is_gold,
            "verified": proxy_link.verified,
            "trophies": list(proxy_link.trophies()),
            "has_verified_email": proxy_link.has_verified_email,
            "subreddit": (
                proxy_link.subreddit if proxy_link.subreddit else None
            ),
            "recent_posts": [
                {
                    "title": post.title,
                    "subreddit": post.subreddit.display_name,
                    "permalink": post.permalink,
                    "url": post.url,
                    "score": post.score,
                    "upvotes_ratio": post.upvote_ratio,
                    "created_date": datetime.fromtimestamp(post.created_utc).date(),
                    "num_comments": post.num_comments,
                    "over_18": post.over_18,
                }
                for post in submissions
                if hasattr(post, "title")
            ],
            "recent_comments": [
                {
                    "body": comment.body[:100],
                    "score": comment.score,
                    "subreddit": comment.subreddit.display_name,
                    "url": comment.permalink,
                    "created_date": datetime.fromtimestamp(comment.created_utc).date(),

                }
                for comment in comments
                if hasattr(comment, "body")
            ],
        }

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

    @staticmethod
    def get_reddit_avatar(username):
        """Get the avatar of a Reddit user"""
        if not username or not isinstance(username, str):
            raise ValueError("Username must be a non-empty string")
        headers = {"User-Agent": "windows:RedditAnalyzer:v1.0 (by /u/lukakerf)"}
        api_url = f"https://www.reddit.com/user/{username}/about.json"
        try:
            response = requests.get(api_url, headers=headers, timeout=5)
            response.raise_for_status()
        except requests.exceptions.RequestException:
            return None
        if response.status_code == 200:
            data = response.json()
            avatar_url = data.get("data", {}).get("icon_img", "").split("?")[0]
            if avatar_url:
                return avatar_url

        return None
