from datetime import datetime
from django.shortcuts import render
from django.http import JsonResponse
from reddit_request import DataGetter, NotFound
from data_app.services import save_analysis_entry, get_analysis_entry, check_if_user_exists, get_date_of_last_analysis, is_last_analysis_recent, serialize_the_persons_data, get_persons_with_query, set_bot_likelihood, random_user_name, get_amount_of_users
from testproject.utils import prepare_data_analysis_page

def homepage(request):
    return render(request, "home.html")

def datapage(request):
    return render(request, "database.html")

def search_data_base_for_account(request):
    query = request.GET.get('query', '')
    page = int(request.GET.get("page", 1))
    limit = int(request.GET.get("limit", 10))

    data = get_persons_with_query(query, page, limit)

    return JsonResponse(data, safe=False)
def get_accounts_data(request):
    page = int(request.GET.get("page", 1))
    limit = int(request.GET.get("limit", 10))
    sort_key = request.GET.get("sort", None)
    sort_dir = request.GET.get("direction", None)

    data = serialize_the_persons_data(page, limit, sort_key, sort_dir)

    return JsonResponse(data, safe=False)

def check_username(request):
    try:
        query1 = request.GET.get('username', '')
        if len(query1) > 1 and query1[1] == "/":
            query=query1[2:]
        else:
            query=query1
        data = {'exists':DataGetter.check_for_errors(query)}
    except NotFound as e:
        data = {'exists':False}
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
    save_analysis_entry(data)
    info = prepare_data_analysis_page(query, data, "just now")
    return render(request, 'analysis.html', info)

def infopage(request):
    return render(request, 'info.html')

def get_random_account(request):
    name = random_user_name()
    return render(request, 'analysis.html', prepare_data_analysis_page(name, get_analysis_entry(name), get_date_of_last_analysis(name)))

def get_analyses_count(request):
    amount = get_amount_of_users()
    return JsonResponse({'count': amount})