from datetime import datetime
from django.shortcuts import render
from django.http import JsonResponse
from django.core.paginator import Paginator
from reddit_request import DataGetter
from data_app.services import save_analysis_entry, get_analysis_entry, check_if_user_exists, get_date_of_last_analysis, is_last_analysis_recent
from testproject.utils import prepare_data_analysis_page

def homepage(request):
    return render(request, "home.html")

def datapage(request):
    return render(request, "database.html")

def get_accounts_data(request):
    page = int(request.GET.get("page", 1))
    limit = int(request.GET.get("limit", 10))
    sort_key = request.GET.get("sort")
    sort_dir = request.GET.get("direction")

    accounts = Account.objects.all()

    if sort_key and sort_dir:
        direction = "" if sort_dir == "asc" else "-"
        accounts = accounts.order_by(f"{direction}{sort_key}")

    paginator = Paginator(accounts, limit)
    page_obj = paginator.get_page(page)

    data = [{
        "username": acc.username,
        "posts": acc.posts,
        "comments": acc.comments,
        "bot_percentage": acc.bot_percentage
    } for acc in page_obj]

    return JsonResponse(data, safe=False)
def analysispage(request):
    d = DataGetter()
    query1 = request.GET.get('query', '')
    if len(query1) > 1 and query1[1] == "/":
        query=query1[2:]
    else:
        query=query1
    if check_if_user_exists(query) and is_last_analysis_recent(query):
        return render(request, 'analysis.html', prepare_data_analysis_page(query,get_analysis_entry(query), get_date_of_last_analysis(query)))
    data = d.get_user_analysis(query)
    info = prepare_data_analysis_page(query, data, datetime.today().strftime("%B %d %Y"))
    save_analysis_entry(data)
    return render(request, 'analysis.html', info)
