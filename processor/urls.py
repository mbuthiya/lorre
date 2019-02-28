from django.urls import path 

from . import views

urlpatterns = [
    path('', views.overview_week,name="week"),
    path('trend/', views.overview_trend,name="trend"),
    path('farms/', views.farms_all,name="farms"),
    path('reports/', views.farms_report,name="reports"),
    path('workers/', views.farms_workers,name="workers"),
    path('requests/', views.farms_request,name="requests"),
    path('farms/<int:id>', views.single_farm,name="farm"),
    path('workers/<int:id>', views.single_worker,name="worker"),
    path('reports/<int:id>', views.single_report,name="report"),
    path('login/',views.loginFunction,name="login"),
    path('signup/',views.signup,name="signup")
]


