import numpy as np
from collections import Counter
from datetime import datetime, timezone
from math import log2

def entropy(values):
    """Calculate normalized entropy of a list of discrete values."""
    counter = Counter(values)
    total = len(values)
    probs = [count / total for count in counter.values()]
    return -sum(p * log2(p) for p in probs) / log2(len(probs)) if len(probs) > 1 else 0

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

    # --- New Features ---
    has_bio = bool(user_data.get("bio", "").strip())

    post_hours = [p["created_date"].hour for p in posts]
    comment_hours = [c["created_date"].hour for c in comments]
    post_time_variability = entropy(post_hours + comment_hours)

    total_awards = sum(p.get("awards", 0) for p in posts) + sum(c.get("awards", 0) for c in comments)

    link_post_ratio = sum(1 for p in posts if "http" in (p.get("body", "") + p.get("title", "")).lower()) / post_count if post_count else 0

    avg_posts_per_day = post_count / account_age_days if account_age_days > 0 else 0

    return {
        'name': user_data['name'],
        'pic': user_data['pic'],
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
        "repetitive_posts": repeated_post_ratio > 0.1,
        "repetitive_comments": repeated_comment_ratio > 0.1,
        'recent_comments': comments,
        'recent_posts': posts,
        "has_bio": has_bio,
        "post_time_variability": post_time_variability,
        "total_awards": total_awards,
        "link_post_ratio": link_post_ratio,
        "avg_posts_per_day": avg_posts_per_day,
    }

def estimate_bot_likelihood(data):
    """Heuristic model that returns bot_likelihood_percent with explanation."""
    user_data = extract_user_features(data)
    human_points = []
    bot_points = []

    if user_data.get("is_mod"):
        human_points.append({
            'name':'Moderator',
            'value':150,
            'description': 'User is a moderator of reddit.'
            })

    if user_data.get("has_verified_email"):
        human_points.append({
            'name':'Verified email',
            'value':100,
            'description':'User has a verified email.'
            })
    if user_data.get("verified"):
        human_points.append({
            'name':'Verified user',
            'value':50,
            'description':'User has been verified by reddit.'
            })
    if user_data.get("is_gold"):
        human_points.append({
            'name':'Gold user',
            'value':100,
            'description':'User has a gold profile status.'
            })
    post_bonus = sum(3 for post in user_data.get("recent_posts", []) if post.get("score", 0) > 100)
    if post_bonus:
        human_points.append({
            'name':'Popular posts',
            'value':post_bonus,
            'description':f'User has {post_bonus//3} popular posts.'
            })
    comment_bonus = sum(2 for comment in user_data.get("recent_comments", []) if comment.get("score", 0) > 50)
    if comment_bonus:
        human_points.append({
            'name':'Popular comments',
            'value':comment_bonus,
            'description':f'User has {comment_bonus//2} popular comments.'
            })
    if not user_data.get("repetitive_posts", False):
        human_points.append({
            'name':'Unique posts',
            'value':200,
            'description':'Almost all posts are unique.'
            })
    if not user_data.get("repetitive_comments", False):
        human_points.append({
            'name':'Unique comments',
            'value':200,
            'description':'Almost all comments are unique.'
            })
    years_old = user_data.get("account_age_days", 0) // 365
    if years_old:
        human_points.append({
            'name':'Old account',
            'value':years_old * 50,
            'description':f'Account was created {years_old} year ago.'
            })
    num_trophies = len(user_data.get("trophies", []))
    if num_trophies:
        human_points.append({
            'name':'Trophies',
            'value':num_trophies * 40,
            'description':f'User has {num_trophies} trophies.'
            })
    if user_data.get("pic") and "default" not in user_data["pic"]:
        human_points.append({
            'name':'Profile picture',
            'value':100,
            'description':'User has a profile picture.'
            })
    if user_data.get("post_to_comment_ratio", 1) < 0.5:
        human_points.append({
            'name':'Commenter ratio',
            'value':100,
            'description':f'User has healthy post to comment ratio of {round(user_data.get("post_to_comment_ratio", 1),2)}.'
            })
    if user_data.get("avg_comment_score", 0) > 2:
        human_points.append({
            'name':'Average comment score',
            'value':100,
            'description':f'User has an average comment score of {round(user_data.get("avg_comment_score", 0))}.'
            })
    if user_data.get("avg_post_score", 0) > 5:
        human_points.append({
            'name':'Average post score',
            'value':100,
            'description':f'User has an average post score of {round(user_data.get("avg_post_score", 0))}.'
            })
    if user_data.get("avg_post_length", 0) > 100:
        human_points.append({
            'name':'Long posts',
            'value':75,
            'description':f'User posts has an average length of {round(user_data.get("avg_post_length", 0))}.'
            })
    if user_data.get("avg_comment_length", 0) > 50:
        human_points.append({
            'name':'Long comments',
            'value':50,
            'description':f'User posts has an average length of {round(user_data.get("avg_comment_length", 0))}.'
            })
    # Тут те що каже що юзер бот
    if not user_data.get("pic") or "default" in user_data["pic"]:
        bot_points.append({
            'name':'No profile picture',
            'value':100,
            'description':f'User has a default profile picture.'
            })
    subreddits = set()
    for post in user_data.get("recent_posts", []):
        subreddits.add(post.get("subreddit"))
    for comment in user_data.get("recent_comments", []):
        subreddits.add(comment.get("subreddit"))

    if len(subreddits) > 30:
        bot_points.append({
            'name':'Too many subreddits',
            'value':(len(subreddits) - 30) * 2.5,
            'description':f'User was active in {(len(subreddits) - 30) * 2.5} subreddits.'
            })

    if user_data["name"].lower().startswith("user") and user_data["name"][4:].isdigit():
        bot_points.append({
            'name':'Generic username',
            'value':150,
            'description':f'User has a generic username.'
            })
    if user_data.get("repetitive_posts", False):
        bot_points.append({
            'name':'Repetitive posts',
            'value':250,
            'description':f'User repetitively posts the same.'
            })
    if user_data.get("repetitive_comments", False):
        bot_points.append({
            'name':'Repetitive comments',
            'value':250,
            'description':f'User repetitively comments the same.'
            })
    if user_data.get("avg_time_between_actions", 0) < 1:
        bot_points.append({
            'name':'Hyperactive behavior',
            'value':200,
            'description':f'User has a hyperactive behavior.'
            })
    if user_data.get("post_to_comment_ratio", 1) > 10:
        bot_points.append({
            'name':'Post to comment ratio',
            'value':150,
            'description':f'User has weird post to comment ratio of {round(user_data.get("post_to_comment_ratio", 1),2)}.'
            })
    if user_data.get("avg_post_length", 0) < 20:
        bot_points.append({
            'name':'Short posts',
            'value':50,
            'description':f'User post are {round(user_data.get("avg_post_length", 0))} characters long on average.'
            })
    if user_data.get("avg_comment_length", 0) < 10:
        bot_points.append({
            'name':'Short comments',
            'value':50,
            'description':f'User comments are {round(user_data.get("avg_post_length", 0))} characters long on average.'
            })
    # --- Score calculation ---
    total_human = sum(factor['value'] for factor in human_points)
    total_bot = sum(factor['value'] for factor in bot_points)

    score = total_bot / (total_human + total_bot + 1e-5)
    bot_likelihood_percent = round(score * 100)

    return {
        "bot_likelihood_percent": bot_likelihood_percent,
        "human_points": human_points,
        "bot_points": bot_points
    }
