from django.conf.urls import url, include
from Rules import views

urlpatterns = [

    # The url for the examine view

    url(r'^Examine/(?P<parameters>[\w|\W]+)/(?P<target>[\w|\W]+)/$', 
        views.Examine.as_view(),name="Examine"),

]


















