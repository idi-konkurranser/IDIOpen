from django.shortcuts import render

from .models import Article
# Create your views here.
'''
Shows all articles for a contest
TODO: Add support for published date
'''

def index(request):
    # Get the current site url
    url = request.path.split('/')[1]
    # Get the articles with foreignkey to the given contest
        
    article_list = Article.objects.all().filter(contest__url = url).exclude(visible_article_list = False).order_by("-created_at")
    context = {'article_list': article_list,
               }
    return render(request, 'article/article_list.html', context)

'''2
Shows the view for a single article
TODO: Add support for published date
'''
def detail(request, article_id):
    article = Article.objects.get(id=article_id)
    context = {'article': article,
               }
    return render(request, 'article/article.html', context)

def detail_url(request, article_url):
    try:
        article = Article.objects.get(url=article_url)
    except Exception:
        article = None
    
    context = {'article': article,
               }
    return render(request, 'article/article.html', context)
