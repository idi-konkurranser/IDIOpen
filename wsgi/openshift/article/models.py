from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django import forms
# Create your models here.

class Article(models.Model):
    '''
    Articles view on the website are stored as instances of this class. 
    Articles are related to a specific contest, store what user authored them.
    Contests have a an article feed, articles can be left out of this feed by
    setting visible_article_list false. If you want an article to appear at the
    top of the article list you can set is_urgent to true.
    '''
    class Meta:
        verbose_name_plural = "View/Add Articles"
    
    title = models.CharField(max_length=200,
                             help_text = "Title of the Article, will be in a header 1 html tag")
    created_at = models.DateTimeField(auto_now_add=True)
    contest = models.ForeignKey('contest.Contest',
                                help_text = "The contest this article should be published in")
    text = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null = True, blank = True, editable = False)
    # I don't use User as a foreignkey here, so an article isn't directly linked to an User model
    #author = models.CharField(max_length=200, null = True, blank = True, editable = False)
    visible_article_list = models.BooleanField(default=True, help_text = 
                           'If this is set the article will appear in the article list. (/article/list/)')
    url = models.CharField(null = True, blank=True, max_length=200, unique=True,
                           help_text = 'Set a url to access this page with.' + 
                           'This is only needed when you need the article accessible outside of the front page.' +
                           ' If set, this article can be viewed by accessing:<strong> \'/{contesturl}/pages/{url}/\'</strong>.<br>' +
                           'To access this article, from the left-hand links on the website, you need to do this via the' +
                           ' "Links" admin interface.'+
                           '<br> You need to create a <strong>/{contesturl}/pages/{url}</strong> there for this to happen.' )
    
    is_urgent = models.BooleanField(default = False,
                                    help_text = 'If set, this article will be at the top.\
                                    Please remark that if you mark as is urgent, it will come before other articles. \
                                    ')
    
    
    def __unicode__(self):      #Default return string
        return self.title
    
