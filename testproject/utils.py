from datetime import datetime
from collections import defaultdict
from dateutil.relativedelta import relativedelta
from reddit_request import DataGetter


def prepare_data_analysis_page(query, data, today):
    up_v_down=0
    up=0
    n=0
    up_comment=0
    j=0
    comment_amount=0
    date_today = today
    date_of_creation =data.get('created_date', [])
    account_age = datetime.today().year - date_of_creation.year
    trophies = len(data.get('trophies', []))
    username = data.get('name')
    if data.get('subreddit')['title']:
        name = data.get('subreddit')['title']
    else:
        name = username
    posts_amount=len(data.get('recent_posts', []))
    post_karma=data.get('link_karma')
    comment_amount= len(data.get('recent_comments', []))
    comment_karma=data.get('comment_karma')
    for i in data.get('recent_posts', []):
        up_v_down +=i['upvotes_ratio']
        up+=i["score"]
        comment_amount+=i['num_comments']
        n+=1
    for i in data.get('recent_comments', []):
        up_comment+=i["score"]
    subreddits_stats = defaultdict(lambda: {"posts": 0, "comments": 0, "upvotes": 0})

    for post in data.get('recent_posts', []):
        sr = post['subreddit']
        subreddits_stats[sr]["posts"] += 1
        subreddits_stats[sr]["upvotes"] += post["score"]

    for comment in data.get('recent_comments', []):
        sr = comment['subreddit']
        subreddits_stats[sr]["comments"] += 1
        subreddits_stats[sr]["upvotes"] += comment["score"]

    subreddit_activity = sorted([{"name": f"r/{k}", **v} for k, v in subreddits_stats.items()],key=lambda x: x["upvotes"],reverse=True)
    j = len(subreddit_activity)
    posts = data.get('recent_posts', [])
    posts_amount = len(posts)
    posting_frequency = 0
    if posts:
        try:
            post_dates = [p['created_date'] for p in posts if p.get('created_date')]
            oldest_post_date = min(post_dates)
            today = datetime.today()
            delta = relativedelta(today, oldest_post_date)
            months = delta.years * 12 + delta.months + 1  
            posting_frequency = round(posts_amount / months, 2)
        except Exception as e:
            print("Error calculating posting frequency:", e)
    if n == 0:
        n = 1

    return {
        "pic":data['pic'],
        "date_today":date_today,
        'date_of_creation': date_of_creation,
        "account_age":account_age,
        "trophies": trophies,
        "username": username,
        "name": name,
        "post":posts_amount,
        "post_karma":post_karma,
        "comment":comment_amount,
        "comment_karma":comment_karma,
        "up": round(up/n,2),
        "up_v_down":round(up_v_down/n,2),
        "comment_amount":round(comment_amount/n,2),
        "averal_comments":comment_amount,
        "j":j,
        "k":j-3,
        "posting_frequency": posting_frequency,
        "up_comment":round(up_comment/n,2),
        "subreddit_activity": subreddit_activity,
        "subreddit_names": [sub['name'] for sub in subreddit_activity][:3],
        "query": query,
        "posts": data['recent_posts'],
        'comments': data['recent_comments']
    }