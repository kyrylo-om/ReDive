"""
URL configuration for testproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage, name='homepage'),
    path('user/', views.analysispage, name='analysispage'),
    path('database/', views.datapage, name='datapage'),
    path('api/accounts/', views.get_accounts_data, name='get_accounts_data'),
    path('api/check-user/', views.check_username, name='check_username'),
    path('api/accounts/search/', views.search_data_base_for_account, name='search_database'),
    path('infopage/', views.infopage, name='infopage'),
    path('random_analysis/', views.get_random_account, name='random_analysis'),
    path('api/analyses-count/', views.get_analyses_count, name='analyses_count'),
    ]
