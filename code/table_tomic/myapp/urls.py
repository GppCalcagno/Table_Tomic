from django.urls import path
from . import views

urlpatterns = [
    path("",views.home,name="home"),
    path("add_user/",views.add_user,name="add_user"),
    path("result/",views.result,name="result"),
    path("ranking/",views.ranking,name="ranking"),
    path("about/",views.about,name="about"),
    path("wip/",views.wip,name="wip"),

]