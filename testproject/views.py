from django.shortcuts import render
from reddit_request import DataGetter
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
    data = d.get_user_analysis(query)
    info = prepare_data_analysis_page(query, data)
    return render(request, 'analysis.html', info)
