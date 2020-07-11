from django import template
from datetime import datetime

register = template.Library()

@register.inclusion_tag('_groups/_badge.html',takes_context=True)
def invite_badge(context,source):
    user = context['user']  
    # print("from invited company") 
    if source == 'company':
        invite_count = user.companyinvite_received.filter(status=0).count()
    else:
        invite_count =  user.familyinvite_received.filter(status=0).count()   
    return {'invite_count':invite_count} 


@register.inclusion_tag('_groups/_info_circle.html',takes_context=True)
def invite_plus(context,source):
    user = context['user']  
    if source == 'company':
        info = bool(user.companyinvite_received.filter(status=0))
    else:
        info =  bool(user.familyinvite_received.filter(status=0).count()   )
    return {'info':info} 
    
