from django.contrib.auth.views import LoginView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView, FormView
from django.urls import reverse_lazy
from .models import Task
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.db.models import Q

# Create your views here.

def custom_page_not_found_view(request, exception):
    return render(request, "errors/404.html", {})

class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    # fiels = '__all__'                     
    redirect_authenticated_user = True    

    def get_success_url(self):
        return reverse_lazy('taskList')

class RegisterPage(FormView):
    template_name = 'base/registration.html'
    form_class = UserCreationForm
    # redirect_authenticated_user = True   THIS NOT WORKING HERE
    success_url = reverse_lazy('taskList')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user) 
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('taskList')
        return super(RegisterPage, self).get(*args, **kwargs)   

class TaskList(LoginRequiredMixin,ListView):
    login_url = 'login'
    model = Task
    context_object_name = "all_tasks"    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_tasks'] = context['all_tasks'].filter(user=self.request.user)
        context['count'] = context['all_tasks'].filter(complete=False).count()

        search_input = self.request.GET.get('search-value') or ''
        if search_input:
            context['all_tasks'] = context['all_tasks'].filter(
                Q(title__startswith=search_input) | Q(title__icontains=search_input))

        context['search_input'] = search_input

        return context

class TaskDetail(LoginRequiredMixin,DetailView):
    login_url = "login"
    model = Task
    context_object_name= "all_tasks"
    template_name = "base/task_detail.html"

class TaskCreate(LoginRequiredMixin,CreateView):
    login_url = "login"
    model = Task
    fields = ['title','description','complete']
    # task_form.html

    success_url = reverse_lazy('taskList')
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin,UpdateView):
    login_url = "login"
    model = Task
    fields = ['title','description','complete']
    success_url = reverse_lazy('taskList')

class TaskDelete(LoginRequiredMixin,DeleteView):
    login_url = "login"
    model = Task
    context_object_name = "Tasks"
    template_name = "base/confirm_delete.html"
    success_url = reverse_lazy('taskList')    
