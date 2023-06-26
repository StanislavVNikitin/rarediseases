from django.urls import path

from .apps import MainappConfig
from .views import *
app_name = MainappConfig.name

urlpatterns = [
    path("disease/<str:slug>", DiseaseDetaileView.as_view(), name="disease"),
    path("tag/<str:slug>", DiseaseByTag.as_view(), name="tag"),
    path("search/", Search.as_view(), name="search"),
    path("contacts/", ContactsPageView.as_view(), name="contacts"),
    path('', HomeView.as_view(), name='home'),
]