from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.views.generic import CreateView,DetailView,ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from .models import Thought
from .forms import ThoughtForm
from django.urls import reverse_lazy
from braces.views import SelectRelatedMixin
import datetime
from django.utils import timezone
import json




class ThougthList(LoginRequiredMixin,ListView):
    # model = Thought
    template_name = 'thoughts/thoughts.html'

    def get_queryset(self,quesryset=None):
        return Thought.objects.filter(user=self.request.user)

class Graf(LoginRequiredMixin,ListView):
    # model = Thought
    template_name = 'thoughts/graf.html'
    # template_name = 'thoughts/graf_2.html'

    def get_queryset(self,quesryset=None):
        return Thought.objects.filter(user=self.request.user)

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        term = timezone.now() - datetime.timedelta(days=7)
        thoughts_qs = user.thoughts.filter(recorded_at__gte = term).order_by('recorded_at')
        data = json.dumps({'labels':[th.recorded_at.strftime('%d-%m-%Y') for th in thoughts_qs],
                'scores':[th.score*-1 for th in thoughts_qs]
        })
        print("method context calling........")
        print("data",data)
        context['chart_data'] = data
        return context
"""
data 

method context calling........
data {
    "labels": ["04-06-2020", "09-06-2020", "10-07-2020", "10-07-2020", "10-07-2020", "10-07-2020"], "scores": [35, 35, 20, 20, 25, 10]}

data 
["04-06-2020", "09-06-2020", "10-07-2020", "10-07-2020", "10-07-2020", "10-07-2020", "10-07-2020", "11-07-2020"], 
[-35, -35, -20, -20, -25, -10, -20, -10]}    
"""        
            


class Dashboard(LoginRequiredMixin,SelectRelatedMixin,DetailView):
    """detailview for the user and it's related data"""
    model = User
    select_related = 'thoughts'
    template_name = 'thoughts/dashboard.html' 

    def get_object(self,quesryset=None):
        user = self.request.user 

    

class CreateThought(LoginRequiredMixin,CreateView):
    form_class = ThoughtForm
    success_url = reverse_lazy('thoughts:dashboard')

    def form_valid(self,form):
        form.instance.user = self.request.user
        return super().form_valid(form)



def cook(request):
    #print(len('75hutyb6kplyfor1l0zys9qg89k7388m'))
    # print('session key',request.session.get('session_keykeys'))
    
    # print('items',request.session.has_key('id'))
    # print('values',request.session.is_empty())
    
    # dic = request.COOKIES
    # for k,v in request.COOKIES.items():
    #     print(k,"        ",v)  
    # response = HttpResponseRedirect('/url/to_your_home_page')    
    response  = HttpResponse('have a nice time')
    # response  = HttpResponseRedirect('/thoughts/dashboard/')
    #response.delete_cookie('zoo')        
    # print("length of req.COOKIES dict:",len(dic))
    #res.set_cookie("nio",1111,max_age=1000)
    
   
    return  response
   



    



    

