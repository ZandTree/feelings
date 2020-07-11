from django.shortcuts import render,reverse,get_object_or_404
from django.views.decorators.http import require_POST

from django.http import HttpResponse,JsonResponse,Http404
from django.core.exceptions import ObjectDoesNotExist
from ..models import Company,CompanyInvite
from ..forms import CompanyForm,CompanyInviteForm,CompanyLeaveForm 
from django.views.generic import CreateView,DetailView,UpdateView,FormView,ListView,RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from braces.views import SetHeadlineMixin
# from datetime import date

      
class Create(LoginRequiredMixin,SetHeadlineMixin,CreateView):
    form_class = CompanyForm
    headline = "Create Company"    
    success_url = reverse_lazy('thoughts:dashboard')
    template_name = 'groups/companies/company_form.html'  
    
    def form_valid(self,form):
        form.instance.created_by = self.request.user
        resp = super().form_valid(form)        
        self.object.members.add(self.request.user)           
        return resp
        
class Detail(LoginRequiredMixin,FormView):
    """ for obj == company, к создал или к которой присоединился чел"""
    form_class = CompanyInviteForm
    template_name = 'groups/companies/company_detail.html'
    
    def get_queryset(self):
        return self.request.user.companies.all()

    def get_success_url(self):
        self.get_object()
        return reverse ('groups:detail-company',kwargs={'slug':self.object.slug})

    def get_object(self):
        self.object = self.request.user.companies.get(slug=self.kwargs['slug'])
        return self.object

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.get_object()
        return context

    def form_valid(self,form):
        """ if form is valid , create a new instance of CompanyInvite class"""
        response = super().form_valid(form)
        CompanyInvite.objects.create(
            from_user = self.request.user,
            to_user = form.invitee,
            company = self.get_object()
        )
        return response

class Edit(LoginRequiredMixin,SetHeadlineMixin,UpdateView):
    form_class = CompanyForm
    headline = "Edit Company"  
    template_name = 'groups/companies/company_form.html'  
    
    def get_queryset(self):        
        return  self.request.user.companies.all()

    def get_headline(self):
        # date = date.today().isoformat()
        # print('date',date)
        return "Edit {}.".format(self.object.name)


class DisplayInvitee(LoginRequiredMixin,ListView):
    template_name = 'groups/companies/invites.html'

    def get_queryset(self):
        return self.request.user.companyinvite_received.filter(status=0)  

class Leave(LoginRequiredMixin,SetHeadlineMixin,FormView):
    """why not re-direct? to know for sure the person whants to leave
    + using generic form for many views
    + object here (via get object) ==> company with slug
    delete from company members an req.user (via.remove)
    """ 
    form_class = CompanyLeaveForm
    template_name = 'groups/companies/company_form.html'
    success_url = reverse_lazy('thoughts:dashboard')

    def get_object(self):
        try:
            self.object= self.request.user.companies.filter(
                            slug=self.kwargs.get('slug')).exclude(
                                created_by = self.request.user).get()
            print("object",self.object)                
            return self.object
        except ObjectDoesNotExist:
            return Http404 

    def get_headline(self):
        self.get_object()
        print("from get_headlines",self.get_object())
        return "Leave {}?".format(self.object.name)

    

    def form_valid(self,form):
        self.get_object()
        #print("all members of the comapny",self.object.members.all())
        self.object.members.remove(self.request.user)
        return super().form_valid(form)


@require_POST
def reject_invite(request):
    data = request.POST.get('uuId',"not found")
    obj = get_object_or_404(CompanyInvite,to_user=request.user,uuid=data,status=0)
    obj.status = 2
    obj.save()
    return JsonResponse({'msg':"You rejected this invitation"})    


@require_POST
def accept_invite(request):
    data = request.POST.get('uuId',"not found")
    obj = get_object_or_404(CompanyInvite,to_user=request.user,uuid=data,status=0)
    obj.status = 1
    obj.save()
    return JsonResponse({'msg':"You accepted this invitation"})     
           
            
