from django import template
from thoughts.forms import ThoughtForm

import datetime
from django.utils import timezone
import json

register = template.Library()

@register.inclusion_tag('thoughts/_snip/_thought_form.html')
def thought_form():
    form = ThoughtForm()
    return {'form':form}

@register.simple_tag(takes_context=True)
def chart_data(context):
    user = context['user']
    ten_days_ago = timezone.now() - datetime.timedelta(days=7)
    thoughts_qs = user.thoughts.filter(recorded_at__gte = ten_days_ago).order_by('recorded_at')
    print("template_tags",thoughts_qs)
    #  let op: series=list of lists
    return json.dumps({'labels':[th.recorded_at.strftime('%Y-%m-%d') for th in thoughts_qs],
            'series':[[th.score*-1 for th in thoughts_qs]]
    })
"""
<QuerySet 
[<Thought: 09 : 49 : 34, 10 Fri July 2020 : Content>, 
<Thought: 19 : 16 : 32, 10 Fri July 2020 : Content>, 
<Thought: 19 : 16 : 44, 10 Fri July 2020 : Bored>, 
<Thought: 19 : 16 : 52, 10 Fri July 2020 : Happy>, 
<Thought: 21 : 46 : 16, 10 Fri July 2020 : Content>]>
"""
       



