from django.shortcuts import render
from reddit_request import DataGetter
from datetime import datetime
from dateutil.relativedelta import relativedelta

def homepage(request):
    return render(request, "home.html")


def datapage(request):
    return render(request, "database.html")

def analysispage(request):
    d = DataGetter()
    query1 = request.GET.get('query', '')
    if query1[1]=="/":
        query=query1[2:]
    else:
        query=query1
    data = d.get_user_analysis(query)
    up_v_down=0
    up=0
    n=0
    up_comment=0
    j=""
    subredits1=''
    subredits2=''
    subredits3=""
    comment_amount=0
    pic= DataGetter.get_reddit_avatar(query)
    date_today = datetime.today().strftime("%B %d %Y")
    date_of_creation =data.get('created_date', [])
    account_age = datetime.today().year - date_of_creation.year
    trophies = len(data.get('trophies', []))
    username = data.get('name')
    if data.get('subreddit').title:
        name = data.get('subreddit').title
    else:
        name = username
    posts_amount=len(data.get('recent_posts', []))
    post_karma=data.get('link_karma')
    comment = len(data.get('recent_comments', []))
    comment_karma=data.get('comment_karma')
    subredits= []
    for i in data.get('recent_posts', []):
        subredits.append(i['subreddit'])
        up_v_down +=i['upvotes_ratio']
        up+=i["score"]
        comment_amount+=i['num_comments']
        n+=1
    for i in data.get('recent_comments', []):
        subredits.append(i['subreddit'])
        up_comment+=i["score"]
    if len(subredits)>=3:
        subredits1="r/"+subredits[0]
        subredits2="r/"+subredits[1]
        subredits3="r/"+subredits[2]
        j=f"and {len(subredits)-3} more"
    elif len(subredits)>=2:
        subredits1="r/"+subredits[0]
        subredits2="r/"+subredits[1]
    elif len(subredits)>=1:
        subredits1="r/"+subredits[0]
    else:
        subredits1="No subreddits"
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
    return render(request, 'analysis.html', {
        "pic":pic,
        "date_today":date_today,
        'date_of_creation': date_of_creation,
        "account_age":account_age,
        "trophies": trophies,
        "username": username,
        "name": name,
        "post":posts_amount,
        "post_karma":post_karma,
        "comment":comment,
        "comment_karma":comment_karma,
        "subredits1":subredits1,
        "subredits2":subredits2,
        "subredits3":subredits3,
        "up": round(up/n,2),
        "up_v_down":round(up_v_down/n,2),
        "comment_amount":round(comment_amount/n,2),
        "averal_comments":comment_amount,
        "j":j,
        "posting_frequency": posting_frequency,
        "up_comment":round(up_comment/n,2),
        "query": query 
    })