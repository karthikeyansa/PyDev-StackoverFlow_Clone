from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from mysite.settings import send_message
from .models import Users,Posts,Comments,Postlike,Commentlike,Polls,PollVote
from .templatetags.apptags import check,ccheck
import requests

def error_404_view(request,exception):
    return render(request,'mysite/404.html',status=404)

def error_500_view(request):
    return render(request,'mysite/500.html',status=500)

@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = get_object_or_404(Users,username = username,password = password)
            if user:
                request.session['user_id'] = user.id
                messages.add_message(request,messages.SUCCESS,'Logged in successful')
                return redirect(welcome)
        except:
            messages.add_message(request, messages.ERROR, 'Wrong credentials')
            return redirect(login)
    return render(request,'mysite/login.html')

@csrf_exempt
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        newuser = Users(username = username,password = password,email = email)
        if newuser:
            to = email
            subject = 'Hello From PyDev Community'
            body = 'Hello <i>%s</i>.<br><br>Thankyou for registering at <b>PyDev</b>.<br><i>Share us your developer stories,your ups and downs and help us to build a open source community.</i><br><br>Your PyDev account username is <b>"%s"</b>.<br>Your PyDev account password is <b>"%s"</b>.<br><br>Regards: <a href="https://pydevstackoverflow.pythonanywhere.com/"<b>PyDev</b></a>'%(username,username,password,)
            send_message(to,subject,body)
            newuser.save()
            messages.add_message(request, messages.SUCCESS, 'Account created successfully')
            return redirect(login)
        else:
            messages.add_message(request,messages.ERROR,'Username or Email Already Exists')
            return redirect(register)
    return render(request,'mysite/register.html')

@csrf_exempt
def welcome(request):
    if request.session['user_id']:
        user = Users.objects.get(id = request.session['user_id'])
        posts = Posts.objects.all().order_by('-timestamp')
        polls = Polls.objects.all().order_by('-id')
        url = 'https://www.trackcorona.live/api/countries/in'
        r = requests.get(url).json()
        covid = {
            'country' : r['data'][0]['location'],
            'confirmed' : r['data'][0]['confirmed'],
            'dead' : r['data'][0]['dead'],
            'recovered' : r['data'][0]['recovered'],
            'time':r['data'][0]['updated'][:19],
        }
        return render(request,'mysite/welcome.html',{'user':user,'posts':posts,'polls':polls,'covid':covid})


def logout(request):
    messages.add_message(request, messages.SUCCESS, 'You have logged out Successfully')
    del request.session['user_id']
    return redirect(login)
@csrf_exempt
def posts(request):
    user = Users.objects.get(id = request.session['user_id'])
    if request.method == 'POST':
        try:
            title = request.POST['title']
            body = request.POST['body']
            thumbnail = request.FILES['image']
            tags = request.POST['tags']
            author = user
            newpost = Posts(tags = tags,title = title,body = body,thumbnail = thumbnail,author = author).save()
            messages.add_message(request, messages.SUCCESS, 'Post Published successfully')
            return redirect(welcome)
        except:
            title = request.POST['title']
            body = request.POST['body']
            author = user
            tags = request.POST['tags']
            newpost = Posts(tags = tags,title=title, body=body, author=author).save()
            messages.add_message(request, messages.SUCCESS, 'Post Published successfully')
            return redirect(welcome)
    return redirect(welcome)

def home(request):
    try:
        user = Users.objects.get(id =request.session['user_id'])
        posts = Posts.objects.filter(author = user).order_by('-timestamp')
        return render(request,'mysite/home.html',{'user':user,'posts':posts})
    except:
        messages.add_message(request, messages.ERROR, 'Wrong credentials')
        return redirect(login)

def account(request):
    try:
        user = Users.objects.get(id=request.session['user_id'])
        if request.method == 'POST':
            image = request.FILES['accountimage']
            user.image = image
            user.save()
            return redirect(account)
        else:
            user = Users.objects.get(id =request.session['user_id'])
            posts = Posts.objects.filter(author = user)
            return render(request,'mysite/account.html',{'user':user,'posts':posts})
    except:
        messages.add_message(request, messages.ERROR, 'Wrong credentials')
        return redirect(login)

