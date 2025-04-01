from django.shortcuts import render
from reddit_request import DataGetter
import random
from datetime import datetime

def homepage(request):
    return render(request, "home.html")


def datapage(request):
    return render(request, "database.html")

def indexpage(request):
    d = DataGetter()
    query1 = request.GET.get('query', '')
    if query1[1]=="/":
        query=query1[2:]
    else:
        query=query1
    data = d.get_user_analysis(query)
    up_v_down=0
    n=0
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
    subredits= [data.get('recent_posts', [])[0]['subreddit'],data.get('recent_posts', [])[1]['subreddit'],data.get('recent_posts', [])[3]['subreddit']]
    for i in data.get('recent_posts', []):
        up_v_down +=i['score']
        n+=1

    return render(request, 'index.html', {
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
        "subredits1":subredits[0],
        "subredits2":subredits[1],
        "subredits3":subredits[2],
        "up_v_down":up_v_down/n,
        "query": query 
    })