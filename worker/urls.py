from django.urls import path
from django.conf.urls.static import static
from django.conf import settings


from . import views

urlpatterns = [
    path("", views.loginWorker, name="worker-login"),
   path("farms/",views.farms,name="worker-farms"),
   path("farms/<int:id>",views.farm,name="worker-farm"),
    path("farms/<int:id>/<int:season>/report", views.new_report, name="new-report"),
   path("report/<int:id>",views.report,name="report")
]
