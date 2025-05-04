from datetime import datetime
from collections import defaultdict
from dateutil.relativedelta import relativedelta
from sematics import semantics_analysis
from data_app.services import set_bot_likelihood
import numpy as np


def prepare_data_analysis_page(query, data, analysis_date):
    up_v_down = 0
    up = 0
    comments_under_post=0
    up_comment = 0
    own_comments = 0
    post_times = []
    comment_times = []
    post_upvote_ratios = []
    total_items = 0
    date_of_creation = data.get("created_date", [])
    account_age = datetime.today().year - date_of_creation.year
    trophies = data.get("trophies", [])
    username = data.get("name")
    if data.get("subreddit")["title"]:
        name = data.get("subreddit")["title"]
    else:
        name = username
    posts_amount = max(1, len(data.get("recent_posts", [])))
    post_karma = data.get("link_karma")
    comment_amount = max(1, len(data.get("recent_comments", [])))
    comment_karma = data.get("comment_karma")

    subreddits_stats = defaultdict(lambda: {"posts": 0, "comments": 0, "upvotes": 0})
    for i in data.get("recent_posts", []):
        up_v_down += i.get("upvotes_ratio", 0)
        up += i.get("score", 0)
        post_upvote_ratios.append(i.get("upvotes_ratio", 0))
        comments_under_post += i ["num_comments"]
        total_items += 1
        sr = i["subreddit"]
        subreddits_stats[sr]["posts"] += 1
        subreddits_stats[sr]["upvotes"] += i.get("score", 0)

        if isinstance(i.get("created_date"), datetime):
            post_times.append(i["created_date"])

    for i in data.get("recent_comments", []):
        score = i.get("score", 0)
        up_comment += score
        total_items += 1
        sr = i["subreddit"]
        subreddits_stats[sr]["comments"] += 1
        subreddits_stats[sr]["upvotes"] += score
        if i.get("is_submitter"):
            own_comments += 1
        if isinstance(i.get("created_date"), datetime):
            comment_times.append(i["created_date"])
    subreddit_activity = sorted(
        [{"name": f"r/{k}", **v} for k, v in subreddits_stats.items()],
        key=lambda x: x["upvotes"],
        reverse=True,
    )

    comments_under_post_amount = round(comments_under_post / posts_amount, 2)

    posting_frequency = 0
    if len(post_times) >= 2:
        post_times.sort()
        total_days = max((post_times[-1] - post_times[0]).total_seconds() / (
            3600 * 24
        ), 1)
        posting_frequency = round(len(post_times) / total_days, 2)

    comment_frequency = 0
    if len(comment_times) >= 2:
        comment_times.sort()
        total_days_c = max((comment_times[-1] - comment_times[0]).total_seconds() / (
            3600 * 24
        ), 1)
        comment_frequency = round(len(comment_times) / total_days_c, 2)
    total_times = post_times + comment_times
    total_frequency = 0
    if len(total_times) >= 2:
        total_times.sort()
        total_days_all = max((total_times[-1] - total_times[0]).total_seconds() / (
            3600 * 24
        ), 1)
        total_frequency = round(len(total_times) / total_days_all, 2)
    avg_post_upvote_ratio = (
        round(sum(post_upvote_ratios) / len(post_upvote_ratios), 2)
        if post_upvote_ratios
        else 0
    )
    avg_comment_upvote_ratio = round(up_comment / comment_amount, 2) if comment_amount else 0
    avg_total_upvote_ratio = round(up + up_comment / total_items, 2) if total_items else 0


    posts_text = " ".join(post["body"] for post in data.get("recent_posts", ""))
    comments_text = " ".join(
        comment["body"] for comment in data.get("recent_comments", "")
    )

    full_text = posts_text + " " + comments_text

    semantics = semantics_analysis(full_text)

    avg_post_length = int(np.mean([len(p.get("body", "")) + len(p.get("title", "")) for p in data["recent_posts"]]) if len(data.get("recent_posts", [])) > 0 else 0)
    avg_comment_length = int(np.mean([len(c["body"]) for c in data["recent_comments"]]) if len(data.get("recent_comments", [])) > 0 else 0)
    avg_submission_length = int(np.mean([len(p.get("body", "")) + len(p.get("title", "")) for p in data["recent_posts"]] + 
                                  [len(c["body"]) for c in data["recent_comments"]]) if total_items > 0 else 0)

    def get_bot_likelihood_percent(user_data):
        """Estimate the likelihood of a user being a bot."""
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
        if account_age > 3:
            human_points.append({
                'name':'Old account',
                'value': 50 * account_age - 3,
                'description':'User has an old account.'
                })
        num_trophies = len(user_data.get("trophies", []))
        if num_trophies:
            human_points.append({
                'name':'Trophies',
                'value':num_trophies * 15,
                'description':f'User has {num_trophies} trophies.'
                })
        if avg_post_upvote_ratio > 0.95:
            human_points.append({
                'name':'High post upvote ratio',
                'value':100,
                'description':f'User has a high post upvote ratio of {avg_post_upvote_ratio}.'
                })
        if avg_comment_upvote_ratio > 15:
            human_points.append({
                'name':'High comment upvote ratio',
                'value':100,
                'description':f'User has a high comment upvote ratio of {avg_comment_upvote_ratio}.'
                })
        #Bot points
        if not user_data.get("pic") or "default" in user_data["pic"]:
            bot_points.append({
                'name':'No profile picture',
                'value':50,
                'description':f'User has a default profile picture.'
                })
        if avg_post_upvote_ratio and avg_post_upvote_ratio <= 0.8:
            bot_points.append({
                'name':'Low post upvote ratio',
                'value': round(100 + 1000 * (0.8 - avg_post_upvote_ratio), 2),
                'description':f'User has a low post upvote ratio of {avg_post_upvote_ratio}.'
                })
        if avg_comment_upvote_ratio <= 5:
            bot_points.append({
                'name':'Low comment upvote ratio',
                'value':150 * 1/avg_comment_upvote_ratio if avg_comment_upvote_ratio > 0 else 150,
                'description':f'User has a low comment upvote ratio of {avg_comment_upvote_ratio}.'
                })
        comments_per_post = comments_under_post / posts_amount if posts_amount > 0 else 0
        if comments_per_post < 4:
            bot_points.append({
                'name':'Low comments per post',
                'value':200 * 1/comments_under_post_amount if comments_under_post_amount > 1 else 200,
                'description':f'User has a low average of {comments_under_post_amount} comments per each of their post.'
                })
        if comment_frequency > 4:
            bot_points.append({
                'name':'High comment frequency',
                'value':25 * comment_frequency,
                'description':f'User comments with a high frequency of {comment_frequency} comments per day.'
                })
        if posting_frequency > 3:
            bot_points.append({
                'name':'High posting frequency',
                'value':25 * posting_frequency,
                'description':f'User posts with a high frequency of {comment_frequency} posts per day.'
                })

        total_human = sum(factor['value'] for factor in human_points)
        total_bot = sum(factor['value'] for factor in bot_points)

        score = total_bot / (total_human + total_bot + 1e-5)
        bot_likelihood_percent = round(score * 100)

        return {
            "bot_likelihood_percent": bot_likelihood_percent,
            "human_points": human_points,
            "bot_points": bot_points
        }

    bot_analysis = get_bot_likelihood_percent(data)
    set_bot_likelihood(username, bot_analysis["bot_likelihood_percent"])
    return {
        "data": {
            "pic": data["pic"],
            "analysis_date": analysis_date,
            "date_of_creation": date_of_creation,
            "account_age": account_age,
            "trophies": trophies,
            "username": username,
            "name": name,
            "post_count": posts_amount,
            "post_karma": post_karma,
            "post_upvotes": up,
            "comment_count": comment_amount,
            "comment_karma": comment_karma,
            "comment_upvotes": up_comment,
            "up": round(up / posts_amount, 2),
            "comments_under_post_amount": comments_under_post_amount,
            "averal_comments": comment_amount,
            "up_comment": round(up_comment / comment_amount, 2),
            "subreddit_activity": subreddit_activity,
            "subreddit_names": [sub["name"] for sub in subreddit_activity],
            "query": query,
            "posts": data["recent_posts"],
            "comments": data["recent_comments"],
            "human_likelihood_percentage": 100 - bot_analysis["bot_likelihood_percent"],
            "bot_likelihood_percentage": bot_analysis["bot_likelihood_percent"],
            "human_points": bot_analysis["human_points"],
            "bot_points": bot_analysis["bot_points"],
            "top_words": semantics['top_words'],
            "polarity": semantics['sentiment']['polarity'],
            "subjectivity": semantics['sentiment']['subjectivity'],
            "total_frequency": total_frequency,
            "posting_frequency": posting_frequency,
            "comment_frequency": comment_frequency,
            "avg_post_ratio": avg_post_upvote_ratio,
            "avg_comment_ratio": avg_comment_upvote_ratio,
            "avg_total_ratio": avg_total_upvote_ratio,
            "own_comments": own_comments,
            "overall_upvotes": round((up + up_comment) / (posts_amount + comment_amount), 2),
            "total_up_v_down": up_v_down,
            "avg_post_length": avg_post_length,
            "avg_comment_length": avg_comment_length,
            "avg_submission_length": avg_submission_length
        }
    }