import uuid
import boto3
import os
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Journal, Entry, Travel, Wellness, Photo
from .forms import JournalForm, EntryForm, TravelForm, WellnessForm

# Create your views here.
# @login_required -> auth decorator for view functions
# LoginRequiredMixin -> auth mixin for CBV

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('home')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)


def home(request):
  return render(request, 'home.html')


def journals_index(request):
  journals = Journal.objects.filter(user=request.user)
  user = request.user
  return render(request, 'journals/index.html', { 'journals': journals, 'user': user })


@login_required
def journals_create(request):
  error_message = ''
  journal_form = JournalForm(request.POST)
  user = request.user.id
  if journal_form.is_valid():
    new_journal = journal_form.save(commit=False)
    new_journal.user_id = user
    new_journal.save()
    return redirect(journals_index)
  else:
    error_message = "Invalid journal creation - try again"
  return render(request, 'journals/journal_form.html', { 
    'journal_form': journal_form,
    'error_message': error_message
  })


class JournalUpdate(LoginRequiredMixin, UpdateView):
  model = Journal
  fields = ['name']


class JournalDelete(LoginRequiredMixin, DeleteView):
  model = Journal
  success_url = '/journals'


@login_required
def journals_detail(request, journal_id):
  journal = Journal.objects.get(id=journal_id)

  if journal.template == 'H':
    print('wellness')
    wellness = journal.wellness_set.all()
    return render(request, 'journals/detail.html', {
    'journal': journal,
    'wellness': wellness
  })
  elif journal.is_travel():
    print('travel')
    travels = journal.travel_set.all()
    return render(request, 'journals/detail.html', {
    'journal': journal,
    'travels': travels
  })
  if journal.is_empty():
    return render(request, 'journals/detail.html', {
    'journal': journal,
  })

  elif journal.has_entries():
    print('entries')
    entries = journal.entry_set.all()
    return render(request, 'journals/detail.html', {
    'journal': journal,
    'entries': entries,
  })


@login_required
def add_entry(request, journal_id):
  error_message = ''
  journal = Journal.objects.get(id=journal_id)

  if journal.is_travel():
    entry_form = TravelForm(request.POST)
  elif journal.is_wellness():
    entry_form = WellnessForm(request.POST)  
  else:
    entry_form = EntryForm(request.POST)

  journal = journal.id
  if entry_form.is_valid():
    new_entry = entry_form.save(commit=False)
    new_entry.journal_id = journal_id
    new_entry.save()
    return redirect('detail', journal_id=journal_id)
  else:
    error_message = "Invalid entry creation - try again"
  return render(request, 'journals/entry_form.html', { 
    'journal' : journal,
    'entry_form': entry_form,
    'error_message': error_message
  })


class EntryUpdate(LoginRequiredMixin, UpdateView):
  model = Entry
  fields = ['title', 'date', 'body', 'mood', 'notes']


class EntryDelete(LoginRequiredMixin, DeleteView):
  model = Entry
  def get_success_url(self):
    return self.object.get_absolute_url()
  


def entry_detail(request, entry_id):
  entry = Entry.objects.get(id=entry_id)
  return render(request, 'entry/detail.html', {
    'entry': entry
  })


class TravelUpdate(LoginRequiredMixin, UpdateView):
  model = Travel
  fields = ['title', 'date', 'body', 'mood', 'location', 'food', 'weather', 'notes']


class TravelDelete(LoginRequiredMixin, DeleteView):
  model = Travel
  def get_success_url(self):
    return self.object.get_absolute_url()

def travel_detail(request, travel_id):
  travel = Travel.objects.get(id=travel_id)
  return render(request, 'entry/travel_detail.html', {
    'travel': travel
  })
  
class WellnessUpdate(LoginRequiredMixin, UpdateView):
  model = Wellness
  fields = ['title', 'body', 'date', 'mood', 'affirmation', 'sleep', 'food', 'notes']   


class WellnessDelete(LoginRequiredMixin, DeleteView):
  model = Wellness
  def get_success_url(self):
    return self.object.get_absolute_url()
  
  
def wellness_detail(request, w_id):
  wellness = Wellness.objects.get(id=w_id)
  return render(request, 'entry/wellness_detail.html', {
    'wellness': wellness
  })

def add_photo(request, travel_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            # build the full url string
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            # we can assign to cat_id or cat (if you have a cat object)
            Photo.objects.create(url=url, travel_id=travel_id)
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
    return redirect('travel_detail', travel_id=travel_id)


def travels_index(request):
  journals = Journal.objects.filter(user=request.user, template = 'T')
  user = request.user
  return render(request, 'journals/index.html', { 'journals': journals, 'user': user })


def wellness_index(request):
  journals = Journal.objects.filter(user=request.user, template = 'H')
  user = request.user
  return render(request, 'journals/index.html', { 'journals': journals, 'user': user })


def personal_index(request):
  journals = Journal.objects.filter(user=request.user, template = 'P')
  user = request.user
  return render(request, 'journals/index.html', { 'journals': journals, 'user': user })



class PhotoDelete(LoginRequiredMixin, DeleteView):
  model = Photo
  def get_success_url(self):
    return self.object.get_absolute_url()