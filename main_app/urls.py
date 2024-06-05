from django.urls import path
from . import views

urlpatterns = [
  path('accounts/signup', views.signup, name='signup'),
  path('', views.home, name='home'),
  path('journals/', views.journals_index, name='journals_index'),
  path('journals/create/', views.journals_create, name='journals_create'),
  path('journals/<int:pk>/update', views.JournalUpdate.as_view(), name='journals_update'),
]