'''
Created on Feb 12, 2014

@author: filip
'''
from django import template
from openshift.contest.models import Contest
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from openshift.contest.models import Team

import os

register = template.Library()

@register.inclusion_tag('navigation.html')
def navigation(contest):
    links = ''
    if contest == '':
        links == 'ERROR: no links'
    else:
        links = contest.links

    return {'links': links,
            'contest': contest,}

@register.assignment_tag(takes_context=True)
def contest(context):
    request = context['request']
    url = request.path.split('/')[1]
    try:
        contest = Contest.objects.get(url=url)
        if not contest.isPublishable(): 
            raise Http404;
    except ObjectDoesNotExist:
        raise Http404
    return contest
    
@register.filter
def filename(value):
    return os.path.basename(value.file.name)

@register.filter(name='addcss')
def addcss(field, css):
   return field.as_widget(attrs={"class":css})
#TODO: implement the sponsor picture stuff
#def advert(value):
# There might be more pictures to return
#    pass
    

@register.assignment_tag(takes_context=True)
def is_on_team(context):
    request = context['request']
    url = request.path.split('/')[1]
    try:
        contest = Contest.objects.get(url=url)
        if not contest.isPublishable(): 
            raise Http404;
    except ObjectDoesNotExist:
        raise Http404
    team = Team.objects.filter(contest=contest).filter(members__id = request.user.id)
    if team.count() > 0:
        return True
    else:
        return False