def deleteaccount(request):
    try:
        user = Users.objects.get(id = request.session['user_id'])
        email = user.email
        subject = 'Goodbye from PyDev'
        message = 'Hello <i>%s</i>.<br><br>This email is to confirm that PyDev has DELETED all your user-data from its servers.<br><br>Thankyou for being a member of PyDev community.<br><br>Wishing you all the best&nbsp;<b>%s</b><br><a href="https://pydevstackoverflow.pythonanywhere.com/"<b>PyDev</b></a>' % (user.username, user.username)
        send_message(email,subject,message)
        user.delete(False)
        messages.add_message(request, messages.SUCCESS, 'Account Deleted Successfully')
        return redirect(login)
    except:
        messages.add_message(request, messages.ERROR, 'Wrong credentials')
        return redirect(login)

@csrf_exempt
def changepassword(request):
    user = Users.objects.get(id = request.session['user_id'])
    if request.method == 'POST':
        newpassword = request.POST['newpassword']
        retypepassword = request.POST['retypepassword']
        oldpassword = user.password
        if newpassword == retypepassword and newpassword != oldpassword:
            user.password = newpassword
            user.save()
            messages.add_message(request, messages.SUCCESS, 'Password changed successfully')
            email = user.email
            subject = 'Password Changed From PyDev'
            message = 'Hello <i>%s</i>.<br><br>Your PyDev account password is <i>"%s"</i>.<br><br>NOTE:If you have not requested password change, your account would have been hacked.Kindly mail us for any queries.<br><br>Mail Us:<a href="mailto:impowaste39@gmail.com">&nbsp;<b>PyDev</b></a><br><br>Regards:&nbsp;<a href="https://pydevstackoverflow.pythonanywhere.com/"><b>PyDev</b></a>'%(user.username,user.password,)
            send_message(email,subject,message)
            return redirect(account)
        else:
            messages.add_message(request, messages.ERROR, 'Password mismatch or typed current password')
            return render(request,'mysite/updatepassword.html',{'user':user})
    return render(request, 'mysite/updatepassword.html', {'user': user})

def deleteprofilepic(request):
    user = Users.objects.get(id = request.session['user_id'])
    user.image.delete(False)
    user.save()
    messages.add_message(request, messages.SUCCESS, 'Profile picture deleted successfully')
    return redirect(account)

def deletepost(request,id):
    title,post = Posts.objects.get(pk = id),Posts.objects.get(id = id).delete()
    messages.add_message(request, messages.SUCCESS, 'Post named "%s" deleted succssfully'%(title.title))
    return redirect(home)

@csrf_exempt
def editpost(request,id):
    post = Posts.objects.get(id = id)
    if request.method == 'POST':
        post.tags = request.POST['tags']
        post.title = request.POST['title']
        post.body = request.POST['body']
        try:
            print(True)
            post.thumbnail = request.FILES['thumbnail']
        except:
            print(False)
            post.thumbnail = post.thumbnail
        post.save()
        return redirect(home)
    else:
        return render(request,'mysite/editpost.html',{'post':post})

@csrf_exempt
def comments(request,id):
    user = Users.objects.get(id = request.session['user_id'])
    post = Posts.objects.get(id = id)
    if request.method == 'POST':
        print(user,post)
        body = request.POST['body']
        print(body)
        newcomment = Comments(body = body,author = user,posts = post).save()
        return redirect(welcome)
    return redirect(welcome)

def deletecomment(request,id):
    comment = Comments.objects.get(id = id)
    comment.delete()
    return redirect(welcome)

def likepost(request,id,action):
    user = Users.objects.get(pk = request.session['user_id'])
    post = Posts.objects.get(pk = id)
    if action == 'like':
        like = Postlike(user = user,post = post).save()
        return redirect(welcome)
    if action == 'unlike':
        if check:
            Postlike.objects.filter(user = user,post =post).delete()
            return redirect(welcome)
    return redirect(welcome)

def likecomment(request,id,action):
    user = Users.objects.get(pk = request.session['user_id'])
    comment = Comments.objects.get(pk = id)
    if action == 'like':
        like = Commentlike(user = user,comment = comment).save()
        return redirect(welcome)
    if action == 'unlike':
        if ccheck:
            Commentlike.objects.filter(user = user,comment = comment).delete()
            return redirect(welcome)
    return redirect(welcome)
@csrf_exempt
def search(request):
    user = Users.objects.get(pk = request.session['user_id'])
    query = request.GET.get('query')
    posts = Posts.objects.filter(tags__icontains = query)
    if posts.count() == 0:
        img = True
        return render(request, 'mysite/searchresults.html',{'img':img})
    elif len(query) == 0:
        messages.add_message(request, messages.ERROR, 'No Keyword Found')
        return redirect(welcome)
    else:
        messages.add_message(request, messages.SUCCESS, 'Found : %d Posts'%(posts.count()))
        return render(request, 'mysite/searchresults.html', {'user': user, 'posts': posts})
