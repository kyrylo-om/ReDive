"""Module about requesting info from Reddit"""
import re
from datetime import datetime, timezone
import os
import praw
import prawcore
import requests
from dotenv import load_dotenv
import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from textblob import TextBlob

load_dotenv()
REDDIT_CLIENT_ID = os.getenv('REDDIT-CLIENT-ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT-CLIENT-SECRET')
REDDIT_USER_AGENT = os.getenv('REDDIT-USER-AGENT')
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
    try:
        nltk.data.find("corpora/stopwords")
    except LookupError:
        nltk.download("stopwords")
    try:
        nltk.data.find("corpora/wordnet")
    except LookupError:
        nltk.download("wordnet")
    _reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID, client_secret=REDDIT_CLIENT_SECRET, user_agent=REDDIT_USER_AGENT)

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
    def description_red(proxy_link: praw.models.Redditor, username:str, limit_post = 1000, limit_comment = 1000):
        """Return the description of a Reddit user"""
        try:
            submissions = list(proxy_link.submissions.new(limit=limit_post))
            comments = list(proxy_link.comments.new(limit=limit_comment))
            subreddit = proxy_link.subreddit
            bot_score = DataGetter.compute_bot_score(proxy_link, submissions, comments)

        except prawcore.exceptions.Forbidden:
            submissions, comments, bot_score = [], [], 0

        return {
            "name": proxy_link.name,
            'pic': proxy_link.icon_img,
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
            "bot_likelihood_percent": bot_score,
            "subreddit": {
                "banner_img": subreddit["banner_img"],
                "name": subreddit["name"],
                "over_18": subreddit["over_18"],
                "public_description": subreddit["public_description"],
                "subscribers":subreddit["subscribers"],
                "title":subreddit["title"]
            },
            "recent_posts": [
                {
                    "title": post.title,
                    "body": post.selftext,
                    "subreddit": post.subreddit.display_name,
                    "permalink": post.permalink,
                    "url": post.url,
                    "score": post.score,
                    "upvotes_ratio": post.upvote_ratio,
                    "created_date": datetime.fromtimestamp(post.created_utc, tz=timezone.utc),
                    "num_comments": post.num_comments,
                    "over_18": post.over_18,
                }
                for post in submissions
                if hasattr(post, "title")
            ],
            "recent_comments": [
                {
                    "body": comment.body,
                    "score": comment.score,
                    "subreddit": comment.subreddit.display_name,
                    "url": comment.permalink,
                    "created_date": datetime.fromtimestamp(comment.created_utc, tz=timezone.utc),
                }
                for comment in comments
                if hasattr(comment, "body")
            ],
        }

    @staticmethod
    def compute_bot_score(proxy_link, submissions, comments):
        '''Compute the bot score of a Reddit user'''
        score = 0
        max_score = 100  # We normalize to this

        # Username bot-like
        if re.search(r'\b(bot|auto)\b|\d{5,}', proxy_link.name.lower()):
            score += 15

        # New account + activity
        account_created = datetime.fromtimestamp(proxy_link.created_utc, tz=timezone.utc)
        account_age_days = (datetime.now(timezone.utc) - account_created).days
        if account_age_days < 7:
            score += 20

        # High post frequency
        if len(submissions) + len(comments) > 100 and account_age_days < 30:
            score += 20

        # Low karma but high activity
        total_karma = proxy_link.link_karma + proxy_link.comment_karma
        if total_karma < 50 and (len(submissions) + len(comments)) > 50:
            score += 15

        comment_bodies = [c.body[:50] for c in comments if hasattr(c, "body")]
        if len(set(comment_bodies)) < len(comment_bodies) * 0.5:
            score += 15

        if proxy_link.is_mod or proxy_link.is_employee:
            score -= 10

        return max(0, min(score, max_score))
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

    # @staticmethod
    # def get_reddit_avatar(username):
    #     """Get the avatar of a Reddit user"""
    #     if not username or not isinstance(username, str):
    #         raise ValueError("Username must be a non-empty string")
    #     headers = {"User-Agent": "windows:RedditAnalyzer:v1.0 (by /u/lukakerf)"}
    #     api_url = f"https://www.reddit.com/user/{username}/about.json"
    #     try:
    #         response = requests.get(api_url, headers=headers, timeout=5)
    #         rate_limit_used = response.headers.get('X-Ratelimit-Used')
    #         rate_limit_remaining = response.headers.get('X-Ratelimit-Remaining')
    #         rate_limit_reset = response.headers.get('X-Ratelimit-Reset')
    #         print("Used: ", rate_limit_used)
    #         print("Remaining: ", rate_limit_remaining)
    #         print(f"Reset on: {int(rate_limit_reset)/60:.2f} minutes")
    #         response.raise_for_status()
    #     except requests.exceptions.RequestException:
    #         return None
    #     if response.status_code == 200:
    #         data = response.json()
    #         avatar_url = data.get("data", {}).get("icon_img", "").split("?")[0]
    #         if avatar_url:
    #             return avatar_url

    #     return None

    @handle_reddit_errors
    def semantics_analysis(self,row: str):
        spliter = row.split()
        results=dict()
        stop_words = set(stopwords.words("english"))
        for i in spliter:
            i = i.lower()
            if not i.isalpha():
                continue
            if i in stop_words:
                continue
            results[i] = results.get(i, 0) + 1
        analysis = {
            "top_words": [],
            "themes": {},
            "sentiment": {"polarity": 0, "subjectivity": 0}
            }
        analysis["top_words"] = sorted(results.items(), key=lambda x: x[1], reverse=True)

        for word, freq in analysis["top_words"]:
            synsets = wn.synsets(word)
            if synsets:
                topic = synsets[0].lexname()
                if topic not in analysis["themes"]:
                    analysis["themes"][topic] = 0
                analysis["themes"][topic] += freq

        sentence = ' '.join([word for word in results])
        blob = TextBlob(sentence)
        analysis["sentiment"]["polarity"] = round(blob.sentiment.polarity,2)
        analysis["sentiment"]["subjectivity"] = round(blob.sentiment.subjectivity,2)
        return results,analysis
