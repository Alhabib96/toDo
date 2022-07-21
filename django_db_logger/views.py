from ast import excepthandler
import logging
import re

from django.http import HttpResponse
from flask_login import user_accessed

logger = logging.getLogger('db')
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Imports for Reordering Feature
from django.views import View
from django.shortcuts import redirect
from django.db import transaction

from .models import Task
from .forms import PositionForm


class CustomLoginView(LoginView):
    template_name = 'login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        kwargs={"username": self.request.user.username}['username']
        logger.info("User " +kwargs+ " is successfuly loged in")
        return reverse_lazy('tasks')


class RegisterPage(FormView):
    template_name = 'register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        kwargs={"username": self.request.user.username}['username']
        logger.info("User "+kwargs+" is successfuly registered")
        return super(RegisterPage, self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            kwargs={"username": self.request.user.username}['username']
            logger.info("User "+kwargs+" filtered by \""+search_input+"\"")
            context['tasks'] = context['tasks'].filter(
                title__contains=search_input)

        context['search_input'] = search_input

        
        
        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'task.html'


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'category', 'complete']
    success_url = reverse_lazy('tasks')
    def form_valid(self, form):
        try:
            if form.data['complete'] == 'on':
                completness = 'Yes'
            logger.info("\nAction: Create Task"+".\nTitle: "+ form.data['title'] + ".\nCategory: "+ form.data['category'] + ".\nDescription: "+ form.data['description']+ ".\nCompleted: "+ completness)
        except:
            logger.info("\nAction: Create Task"+".\nTitle: "+ form.data['title'] + ".\nCategory: "+ form.data['category'] + ".\nDescription: "+ form.data['description']+ ".\nCompleted: No")
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'category', 'complete']
    success_url = reverse_lazy('tasks')
    def form_valid(self, form):
        try:
            if form.data['complete'] == 'on':
                completness = 'Yes'
            logger.info("\nAction: Update Task"+".\nTitle: "+ form.data['title'] + ".\nCategory: "+ form.data['category'] + ".\nDescription: "+ form.data['description']+ ".\nCompleted: "+ completness)
        except:
            logger.info("\nAction: Update Task"+".\nTitle: "+ form.data['title'] + ".\nCategory: "+ form.data['category'] + ".\nDescription: "+ form.data['description']+ ".\nCompleted: No")
        form.instance.user = self.request.user
        return super(UpdateView, self).form_valid(form)        



class DeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')        
    def get_queryset(self, **kwargs):
        owner = self.request.user
        # print(self.model.objects.get(id=self.kwargs['pk']).complete)
        if not (self.model.objects.get(id=self.kwargs['pk']).complete):
            logger.warning('Incomplete task "'+self.model.objects.get(id=self.kwargs['pk']).title+'" is about to get deleted')
        return self.model.objects.filter(user=owner)
    

class TaskReorder(View):
    def post(self, request):
        form = PositionForm(request.POST)

        if form.is_valid():
            positionList = form.cleaned_data["position"].split(',')
            with transaction.atomic():
                self.request.user.set_task_order(positionList)

        return redirect(reverse_lazy('tasks'))

def __gen_500_errors(request):
    try:
        1/0
    except Exception as e:
        logger.exception(e)

    return HttpResponse('Hello 500!')

def error_404_view(request, exception):
    logger.error("Page Not Found")
    return render(request, '404.html')