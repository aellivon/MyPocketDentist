from django.conf.urls import url, include
from Disease import views


urlpatterns = [
	
    # The url for all disease

 	url(r'^ListOfAllDiseases/', 
        views.GetListOfAllDisease.as_view(),name="AllDiseases"),


 	# The url for disease profile

    url(r'^DiseaseProfile/(?P<profile_id>[\w|\W]+)/$', 
        views.ShowDiseaseProfile.as_view(),name="disease_profile"),


    # The url for search disease


    url(r'^SearchDiseaseProfile/(?P<search>[\w|\W]+)/$', 
        views.SearchDiseaseProfile.as_view(),name="search_disease_profile"),

]


















