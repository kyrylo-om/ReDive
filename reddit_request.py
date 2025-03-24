"""Module about requesting info from Reddit"""

import praw
import prawcore


class NotFound(Exception):
    """Not Found error"""

    def __init__(self, message):
        self.message = message


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

        self._reddit_analyzed_users = {}

    @property
    def reddit_amount(self):
        """Returns the amount of analyzed reddit users"""
        return len(self._reddit_analyzed_users)

    def store_user(self, username: str):
        """Stores the user in the class.
        later will be done through database probably"""
        if not isinstance(username, str):
            raise TypeError("Username must be a string")

        try:
            user = RedditUser(DataGetter._reddit.redditor(username))
            _ = user.proxy_link.id  # Перевірка на існування користувача
        except prawcore.exceptions.NotFound as exc:
            raise NotFound(f"User '{username}' not found") from exc
        except Exception as exc:
            raise NotFound(f"Unexpected error: {exc}") from exc

        self._reddit_analyzed_users[username] = user

    def get_user_analysis(self, username: str):
        """
        Get the user analysis
        """
        if not isinstance(username, str):
            raise TypeError("Username must be a string")

        if username in self._reddit_analyzed_users:
            return self.description_red(self._reddit_analyzed_users[username])

        return self.store_user(username) or self.description_red(
            self._reddit_analyzed_users[username]
        )

    @staticmethod
    def description_red(user: "RedditUser"):
        """Return the description of a Reddit user"""
        try:
            submissions = list(user.proxy_link.submissions.new(limit=3))
            comments = list(user.proxy_link.comments.new(limit=3))
        except prawcore.exceptions.Forbidden:
            submissions, comments = [], []

        return {
            "name": user.proxy_link.name,
            "id": user.proxy_link.id,
            "karma": user.proxy_link.link_karma + user.proxy_link.comment_karma,
            "link_karma": user.proxy_link.link_karma,
            "comment_karma": user.proxy_link.comment_karma,
            "created_utc": user.proxy_link.created_utc,
            "is_mod": user.proxy_link.is_mod,
            "is_employee": user.proxy_link.is_employee,
            "is_gold": user.proxy_link.is_gold,
            "verified": user.proxy_link.verified,
            "has_verified_email": user.proxy_link.has_verified_email,
            "subreddit": (
                user.proxy_link.subreddit.display_name
                if user.proxy_link.subreddit
                else None
            ),
            "recent_posts": [
                {
                    "title": post.title,
                    "score": post.score,
                    "url": post.url,
                    "created_utc": post.created_utc,
                }
                for post in submissions
                if hasattr(post, "title")
            ],
            "recent_comments": [
                {
                    "body": comment.body[:100],
                    "score": comment.score,
                    "subreddit": comment.subreddit.display_name,
                    "created_utc": comment.created_utc,
                }
                for comment in comments
                if hasattr(comment, "body")
            ],
        }


class RedditUser:
    """Class representing a Reddit user"""

    def __init__(self, proxy_link: praw.models.Redditor):
        self.proxy_link: praw.models.Redditor = proxy_link
