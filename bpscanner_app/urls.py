"""bp_scanner URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from bpscanner_app import views

urlpatterns = [
    path("dashboard", views.dashboard, name='dashboard'),
    path("search", views.search, name='search'),
    path("database", views.database, name='database'),
    path('get-task-info/', views.get_task_info, name="get_task_info"),
    path("search_city/<city>", views.search_city, name="search_city"),
    path("check_person/", views.check_person, name="check_person"),
    path("check_photo/", views.check_photo, name="check_photo"),

    path("people", views.people, name="people")

]