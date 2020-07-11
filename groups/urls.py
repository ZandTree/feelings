from django.urls import path,include
from .views import company,family
# CreateCompany,CreateFamily,CompanyDetail,FamilyDetail
app_name = 'groups'



company_patterns = [
    path('create/',company.Create.as_view(),name="create-company"),
    path('view-detail/<slug:slug>',company.Detail.as_view(),name="detail-company"),
    path('edit/<slug:slug>',company.Edit.as_view(),name="edit-company"),
    path('leave/<slug:slug>',company.Leave.as_view(),name="leave-company"),
    path('invites/',company.DisplayInvitee.as_view(),name="comp-invitations"),
    path('reject-invite/',company.reject_invite,name="comp-reject-invitation"),
    path('accept-invite/',company.accept_invite,name="comp-accept-invitation"),
]


family_patterns = [
    path('create/',family.Create.as_view(),name="create-family"),
    path('view-detail/<slug:slug>',family.Detail.as_view(),name="detail-family"),
    path('edit/<slug:slug>',family.Edit.as_view(),name="edit-family"),
    path('leave/<slug:slug>',family.Leave.as_view(),name="leave-family"),
    path('invites/',family.DisplayInvitee.as_view(),name="fam-invitations"),
    path('reject-invite/',family.reject_invite,name="fam-reject-invitation"),
    path('accept-invite/',family.accept_invite,name="fam-accept-invitation"),
    
] 

urlpatterns = [
    path('family/',include(family_patterns)),
    path('company/',include(company_patterns)),
    ]      


