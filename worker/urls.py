from django.urls import path
from django.conf.urls.static import static
from django.conf import settings


from . import views

urlpatterns = [
    path("", views.loginWorker, name="worker-login"),
   path("farms/",views.farms,name="worker-farms"),
   path("farms/<int:id>",views.farm,name="worker-farm")
]
