from datetime import datetime
from collections import defaultdict
from dateutil.relativedelta import relativedelta
from reddit_request import DataGetter


def prepare_data_analysis_page(query, data, today):
    d = DataGetter()
    up_v_down=0
    up=0
    n=0
    c=0
    up_comment=0
    j=0
    comment_amount=0
    post_text=""
    date_today = today
    date_of_creation =data.get('created_date', [])
    account_age = datetime.today().year - date_of_creation.year
    trophies = data.get('trophies', [])
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
        if n<50:
            post_text+=i["title"]+" "
            try:
                post_text+=i["body"]+" "
            except KeyError:
                pass
        n+=1
    for i in data.get('recent_comments', []):
        up_comment+=i["score"]
        if c<50:
            try:
                post_text += i["body"] + " "
            except KeyError:
                pass
        c+=1
    subreddits_stats = defaultdict(lambda: {"posts": 0, "comments": 0, "upvotes": 0})

    # ??? why do you iterate over the same lists twice
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
    try:
        post_times = [
            p["created_date"]
            for p in posts
            if isinstance(p.get("created_date"), datetime)
        ]
        if len(post_times) >= 2:
            post_times.sort()
            total_days = (post_times[-1] - post_times[0]).total_seconds() / (3600 * 24)
            if total_days >= 1:
                posting_frequency = round(len(post_times) / total_days * 7, 2)
    except Exception as e:
        print("Error calculating weekly posting frequency:", e)
    # will be needed when we will use semantics:
    # semantics_list, semantics_analysis = d.semantics_analysis(post_text)
    if n == 0:
        n = 1
    return {
        "data":{
            "pic":data['pic'],
            "date_today":date_today,
            'date_of_creation': date_of_creation,
            "account_age":account_age,
            "trophies": trophies,
            "username": username,
            "name": name,
            "post_count":posts_amount,
            "post_karma":post_karma,
            "comment_count":comment_amount,
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
            "subreddit_names": [sub['name'] for sub in subreddit_activity],
            "query": query,
            "posts": data['recent_posts'],
            'comments': data['recent_comments']
        }
    }
