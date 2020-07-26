from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.login,name = 'login'),
    path('register',views.register,name = 'register'),
    path('welcome',views.welcome,name = 'welcome'),
    path('logout',views.logout,name = 'logout'),
    path('posts',views.posts,name = 'posts'),
    path('home',views.home,name = 'home'),
    path('account',views.account,name = 'account'),
    path('account/delete',views.deleteaccount,name = 'deleteaccount'),
    path('changepassword',views.changepassword,name = 'changepassword'),
    path('deleteprofilepic',views.deleteprofilepic,name = 'deleteprofilepic'),
    path('deletepost/<int:id>',views.deletepost,name = 'deletepost'),
    path('editpost/<int:id>',views.editpost,name='editpost'),
    path('comment/<int:id>',views.comments,name = 'comments'),
    path('deletecomment/<int:id>',views.deletecomment,name = 'deletecomment'),
    path('likepost/<int:id>/<str:action>',views.likepost,name = 'likepost'),
    path('likecomment/<int:id>/<str:action>',views.likecomment,name = 'likecomment'),
    path('search',views.search,name = 'search'),
    path('createpoll',views.createpoll,name = 'createpoll'),
    path('poll/delete/<int:id>',views.deletepoll,name = 'deletepoll'),
    path('poll/vote/<int:id>',views.votingpoll,name = 'votingpoll'),
    path('weather',views.weather,name = 'weather'),
    path('forgot',views.forgot,name = 'forgot'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)