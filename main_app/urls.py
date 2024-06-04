from django.urls import path
from . import views

urlpatterns = [
  path('accounts/signup', views.signup, name='signup'),
  path('', views.home, name='home'),
  path('journals/', views.JournalList.as_view(), name='journals_index'),
]