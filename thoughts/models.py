from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

CONDITIONS = (
    (None,'your mood to display'),
    (0,'Ecstatic'),
    (5,'Passionate'),
    (10,'Happy'),
    (15,'Positive'),
    (20,'Content'),
    (25,'Bored'),
    (26,'Tired'),
    (27,'Hungry'),
    (30,'Pessimistic'),
    (35,'Frustrated'),
    (40,'Overwhelmed'),
    (45,'Disappointed'),
    (50,'Worried'),
    (55,'Angry'),
    (60,'Jealous'),
    (65,'Insecure'),
    (75,'Guilty'),
    (80,'Fear'),
    (85,'Grief'),
    (90,'Despair')

)
class Thought(models.Model):
    score = models.IntegerField(choices = CONDITIONS,default = 15)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='thoughts')
    recorded_at = models.DateTimeField(default=timezone.now,editable=False)
    notes = models.TextField(blank=True,default="")

    def __str__(self):
        # return str(self.score)
        # return '{}: {}'.format(self.recorded_at.strftime("%H : %M : %S, %d %a %B %Y"),self.get_condition_display()
        # .get_foo_display () |=> to retrieve the human-readable name for the field’s current value
        # короче: display то, что увидит юзер exp: "Happy"
        return "{0} : {1}".format(
            self.recorded_at.strftime("%H : %M : %S, %d %a %B %Y"),
            self.get_score_display()
            )
    class Meta:
        ordering = ("-recorded_at",)
    
