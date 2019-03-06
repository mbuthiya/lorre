from django.urls import path 
from django.conf.urls.static import static
from django.conf import settings


from . import views

urlpatterns = [
    path('', views.overview_week,name="week"),
    path('trend/', views.overview_trend,name="trend"),
    path('farms/', views.farms_all,name="farms"),
    path('workers/', views.farms_workers,name="workers"),
    path('workers/new/', views.new_worker,name="newWorker"),
    path('farm/<int:id>', views.single_farm,name="singleFarm"),
    path('reports/<int:id>', views.single_report,name="report"),
    path('login/',views.loginFunction,name="login"),
    path('signup/',views.signup,name="signup"),
    path("logout/",views.logoutFunction, name="logout"),
    path("profile/<int:id>",views.profile,name="profile")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