@csrf_exempt
def createpoll(request):
    user = Users.objects.get(pk = request.session['user_id'])
    if request.method == 'POST':
        question = request.POST['question']
        choice1 = request.POST['choice1']
        choice2 = request.POST['choice2']
        newpoll = Polls(question = question,choice1 = choice1,choice2 = choice2,owner = user).save()
        return redirect(welcome)

def deletepoll(request,id):
    user = get_object_or_404(Users,pk = request.session['user_id'])
    poll = get_object_or_404(Polls, pk=id).delete()
    messages.add_message(request, messages.SUCCESS, 'Poll Deleted Successfully')
    return redirect(welcome)

@csrf_exempt
def votingpoll(request,id):
    user = get_object_or_404(Users,pk = request.session['user_id'])
    if request.method == 'POST':
        poll = get_object_or_404(Polls,pk = id)
        selected = request.POST.get('choice')
        if selected == poll.choice1:
            voting = PollVote(user = user,poll = poll).save()
            poll.choice1_total += 1
        elif selected == poll.choice2:
            voting = PollVote(user = user,poll = poll).save()
            poll.choice2_total += 1
        poll.save()
        return redirect(welcome)

@csrf_exempt
def weather(request):
    if request.method == 'POST':
        req = request.POST.get('req')
        if req.isdigit():
            res = requests.get('https://api.openweathermap.org/data/2.5/weather?zip='+ req +',in&appid=ba7bb2fcd4d0e41b8155727a76289e9f').json()
            try:
                city = {
                    'name': res['name'],
                    'temperature': int(float(res['main']['temp']) - 273.15),
                    'country': res['sys']['country'],
                    'description': res['weather'][0]['description'],
                    'icon': res['weather'][0]['icon'],
                }
            except:
                city = {'cod': '404',
                        'message': 'city not found',
                        'img':True
                        }
            return render(request, 'mysite/weatherapi.html',{'city':city})
        if req.isalpha():
            res = requests.get('https://api.openweathermap.org/data/2.5/weather?q='+ req +',in&appid=ba7bb2fcd4d0e41b8155727a76289e9f').json()
            try:
                city = {
                    'name': res['name'],
                    'temperature': int(float(res['main']['temp']) - 273.15),
                    'country': res['sys']['country'],
                    'description': res['weather'][0]['description'],
                    'icon': res['weather'][0]['icon'],
                }
            except:
                city = {'cod': '404',
                        'message': 'city not found'
                }
            return render(request, 'mysite/weatherapi.html', {'city': city})
    return render(request,'mysite/weatherapi.html')
@csrf_exempt
def forgot(request):
    if request.method == 'POST':
        data = request.POST.get('username')
        unknownuser = Users.objects.filter(username = data).first()
        unknownemail = Users.objects.filter(email = data).first()
        if unknownuser:
            username = unknownuser.username
            password = unknownuser.password
            email = unknownuser.email
            subject = 'Password Recovery From PyDev'
            message = 'Hello <i>%s</i>.<br><br>Your PyDev account password is <b>"%s"</b>.<br><br>NOTE:If you have not requested password change, your account would have been hacked.Kindly mail us for any queries.<br><br>Mail Us:<a href="mailto:impowaste39@gmail.com">&nbsp;<b>PyDev</b></a><br><br>Regards:&nbsp;<a href="https://pydevstackoverflow.pythonanywhere.com/"><b>PyDev</b></a>'%(username,password,)
            send_message(email,subject,message)
            messages.add_message(request, messages.SUCCESS, 'We have send your password to your registered email account')
            return redirect(forgot)
        elif unknownemail:
            username = unknownemail.username
            password = unknownemail.password
            email = unknownemail.email
            subject = 'Password Recovery From PyDev'
            message = 'Hello <i>%s</i>.<br><br>Your PyDev account password is <b>"%s"</b>.<br><br>NOTE:If you have not requested password change, your account would have been hacked.Kindly mail us for any queries.<br><br>Mail Us:<a href="mailto:impowaste39@gmail.com">&nbsp;<b>PyDev</b></a><br><br>Regards:&nbsp;<a href="https://pydevstackoverflow.pythonanywhere.com/"><b>PyDev</b></a>' % (username, password,)
            send_message(email,subject,message)
            messages.add_message(request, messages.SUCCESS,'We have send your password to your registered email account')
            return redirect(forgot)
        else:
            messages.add_message(request, messages.ERROR, 'No Search Results Found!')
            return redirect(forgot)
    return render(request,'mysite/forgotpassword.html')
