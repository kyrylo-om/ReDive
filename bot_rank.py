from datetime import datetime, timezone
import numpy as np
from collections import Counter

def extract_user_features(user_data: dict) -> dict:
    now = datetime.now(timezone.utc).date()

    account_age_days = (now - user_data["created_date"]).days
    total_karma = user_data["karma"]
    link_karma = user_data["link_karma"]
    comment_karma = user_data["comment_karma"]

    is_mod = int(user_data["is_mod"])
    is_gold = int(user_data["is_gold"])
    is_employee = int(user_data["is_employee"])
    verified = int(user_data["verified"])
    has_verified_email = int(user_data["has_verified_email"])

    posts = user_data["recent_posts"]
    comments = user_data["recent_comments"]

    post_count = len(posts)
    comment_count = len(comments)

    num_trophies = len(user_data['trophies'])

    avg_post_score = np.mean([p["score"] for p in posts]) if post_count > 0 else 0
    avg_comment_score = np.mean([c["score"] for c in comments]) if comment_count > 0 else 0

    avg_post_length = np.mean([len(p.get("body", "")) + len(p.get("title", "")) for p in posts]) if post_count > 0 else 0
    avg_comment_length = np.mean([len(c["body"]) for c in comments]) if comment_count > 0 else 0

    post_to_comment_ratio = post_count / comment_count if comment_count > 0 else float('inf')

    all_times = [p["created_date"] for p in posts] + [c["created_date"] for c in comments]
    all_times.sort()
    if len(all_times) > 1:
        diffs = [(t2 - t1).total_seconds() / 3600 for t1, t2 in zip(all_times[:-1], all_times[1:])]
        avg_time_between_actions = np.mean(diffs)
    else:
        avg_time_between_actions = 0

    post_texts = [p.get("title", "") + p.get("body", "") for p in posts]
    post_counter = Counter(post_texts)
    repeated_posts = sum(1 for text, count in post_counter.items() if count > 1)
    repeated_post_ratio = repeated_posts / post_count if post_count > 0 else 0

    comment_texts = [c["body"] for c in comments]
    comment_counter = Counter(comment_texts)
    repeated_comments = sum(1 for text, count in comment_counter.items() if count > 1)
    repeated_comment_ratio = repeated_comments / comment_count if comment_count > 0 else 0

    return {
        'name':user_data['name'],
        'pic':user_data['pic'],
        "account_age_days": account_age_days,
        "total_karma": total_karma,
        "link_karma": link_karma,
        "comment_karma": comment_karma,
        'trophies': user_data['trophies'],
        "is_mod": is_mod,
        "is_gold": is_gold,
        "is_employee": is_employee,
        "verified": verified,
        "has_verified_email": has_verified_email,
        "post_count": post_count,
        "comment_count": comment_count,
        "avg_post_score": avg_post_score,
        "avg_comment_score": avg_comment_score,
        "avg_post_length": avg_post_length,
        "avg_comment_length": avg_comment_length,
        "post_to_comment_ratio": post_to_comment_ratio,
        "avg_time_between_actions": avg_time_between_actions,
        "repeated_post_ratio": repeated_post_ratio,
        "repeated_comment_ratio": repeated_comment_ratio,
        'recent_comments': user_data['recent_comments'],
        'recent_posts': user_data['recent_posts'],
        'repetitive_posts': repeated_post_ratio > 0.1,
        'repetitive_comments': repeated_comment_ratio > 0.1,
    }

def estimate_bot_likelihood(data):
    """Heuristic model that returns bot_likelihood_percent with explanation."""
    user_data = extract_user_features(data)
    human_points = {}
    bot_points = {}

    # --- Human-like behavior ---
    if user_data.get("is_mod"):
        human_points["moderator_status"] = 150

    # Posts with high upvotes
    post_bonus = sum(3 for post in user_data.get("recent_posts", []) if post.get("score", 0) > 100)
    if post_bonus:
        human_points["popular_posts"] = post_bonus

    # Comments with high upvotes
    comment_bonus = sum(2 for comment in user_data.get("recent_comments", []) if comment.get("score", 0) > 50)
    if comment_bonus:
        human_points["popular_comments"] = comment_bonus

    if not user_data.get("repetitive_posts", False):
        human_points["unique_posts"] = 200

    if not user_data.get("repetitive_comments", False):
        human_points["unique_comments"] = 200

    # Account age in years
    years_old = user_data.get("account_age_days", 0) // 365
    if years_old:
        human_points["account_age"] = years_old * 50

    # Trophies
    num_trophies = len(user_data.get("trophies", []))
    if num_trophies:
        human_points["trophies"] = num_trophies * 40

    # Has profile picture
    if user_data.get("pic") and "default" not in user_data["pic"]:
        human_points["has_profile_picture"] = 100

    # --- Bot-like behavior ---
    if not user_data.get("pic") or "default" in user_data["pic"]:
        bot_points["no_profile_picture"] = 100

    subreddits = set()
    for post in user_data.get("recent_posts", []):
        subreddits.add(post.get("subreddit"))
    for comment in user_data.get("recent_comments", []):
        subreddits.add(comment.get("subreddit"))

    if len(subreddits) > 30:
        bot_points["too_many_subreddits"] = (len(subreddits) - 30) * 3

    if user_data["name"].lower().startswith("user") and user_data["name"][4:].isdigit():
        bot_points["generic_username"] = 150

    if user_data.get("repetitive_posts", False):
        bot_points["repetitive_posts"] = 250

    if user_data.get("repetitive_comments", False):
        bot_points["repetitive_comments"] = 250

    # --- Score calculation ---
    total_human = sum(human_points.values())
    total_bot = sum(bot_points.values())

    score = total_bot / (total_human + total_bot + 1e-5)
    bot_likelihood_percent = round(score * 100)

    return {
        "bot_likelihood_percent": bot_likelihood_percent,
        "human_points": human_points,
        "bot_points": bot_points
    }