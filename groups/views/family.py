from django.shortcuts import render,reverse,get_object_or_404
from django.views.decorators.http import require_POST
from django.http import HttpResponse,JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from ..models import Family,FamilyInvite
from ..forms import FamilyForm,FamilyInviteForm,FamilyLeaveForm
from django.views.generic import CreateView,DetailView,UpdateView,FormView,ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from braces.views import SetHeadlineMixin


class Create(LoginRequiredMixin,SetHeadlineMixin,CreateView):
    form_class = FamilyForm
    headline = "Create Family"    
    success_url = reverse_lazy('thoughts:dashboard')
    template_name = 'groups/families/family_form.html'

    def form_valid(self,form):
        form.instance.created_by = self.request.user     
        resp = super().form_valid(form)   
        self.object.members.add(self.request.user)
        return resp


class Detail(LoginRequiredMixin,FormView):
    """form view expects form, form_valid and what to do with valid form"""
    form_class = FamilyInviteForm
    template_name = 'groups/families/family_details.html'

    def get_queryset(self):
        return self.request.user.families.all()

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)    
        context['object'] = self.get_object()
        return context
         
    def get_object(self):
        self.object = self.request.user.families.get(slug=self.kwargs['slug'])
        return self.object
        
    def get_success_url(self):
        self.get_object()
        return reverse ('groups:detail-family',kwargs={'slug':self.object.slug})

    def form_valid(self,form):
        """ if form is valid , create a new instance of FamilyInvite class"""
        response = super().form_valid(form)
        FamilyInvite.objects.create(
            from_user = self.request.user,
            to_user = form.invitee,
            family = self.get_object()
        )
        return response       
    
    
class Edit(LoginRequiredMixin,SetHeadlineMixin,UpdateView):
    form_class = FamilyForm
    template_name = 'groups/families/family_form.html' 

    def get_queryset(self):        
        return  self.request.user.families.all() 

    def get_headline(self):       
        return "Edit {}.".format(self.object.name)

class DisplayInvitee(LoginRequiredMixin,ListView):
    template_name = 'groups/families/invites.html'

    def get_queryset(self):
        return self.request.user.familyinvite_received.filter(status=0)             
    
class Leave(LoginRequiredMixin,SetHeadlineMixin,FormView):
    """object here (via get object) ==> company with slug
    delete from company members an req.user (via.remove)
    
    """ 
    form_class = FamilyLeaveForm
    template_name = 'groups/families/family_form.html'
    success_url = reverse_lazy('thoughts:dashboard')

    def get_object(self):
        try:
            self.object= self.request.user.families.filter(
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
    obj = get_object_or_404(FamilyInvite,to_user=request.user,uuid=data,status=0)
    obj.status = 2
    obj.save()
    return JsonResponse({'msg':"You rejected this invitation"})    


@require_POST
def accept_invite(request):
    data = request.POST.get('uuId',"not found")
    obj = get_object_or_404(FamilyInvite,to_user=request.user,uuid=data,status=0)
    obj.status = 1
    obj.save()
    return JsonResponse({'msg':"You accepted this invitation"})           