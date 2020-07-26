from django import template
from ..models import Postlike,Posts,Users,Commentlike,Polls,PollVote
register = template.Library()

@register.filter
def check(user,post):
    try:
        liked = Postlike.objects.get(user = user.id,post = post.id)
        print('liked')
        if liked:
            return True
    except:
        return False

@register.filter
def counter(post):
    return Postlike.objects.filter(post = post.id).count()

@register.filter
def ccheck(user,comment):
    try:
        liked = Commentlike.objects.get(user = user.id,comment = comment.id)
        print('likedcomment')
        if liked:
            return True
    except:
        return False

@register.filter
def ccounter(comment):
    return Commentlike.objects.filter(comment = comment.id).count()

@register.filter
def vcheck(user,poll):
    try:
        voted = PollVote.objects.get(user = user,poll = poll)
        if voted:
            return True
    except:
        return False
