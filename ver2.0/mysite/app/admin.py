from django.contrib import admin
from .models import Users,Posts,Comments,Postlike,Commentlike,PollVote,Polls
# Register your models here.
admin.site.register(Users)
admin.site.register(Posts)
admin.site.register(Comments)
admin.site.register(Postlike)
admin.site.register(Commentlike)
admin.site.register(PollVote)
admin.site.register(Polls)