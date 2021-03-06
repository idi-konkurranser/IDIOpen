from django.db import models
from openshift.contest.models import Team, Contest
from django.conf import settings
    
class Question (models.Model):
    '''
    Questions submitted by users are stored as instances of this class.
    The questions are related to the team asking the question, and marked
    with whether or not the question has been answered.
    '''
    class Meta:
        verbose_name = "or add an answer to a question"
        verbose_name_plural = "View and answer questions"
        
    subject     = models.CharField(max_length = 120, help_text = "Max 120 chars")
    body        = models.TextField(max_length = 355, help_text = "Max 355 chars")
    sender      = models.ForeignKey(Team)
    sent_at     = models.DateTimeField(null=True, blank=True, auto_now = True)
    contest     = models.ForeignKey(Contest)
    answered    = models.BooleanField(default = False, 
                    help_text='Uncheck this if you think the question hasn\'t been answered. \
                     This checkbox will be automatically checked when an answer has been provided to the question.')

    def __unicode__(self):
        return self.subject

class QuestionAnswer(models.Model):
    '''
    This class represents the answers to the Question instances. These are created by
    privileged users(admin/judge) in response to the questions posed by contestants.
    '''
    class Meta:
        verbose_name = "Clarification"
        verbose_name_plural = "View/Add Clarifications"
   
    subject     = models.CharField(max_length = 120, help_text = "Max 120 chars")
    body        = models.TextField(max_length = 355, help_text = "Max 355 chars")
    answered_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank = True, null=True) 
    answered_at = models.DateTimeField(null=True, blank=True, auto_now = True)  
    question    = models.ForeignKey(Question, null=True, blank=True, default = None)
    contest     = models.ForeignKey(Contest, help_text = "Please specify which contest to show this clarification")
