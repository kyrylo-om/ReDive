from datetime import datetime
from django.shortcuts import render
from reddit_request import DataGetter
from data_app.services import save_analysis_entry, get_analysis_entry, check_if_user_exists, get_date_of_last_analysis, is_last_analysis_recent
from testproject.utils import prepare_data_analysis_page

def homepage(request):
    return render(request, "home.html")

def datapage(request):
    return render(request, "database.html")

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
