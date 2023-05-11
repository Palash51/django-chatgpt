from django.urls import path
from . import views

urlpatterns = [
    path('', views.TodoList.as_view(), name='todo_list'),
    path('<int:pk>/', views.TodoDetail.as_view(), name='todo_detail'),
    path('scrape-data/', views.ScrapeWebSiteData.as_view(), name='scrape_data'),
]
