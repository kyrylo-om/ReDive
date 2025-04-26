from datetime import datetime
from collections import defaultdict
from dateutil.relativedelta import relativedelta
from sematics import semantics_analysis
from bot_rank import estimate_bot_likelihood
from data_app.services import set_bot_likelihood


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
    num_subreddits = len(subreddit_activity)

    posting_frequency = 0
    if len(post_times) >= 2:
        post_times.sort()
        total_days = (post_times[-1] - post_times[0]).total_seconds() / (3600 * 24)
        if total_days >= 1:
            posting_frequency = round(len(post_times) / total_days * 7, 2)

    comment_frequency = 0
    if len(comment_times) >= 2:
        comment_times.sort()
        total_days_c = (comment_times[-1] - comment_times[0]).total_seconds() / (
            3600 * 24
        )
        if total_days_c >= 1:
            comment_frequency = round(len(comment_times) / total_days_c * 7, 2)
    total_times = post_times + comment_times
    total_frequency = 0
    if len(total_times) >= 2:
        total_times.sort()
        total_days_all = (total_times[-1] - total_times[0]).total_seconds() / (
            3600 * 24
        )
        if total_days_all >= 1:
            total_frequency = round(len(total_times) / total_days_all * 7, 2)
    avg_post_upvote_ratio = (
        round(sum(post_upvote_ratios) / len(post_upvote_ratios), 2)
        if post_upvote_ratios
        else 0
    )
    avg_comment_upvote_ratio = round(up_comment / comment_amount, 2) if comment_amount else 0
    avg_total_upvote_ratio = round(up + up_comment / total_items, 2) if total_items else 0

    bot_analysis = estimate_bot_likelihood(data)
    set_bot_likelihood(username, bot_analysis["bot_likelihood_percent"])

    posts_text = " ".join(post["body"] for post in data.get("recent_posts", ""))
    comments_text = " ".join(
        comment["body"] for comment in data.get("recent_comments", "")
    )

    full_text = posts_text + " " + comments_text

    word_counts, analysis = semantics_analysis(full_text)
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
            "comments_under_post_amount": round(comments_under_post / posts_amount, 2),
            "averal_comments": comment_amount,
            "num_subreddits": num_subreddits,
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
            "word_counts": word_counts,
            "analysis": analysis,
            "total_frequency": total_frequency,
            "posting_frequency": posting_frequency,
            "comment_frequency": comment_frequency,
            "avg_post_ratio": avg_post_upvote_ratio,
            "avg_comment_ratio": avg_comment_upvote_ratio,
            "avg_total_ratio": avg_total_upvote_ratio,
            "own_comments": own_comments,
            "overall_upvotes": round((up + up_comment) / (posts_amount + comment_amount), 2),
            "total_up_v_down": up_v_down,
        }
    }