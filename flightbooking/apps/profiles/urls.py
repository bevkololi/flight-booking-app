from django.urls import path
from .views import ProfileListView, ProfileGetView

app_name = 'profiles'

urlpatterns = [
    path('', ProfileListView.as_view(), name="get-profiles"),
    path('<str:username>/', ProfileGetView.as_view(), name='profiles'),
]
