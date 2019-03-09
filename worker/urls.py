from django.urls import path
from django.conf.urls.static import static
from django.conf import settings


from . import views

urlpatterns = [
    path("", views.loginWorker, name="worker-login"),
    path("farms/",views.farms,name="worker-farms"),
    path("newseason/",views.new_season,name="newseason"),
    path("farms/<int:id>",views.farm,name="worker-farm"),
    path("farms/<int:id>/<int:season>/report", views.new_report, name="new-report"),
    path("report/<int:id>",views.report,name="report"),
    path("report/<int:id>/newcomment",views.newComment,name="newcomment"),
    path("report/<int:id>/cropInfo",views.new_crop_info,name="new-crop-info"),
    path("report/<int:id>/cropManage",views.new_crop_manage,name="new-crop-manage"),
    path("report/<int:id>/cropInput",views.new_crop_Input,name="new-crop-manage"),
    path("report/<int:id>/newRequest",
         views.new_crop_Request, name="new-crop-request"),

]
