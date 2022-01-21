from django.shortcuts import render,redirect,get_object_or_404,reverse,HttpResponse
from django.core.paginator import Paginator
from django.views.generic import DetailView,UpdateView,ListView
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,Http404,HttpResponse
from django.forms.models import model_to_dict
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Q
from .forms import *
import datetime

records_page = 8

def main(request): #main page, showing ideas with fresh comments/главная страница, показывает идеи со свежими комментариями
    return render(request,'Records.html',{'data':Paginator(Idea.objects.order_by('-update'),records_page).page(1),
                                          'filter':'popular','title':'Main page','login':AuthenticationForm})

def popular(request,pg=None): #ideas with fresh comments/идеи со свежими комментариями
    if not pg:
        return redirect('main')
    return render(request,'Records.html',{'data':Paginator(Idea.objects.order_by('-update'),records_page).page(pg),
                                          'filter':'popular','title':'Popular ideas','login':AuthenticationForm})

class IdeaEdit(UserPassesTestMixin,UpdateView):#editing idea/редактор идей
    model = Idea
    template_name = 'Editor.html'
    fields=['title','descr']
    def test_func(self, **kwargs):
        return self.request.user.pk==self.get_object().user.pk
    def get_absolute_url(self):
        return redirect('record',pk=self.get_object().pk)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['one'] = self.object
        context['title'] = self.object.title
        context['user'] = self.request.user
        context['tags'] = Tag.objects.all()
        context['one_tags'] = '-'.join([str(i.pk) for i in self.object.tags.all()])
        return context

class IdeaView(DetailView): #запись/game idea
    model = Idea
    template_name = 'Record.html'
    comments = 15
    def get_object(self, **kwargs):
        idea = Idea.objects.get(pk=self.kwargs['pk'])
        return idea

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['one'] = self.object
        context['title'] = self.object.title
        context['user'] = self.request.user
        context['login'] = AuthenticationForm
        context['form'] = CommentForm
        try:
            context['comms'] = Paginator(self.object.comms.filter(is_reply=False).all(),self.comments).page(
                self.kwargs['pg'])
        except:
            context['comms'] = Paginator(self.object.comms.filter(is_reply=False).all(),self.comments).page(1)
        return context

def editor(request,pk):#save after updating\сохранение после редактирования
    obj = Idea.objects.get(pk=pk)
    tags = request.POST['tags_id']
    if tags.split('-')[1:-1]:
        if request.POST['title']:
            obj.title = request.POST.get('title')
        obj.descr = request.POST.get('descr')
        obj.tags.set([Tag.objects.get(pk=int(i)) for i in tags.split('-')[1:-1]])
        obj.save()
    return redirect('record',pk=obj.pk)

def records(request,pg=None): #ideas ordered by creating date/идеи по порядку выкладывания
    if not pg:
        pg = 1
    return render(request,'Records.html',{'data':Paginator(Idea.objects.all(),records_page).page(pg),'login':AuthenticationForm,
                                          'filter':'all','user':request.user,'title':'All records'})

@login_required
def create_idea(request): #saving new idea/новая запись
    if request.method == 'POST':
        post = request.POST
        tags = post['tags_id']
        data = IdeaForm(request.POST)
        data = data.save(commit=False)
        data.user = request.user
        if tags.split('-')[1:-1]:
            data.save()
            for i in tags.split('-')[1:-1]:
                data.tags.add(int(i))
            data.save()
            return redirect('record',pk=data.pk)
    return render(request,'NewIdea.html',{'user':request.user,'title':'New record',
                                          'form':IdeaForm(),'tags':Tag.objects.all()})

@login_required
def comment(request,pk): #комментарий/commenting
    if request.method == 'POST':
        idea = Idea.objects.get(pk=pk)
        data = CommentForm(request.POST)
        data = data.save(commit=False)
        data.user = request.user
        data.idea = idea
        data.save()
        idea.update = datetime.datetime.now()
        idea.save()
        return redirect('record',pk=pk)

@login_required
def reply(request,com): #ответ на комментарий/comment replying
    if request.method == 'POST':
        c = Comment.objects.get(pk=com)
        data = ReplyForm(request.POST)
        data = data.save(commit=False)
        data.user = request.user
        data.parent = c
        data.main_parent = c
        data.idea = c.idea
        data.is_reply = True
        if c.is_reply:
            if c.main_parent:
                data.main_parent = c.main_parent
            else:
                data.main_parent = c.parent
        data.main_parent.update = datetime.datetime.now()
        data.main_parent.save()
        data.save()
    return redirect('record',pk=data.idea.pk)

class TagsView(ListView): #список тегов/view of tags
    model = Tag
    paginate_by = 20
    template_name = 'Tags.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        data = Paginator(self.model.objects.all(),self.paginate_by)
        page = self.request.GET.get('pg')
        try:
            data = data.page(page)
        except:
            data = data.page(1)
        context['title'] = 'Tags'
        context['user'] = self.request.user
        context['login'] = AuthenticationForm
        context['data'] = data
        return context

class tag(DetailView): #тег и записи к нему/tag_name and records with it
    model = Tag
    template_name = 'Records.html'
    def get_object(self, **kwargs):
        return Tag.objects.get(pk=self.kwargs['pk'])
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        context['user'] = self.request.user
        context['login'] = AuthenticationForm
        context['subs'] = True
        context['tag'] = self.object
        try:
            context['data'] = Paginator(self.object.ideas.all(),records_page).page(self.kwargs['pg'])
        except:
            context['data'] = Paginator(self.object.ideas.all(),records_page).page(1)
        return context

def signup(request): #авторизация/authorization
    if request.method == 'POST':
        form = UserCreationForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request,user)
            return redirect('main')
    form = UserCreationForm()
    return render(request, 'Sign.html', {'title':'Authorization','sign':form})

def Login(request): #аутентификация/authentication
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username, password=password)
        if user:
            login(request,user)
            return redirect('main')
    return redirect('main')

@login_required
def LogOut(request): #выход из аккаунта/log out
    logout(request)
    return HttpResponseRedirect('/')

def user_page(request,pk,pg=None):
    if not pg:
        pg = 1
    us = User.objects.get(pk=pk)
    return render(request,'UserPage.html',{'title':us.username,'us':us,'records':Paginator(us.ideas.all(),records_page).page(pg),
                                           'login':AuthenticationForm})

@login_required
def subs(request,pk): #подписка/subscribing
    t = Tag.objects.get(pk=pk)
    if request.user not in t.subscribers.all():
        t.subscribers.add(request.user)
    else:
        t.subscribers.remove(request.user)
    t.save()
    return redirect('tag',pk=pk)

def user_subs(request,pk,pg=None):
    if not pg:
        pg = 1
    us = User.objects.get(pk=pk)
    return render(request,'Tags.html',{'title':f"{us.username}'s subscribes",'login':AuthenticationForm,'data':Paginator(us.subscribes.all(),5).page(pg)})

def search(request): #search query/поиск по запросу
    return redirect('search',query=request.POST['search'])

def search_results(request,query,pg=None): #search results/результаты поиска
    if not pg:
        pg = 1
    return render(request,'Records.html',{'data':Paginator(Idea.objects.filter(Q(title__icontains=query) | Q(descr__icontains=query)),records_page).page(pg),
                                          'filter':f'search/{query}','title':query,'login':AuthenticationForm})
