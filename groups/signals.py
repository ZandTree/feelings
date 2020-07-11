from .models import CompanyInvite,FamilyInvite
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .emails import send_invite_email

@receiver(post_save,sender=CompanyInvite)
def join_company(sender,instance,created,*args,**kwargs):
    """фиксирую момент,когда объект модели CompanyInvite создан and сохранён
    with default status === 0;однако, если его статус стал == 1(т.е. согласен присоединиться)
    то слушатель-сигнал добавит  в company members
    """
    if not created:
        print("signal company calling")
        if instance.status == 1:
            instance.company.members.add(instance.to_user)


@receiver(post_save,sender=FamilyInvite)
def join_familty(sender,instance,created,*args,**kwargs):    
    if not created:
        print("signal family calling")
        if instance.status == 1:
            instance.family.members.add(instance.to_user)            
    

# 2 signals for inviting to join company and family        
def send_invitation(sender,instance,created,*args,**kwargs):
    if created:
        send_invite_email(sender,instance.id)
        print('invitaion to join comapy,email sent')
        print('instance',instance.__class__)

post_save.connect(send_invitation,sender=CompanyInvite)
post_save.connect(send_invitation,sender=FamilyInvite)


# sender= settings.AUTH_USER_MODEL)

# @receiver(post_save, sender=User)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)


        



    