from django.urls import path
from . import views

urlpatterns = [
  path('accounts/signup', views.signup, name='signup'),
  path('', views.home, name='home'),
  path('journals/', views.journals_index, name='journals_index'),
  path('journals/create/', views.journals_create, name='journals_create'),
  path('journals/<int:pk>/update/', views.JournalUpdate.as_view(), name='journals_update'),
  path('journals/<int:pk>/delete/', views.JournalDelete.as_view(), name='journals_delete'),
  path('journals/<int:journal_id>/', views.journals_detail, name='detail'),
  path('journals/<int:journal_id>/add_entry/', views.add_entry, name='add_entry'),
  path('entries/<int:pk>/update/', views.EntryUpdate.as_view(), name='entry_update'),
  path('entries/<int:pk>/delete/', views.EntryDelete.as_view(), name='entry_delete'),
  path('entries/<int:entry_id>/', views.entry_detail, name='entry_detail'),
]

