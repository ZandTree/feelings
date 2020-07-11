from django.core.mail import send_mail
from django.http import HttpRequest
# from django.template.loader import get_template
from django.shortcuts import render


def send_invite_email(invite_class,invite_id):
    """ checks if object invite exists and retrieves attr=to_user_email
    + built-in function send_mail (params:txt and html msg's);
    used by sigmals in groups.modles

    """
    try:
        invite = invite_class.objects.get(pk=invite_id)
    except invite_class.DoesNotExist:
        pass 
    else:
        req = HttpRequest()
        text = render(req,'emails/invite_email.txt')  
        html = render(req,'emails/invite_email.html') 
        send_mail(
            subject="New invitation",
            # bytes to utf-8
            message = text.content.decode('utf-8'),
            from_email = "feelings@mail.com",
            recipient_list=[invite.to_user.email],
            html_message=html.content.decode('utf-8'),
            fail_silently=False
            )

    
