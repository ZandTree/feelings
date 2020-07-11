from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.utils import timezone

# thirs party module django-autoslug
from autoslug import AutoSlugField
import uuid # 32 chars

# rest_frame
from rest_framework.authtoken.models import Token

class Group(models.Model):
    """this model is abstract: на её основе я создам Family and Company;
    соответственно создатель(объект класса Family or Company|=> related_name="%(class)s_created)
    """
    name = models.CharField(max_length=64)
    created_at = models.DateTimeField(default = timezone.now)
    created_by = models.ForeignKey(
                    User,
                    blank = True,
                    null=True,
                    related_name="%(class)s_created",
                    on_delete=models.SET_NULL
                    )
    description = models.TextField(default='')
    # указание на то, что берётся за основу при создании slug (here|=> name)
    slug = AutoSlugField(populate_from='name',unique=True)

    class Meta:
        abstract = True
    def __str__(self):
        return self.name

class Company(Group):
    members = models.ManyToManyField(User,related_name='companies')
    class Meta:
        verbose_name_plural = 'companies'

    def get_absolute_url(self):
        return  reverse('groups:detail-company',kwargs={'slug':self.slug})  
        
    
class Family(Group):
    members = models.ManyToManyField(User,related_name="families")
    class Meta:
        verbose_name_plural = 'families'
    def get_absolute_url(self):
        return  reverse('groups:detail-family',kwargs={'slug':self.slug}) 

INVITED_STATUSES = (
            (0,'Pending'),
            (1,'Accepted'),
            (2,'Rejected')
        )
class Invite(models.Model):
    """ sort messaging from one user to another"""
    from_user = models.ForeignKey(User,related_name='%(class)s_invites',on_delete=models.CASCADE)
    to_user = models.ForeignKey(User,related_name='%(class)s_received',on_delete=models.CASCADE)
    #accepted = models.BooleanField(default=False) 
    # был в начале, потом обнаружилось, что нужно ещё и reject|=> created choices
    status = models.IntegerField(default=0,choices=INVITED_STATUSES)
    uuid = models.CharField(max_length=32,default='',blank=True)

    class Meta:
        abstract = True

    def save(self,*args,**kwargs):
        if not self.pk:
            self.uuid = uuid.uuid4().hex
        super().save(*args,**kwargs)
    def __str__(self):
        return "{} invited {}".format(self.from_user ,self.to_user)


class FamilyInvite(Invite):
    family = models.ForeignKey(Family,related_name='invites',on_delete=models.CASCADE)

    def __str__(self):
        string = super().__str__()
        return "{} to {} family".format(string,self.family)

class CompanyInvite(Invite):
    company = models.ForeignKey(Company,related_name='invites',on_delete=models.CASCADE)
    def __str__(self):
        string = super().__str__()
        return  "{} to {} company".format(string,self.company)    





# @receiver(post_save,sender=CompanyInvite)
# def join_company(sender,instance,created,*args,**kwargs):
#     """фиксирую момент,когда объект модели CompanyInvite создан and сохранён
#     with default status === 0;однако, если его статус стал == 1(т.е. согласен присоединиться)
#     то слушатель-сигнал добавит  в company members
#     """
#     if not created:
#         print("signal company calling")
#         if instance.status == 1:
#             instance.company.members.add(instance.to_user)


# @receiver(post_save,sender=FamilyInvite)
# def join_familty(sender,instance,created,*args,**kwargs):    
#     if not created:
#         print("signal family calling")
#         if instance.status == 1:
#             instance.family.members.add(instance.to_user)            
    

# # 2 signals for inviting to join company and family        
# def send_invitation(sender,instance,created,*args,**kwargs):
#     if created:
#         send_invite_email(sender,instance.id)
#         print('invitaion to join comapy,email sent')
#         print('instance',instance.__class__)

# post_save.connect(send_invitation,sender=CompanyInvite)
# post_save.connect(send_invitation,sender=FamilyInvite)


# # sender= settings.AUTH_USER_MODEL)

# @receiver(post_save, sender=User)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)


        



    